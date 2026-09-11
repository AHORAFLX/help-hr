"""
generation_state.py
===================
Estado incremental de la generación, por ``ArticleId``.

El estado de la ejecución en curso se acumula en memoria y se vuelca a disco
cada ``FLUSH_EVERY`` artículos (antes se reescribía el JSON entero en cada
artículo, lo que hacía la generación cuadrática en número de artículos).

``generation_state.json`` solo se consolida cuando el flujo entero termina
bien; si se corta a mitad, la próxima ejecución vuelve a intentar lo que
quedó pendiente.

Requiere Python 3.12 o superior.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

STATE_FILE_NAME = "generation_state.json"
RUN_STATE_FILE_NAME = ".generation_run_state.json"

#: Cada cuántos artículos se vuelca el estado de la ejecución a disco.
FLUSH_EVERY = 200

#: Módulos cuyo contenido determina cómo queda un `.md`. Si cambia alguno, lo
#: generado antes ya no se corresponde con lo que produciría el código de hoy.
MODULOS_QUE_AFECTAN_A_LA_SALIDA = (
    'common.py', 'converters.py', 'article_fixes.py', 'repair_links.py',
)


def calcular_huella_pipeline(paquete_dir: Optional[Path] = None) -> str:
    """
    Huella del código que decide el contenido de los ``.md``.

    El estado incremental compara el ``updated_at`` del artículo en Freshdesk,
    pero no sabía nada del código. Al arreglar el conversor o los enlaces, la
    mejora solo llegaba a los artículos que por casualidad cambiaran en origen:
    el resto se quedaba con la salida antigua para siempre, sin ningún aviso.
    Con la huella, un cambio en el pipeline invalida el estado y se regenera
    todo una vez.
    """
    paquete_dir = paquete_dir or Path(__file__).resolve().parent
    resumen = hashlib.sha256()
    for nombre in sorted(MODULOS_QUE_AFECTAN_A_LA_SALIDA):
        ruta = paquete_dir / nombre
        resumen.update(nombre.encode('utf-8'))
        if ruta.exists():
            resumen.update(ruta.read_bytes())
    return resumen.hexdigest()[:16]


def huella_guardada(state: dict[str, Any]) -> str:
    return str((state.get("meta") or {}).get("pipeline_fingerprint") or "")


def pipeline_ha_cambiado(state: dict[str, Any], huella_actual: str) -> bool:
    """
    ``True`` si el código cambió desde la última ejecución consolidada.

    Un estado sin huella (de una versión anterior) también cuenta como cambio:
    no hay forma de saber con qué código se generó.
    """
    if not state.get("articles"):
        return False
    return huella_guardada(state) != huella_actual


def parse_iso_datetime(value: str) -> Optional[datetime]:
    text = str(value or "").strip()
    if not text:
        return None

    if text.endswith("Z"):
        text = text[:-1] + "+00:00"

    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None

    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def format_utc_timestamp(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + '.tmp')
    tmp_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp_path.replace(path)


def get_state_path(output_dir: Path) -> Path:
    return output_dir / STATE_FILE_NAME


def get_run_state_path(output_dir: Path) -> Path:
    return output_dir / RUN_STATE_FILE_NAME


def load_generation_state(output_dir: Path) -> dict[str, Any]:
    return _read_json(get_state_path(output_dir), {"meta": {}, "articles": {}})


def get_last_generated_at(state: dict[str, Any]) -> Optional[datetime]:
    return parse_iso_datetime((state.get("meta") or {}).get("last_generated_at") or "")


def should_generate_article(
    state: dict[str, Any],
    article_id: str,
    source_updated_at: str,
    output_path: Optional[Path] = None,
) -> bool:
    """Decide si hay que (re)generar un artículo en modo incremental."""
    if output_path is not None and not output_path.exists():
        return True

    entry = (state.get("articles") or {}).get(str(article_id))
    if not entry:
        return True

    if str(entry.get("source_updated_at") or "") != str(source_updated_at or ""):
        return True

    last_generated_at = get_last_generated_at(state)
    source_updated_dt = parse_iso_datetime(source_updated_at)
    if last_generated_at is None or source_updated_dt is None:
        return True

    return source_updated_dt > last_generated_at


class RunState:
    """
    Acumulador en memoria de los artículos generados en la ejecución actual.

    Se vuelca a disco cada ``FLUSH_EVERY`` registros para no perderlo todo si
    el proceso muere, pero sin reescribir el fichero en cada artículo.
    """

    def __init__(self, output_dir: Path, *, resume: bool = False) -> None:
        self._path = get_run_state_path(output_dir)
        self._articles: dict[str, dict[str, Any]] = {}
        self._pending = 0

        if resume:
            self._articles = dict((_read_json(self._path, {"articles": {}}).get("articles") or {}))
        elif self._path.exists():
            self._path.unlink()

    def __len__(self) -> int:
        return len(self._articles)

    def record(
        self,
        article_id: str,
        *,
        title: str,
        product: str,
        category_id: str,
        category_name: str,
        folder_id: str,
        folder_name: str,
        path: str,
        source_updated_at: str,
    ) -> None:
        self._articles[str(article_id)] = {
            "title": title,
            "product": product,
            "category_id": category_id,
            "category_name": category_name,
            "folder_id": folder_id,
            "folder_name": folder_name,
            "path": path,
            "source_updated_at": source_updated_at,
        }
        self._pending += 1
        if self._pending >= FLUSH_EVERY:
            self.flush()

    def flush(self) -> None:
        """Vuelca el estado acumulado a ``.generation_run_state.json``."""
        if not self._articles:
            return
        _write_json(self._path, {"articles": self._articles})
        self._pending = 0

    def articles(self) -> dict[str, dict[str, Any]]:
        return self._articles


def finalize_generation_state(
    output_dir: Path,
    run_state: Optional[RunState] = None,
    executed_at: Optional[str] = None,
    removed_article_ids: Iterable[str] = (),
    pipeline_fingerprint: Optional[str] = None,
) -> str:
    """
    Consolida el estado de la ejecución en ``generation_state.json``.

    Se llama una sola vez, al final del flujo completo y solo si todo ha ido
    bien. Guarda además la huella del código con el que se generó, para que la
    próxima ejecución sepa si lo de disco sigue vigente.
    """
    state_path = get_state_path(output_dir)
    run_state_path = get_run_state_path(output_dir)

    state = _read_json(state_path, {"meta": {}, "articles": {}})
    state.setdefault("meta", {})
    state.setdefault("articles", {})

    if run_state is not None:
        run_state.flush()
        generated = run_state.articles()
    else:
        generated = _read_json(run_state_path, {"articles": {}}).get("articles") or {}

    executed_at = executed_at or format_utc_timestamp(datetime.now(timezone.utc))

    for article_id, entry in generated.items():
        merged = dict(entry or {})
        merged["last_generated_at"] = executed_at
        state["articles"][str(article_id)] = merged

    for article_id in removed_article_ids:
        state["articles"].pop(str(article_id), None)

    state["meta"]["last_generated_at"] = executed_at
    state["meta"]["pipeline_fingerprint"] = pipeline_fingerprint or calcular_huella_pipeline()
    _write_json(state_path, state)

    if run_state_path.exists():
        run_state_path.unlink()

    return executed_at


def find_orphan_articles(
    state: dict[str, Any],
    live_article_ids: set[str],
    scoped_category_ids: Optional[set[str]] = None,
) -> dict[str, dict[str, Any]]:
    """
    Devuelve las entradas del estado cuyo artículo ya no existe en origen.

    ``scoped_category_ids`` limita la búsqueda a las categorías que se han
    procesado en esta ejecución: sin ese filtro, generar una sola categoría
    marcaría como huérfano todo lo demás.
    """
    orphans: dict[str, dict[str, Any]] = {}
    for article_id, entry in (state.get("articles") or {}).items():
        if str(article_id) in live_article_ids:
            continue
        if scoped_category_ids is not None:
            if str((entry or {}).get("category_id") or '') not in scoped_category_ids:
                continue
        orphans[str(article_id)] = entry or {}
    return orphans


def find_relocated_articles(
    state: dict[str, Any],
    assigned_paths: dict[str, Path],
    output_dir: Path,
    scoped_article_ids: Optional[set[str]] = None,
) -> dict[str, tuple[str, str]]:
    """
    Devuelve ``{article_id: (ruta_antigua, ruta_nueva)}`` de los artículos que
    han cambiado de sitio y cuyo ``.md`` antiguo sigue en disco.

    Un artículo que cambia de categoría, de carpeta o de título NO es un
    huérfano: sigue vivo en origen, así que ``find_orphan_articles`` no lo ve.
    Lo que queda atrás es su fichero anterior, que nadie vuelve a tocar. Aquí
    se detecta comparando la ruta guardada en el estado con la que le toca
    ahora, que ya calcula ``assign_output_paths``.

    Dos salvaguardas, para no borrar nunca la única copia de un artículo:

    - Solo se miran artículos dentro de ``scoped_article_ids`` (los de esta
      ejecución). Un artículo movido *desde* una categoría que no se está
      generando queda fuera: hace falta ``--all`` para limpiarlo.
    - Se exige que el fichero NUEVO exista ya en disco. Si su conversión falló,
      el antiguo se queda donde está.
    """
    relocated: dict[str, tuple[str, str]] = {}

    for article_id, entry in (state.get("articles") or {}).items():
        article_id = str(article_id)
        if scoped_article_ids is not None and article_id not in scoped_article_ids:
            continue

        old_rel = str((entry or {}).get("path") or "").strip()
        new_path = assigned_paths.get(article_id)
        if not old_rel or new_path is None:
            continue

        new_rel = new_path.relative_to(output_dir).as_posix()
        if old_rel == new_rel:
            continue

        old_path = output_dir / old_rel
        if old_path.suffix.lower() != ".md" or not old_path.exists():
            continue
        if not new_path.exists():
            continue

        relocated[article_id] = (old_rel, new_rel)

    return relocated
