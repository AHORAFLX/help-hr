---
name: sebastian-docs-style
description: House style and structure rules for the Sebastian HR MkDocs documentation in this repo (docs/**/*.es.md, Spanish). Load this before creating, editing, reviewing, or "cleaning up" any file under docs/ — heading casing and depth, admonition syntax, list markers, when a bulleted list should become a table, breadcrumb notation, the PRO/LITE feature badge, and Freshdesk-migration artifacts to fix on sight. Trigger even when the request doesn't say "style" or "convention" — e.g. "add a section about X", "document the new Y field", "fix this page", "tidy up this list", "add a table for Z" all imply following these rules. Also load it before writing a *new* doc page from scratch under docs/.
---

# Sebastian HR docs style

This repo is a MkDocs Material site for Sebastian HR product docs. All content is
Spanish-language Markdown under `docs/**/*.es.md`, one topic folder per area.
`mkdocs.yml` has no `nav:` (navigation is auto-generated from the folder tree and
each file's H1 / frontmatter `title:`) and `toc_depth: 3` (the right-side page
outline only shows H1–H3 — anything deeper is structurally invisible to a reader).

The pages were bulk-migrated from Freshdesk via a Python pipeline
(`NOTAS-DEL-PIPELINE.md`) and then hand-edited, so they carry a recognizable set
of migration scars (see "Artifacts to fix on sight" below). You'll see these
constantly — fix them in passing whenever you touch a line that has one, even if
that wasn't the point of the edit.

The rules below aren't arbitrary — most exist because `toc_depth: 3` and the
anchor-based navigation actually break in specific ways if you don't follow them.
Understanding *why* a rule exists tells you how to handle the case it doesn't
quite cover.

## Headings

- **One H1 per file** (the page title). Don't recase it, even if it's Title Case
  and everything else is sentence case — the H1 drives the sidebar nav label and
  changing it changes what readers see in navigation, which is a bigger decision
  than a style pass.
- **Keep the H1 short enough to fit on one line** in the sidebar. Trim
  descriptive subtitles/qualifiers bolted onto a title (e.g. "Dudas legales
  sobre geolocalización de los empleados en su jornada de trabajo" →
  "Dudas legales sobre la geolocalización", "Modificación Masiva de Datos de
  Empleados" → "Modificación Masiva de Empleados") — keep the words that
  distinguish the page, drop the rest. If the title loses essential context make it so it takes more than one line, but don't add extra words just to make it longer.
- **H2/H3 in sentence case**: "Cómo funciona", not "Cómo Funciona" or
  "CÓMO FUNCIONA". Keep acronyms and proper nouns capitalized wherever they'd
  naturally be capitalized: PRO, LITE, ERP, RFID, NFC, QR, SQL, IIS, FAQ, AHORA,
  DNI, NIE, IBAN, IC, SP, A3NOM, and camelCase/PascalCase identifiers like
  `DateJourney`, `CheckTime`, product names like Kapri, Tally, ABH Sign. Literal
  `¿...?` question headings keep their natural casing as written.
- **Max depth is H3.** Never write `####`. If content genuinely wants a 4th
  level of nesting, either flatten the deepest layer so it becomes a sibling at
  H3 (accept the lost visual nesting) or demote it to a **bold inline label**
  instead of a heading — this is common for "sub-values of one field" style
  content (e.g. a field's possible states). Reason: `toc_depth: 3` means H4+
  never appears in the page outline, so a reader literally cannot navigate to
  it — treat "would need H4" as a signal the content should be restructured,
  not an excuse to go deeper.
- **No skipped levels**: don't jump from the file's H1 straight to H3. The
  first heading after the H1 is always H2.
- **No two headings with identical text in the same file.** MkDocs slugifies
  heading text into anchors, so duplicates collide (`#foo`, `#foo_1`, `#foo_2`)
  and deep links become unpredictable. Disambiguate using context that's
  already sitting right there in the surrounding content (e.g. "Configuración
  de reglas" → "Configuración de reglas por solicitud" /
  "... por periodo"), not by bolting a number onto the heading.
- **Strip manual numbering**: `1\.`, `1.`, `2.1`, `Paso 1:`, and lettered
  variants like `A.`/`B.` (e.g. "## A. Flujo de un solo paso" →
  "## Flujo de un solo paso") at the start of a heading should go — MkDocs
  orders sections by document position on its own, so the label is pure
  redundant noise (and `1\.` is actively broken, see below). The one place
  numbering-like suffixes have stuck as a deliberate, reader-facing convention
  is `(N.1)` / `(N.2)` — used for a handful of strictly-ordered priority
  levels where the number *is* the information (e.g. which of several
  assignment methods wins). If a file already uses that pattern, match it;
  don't introduce it elsewhere without a reason as strong as "the order itself
  is the content."
- **Strip a trailing colon from a heading**: "### Otras tablas modificadas:" →
  "### Otras tablas modificadas".
- **Promote an enumerated "case" label into a short heading, not a verbatim
  one.** Migrated content often lists worked examples as plain sentences like
  "Caso 3: El empleado ficha un descanso con tiempo superior al tiempo de
  descanso del turno" or "Caso de Uso – Excesos extraordinarios en la
  jornada:". Turn these into H3s, but drop the `Caso N:` / `Caso de Uso – `
  prefix and the generic repeated subject ("El empleado") along with it,
  keeping only the part that actually distinguishes this case from its
  siblings, sentence case, no trailing colon/period: → "### Ficha un descanso
  con tiempo superior al tiempo de descanso del turno",
  "### Excesos extraordinarios en la jornada".
- **Promote plain-text section labels to real headings.** A lot of migrated
  content has what's clearly meant as a section break — a short standalone
  line before a block of related paragraphs/images — written as plain text
  instead of `##`/`###`. These are invisible to the TOC and to search. This is
  the single highest-value fix in the whole style pass: one page went from 2
  headings across 316 lines to 16 real, navigable sections just by promoting
  labels that were already structurally sections in everything but markup.
  Look for it whenever a page feels like it "has no navigation" even though
  it's clearly organized into topics.
- **A heading must carry its own text** — never just an image (`## ![](...)`)
  and never text with an image glued to the end with no space
  (`## Config![](...)`). Give the image its own line below.

## Admonitions

Use MkDocs's `!!! type "Title"` syntax (body indented 4 spaces) instead of a
blockquote or a plain "Nota: ..." paragraph, whenever the content is clearly a
labeled callout:

| Original label | Admonition |
| --- | --- |
| Importante / Atención / Advertencia | `!!! warning "Importante"` |
| Nota | `!!! note "Nota"` |
| Ejemplo | `!!! example "Ejemplo"` |
| Recomendación / Consejo | `!!! tip "Recomendación"` |
| Paired "do this" / "don't do this" | `!!! success "Haz esto"` / `!!! failure "Evita esto"` |

A plain `>` blockquote that's just a gentle unlabeled aside (no "Nota:"-style
lead-in, nothing warning-shaped) is fine to leave as a blockquote — not every
`>` needs to become a box. If you do want to admonition-ize an unlabeled aside,
inventing a short, specific title (`!!! info "Reutilización de ajustes"`) is
fine — this has already been done in the project. When genuinely unsure whether
something reads as a callout, ask rather than mass-converting every blockquote
in a file.

A blockquote or plain sentence that states a **hard precondition or
requirement** ("Para calcular los ajustes... estas jornadas deben estar en
estado BALANCE") reads as `!!! warning "..."` with an invented short title
(e.g. `!!! warning "Requisito previo"`), not `!!! note` — reserve `note` for
softer contextual asides.

An italicized standalone sentence that walks through a worked example — with
or without the literal word "Ejemplo" — is the same pattern as an explicit
"Ejemplo:" label: wrap it in `!!! example "Ejemplo"` and de-italicize the
body. This includes a lead-in like "_Por ejemplo, si el turno finaliza a las
18:00 y configuras 10 minutos..._" and a "Por ejemplo, un empleado podría:"
paragraph immediately followed by bullets — the bullets move inside the
admonition body too.

## Lists

- Bullets: `- item`, zero indent at the top level, +2 spaces per nested level.
  Not `* item` or `  * item` — that indent-and-asterisk combination is the
  original pipeline's bullet style and should be normalized to `-` on sight
  whenever you're touching a list, even if converting bullets wasn't the task.
- **Zero-indent applies even when the marker is already correct.** A whole
  pass ("Improved lists") existed just to fix `  - item` / `  1. item` at the
  top level down to `- item` / `1. item` — an indented top-level marker is a
  bug to fix on sight, not just a `*`-vs-`-` one.
- Numbered lists: `1. item`, never `1\.`. The escaped period is not cosmetic —
  Python-Markdown's list parser doesn't recognize `1\.` as a list marker at
  all, so the "list" silently renders as plain paragraphs with no numbering.
  Any time you see `\.` after a leading digit, that's a real rendering bug, not
  a style nit.
- **Bold the label in a `Label: description` bullet that stays a list** (i.e.
  when it doesn't meet the bar below to become a table): `- **Fijos**: Se
  aplican automáticamente...`. This is the same visual pattern as a table's
  left column, just without converting to one — plain-text or italicized
  labels (`_Empleado_: Elegir...`) get bolded on sight.
- **Unroll a run-on sentence that enumerates several terminating/exclusive
  conditions** (chained with commas, "o", "o bien") into a short lead-in plus
  a bulleted list, e.g. "...hasta que exista una separación... o bien la
  duración total... exceda, o finalmente, el nuevo fichaje se encuadre..."
  becomes "...hasta que ocurra alguna de estas situaciones:" followed by one
  bullet per condition. Do this when the sentence is listing 2+ alternative
  conditions, not for a simple two-clause sentence.

## When a list should become a table

Convert a run of **3 or more** consecutive bullets shaped like
`**Label**: description` or `Label: description` into a table when the list is
enumerating one of these:

- form fields or dialog/config parameters ("Rellena estos campos: ...")
- data/report columns
- lookup or enum values (percentage brackets, status values, etc.)

```
| Campo | Descripción |
| --- | --- |
| Fecha de inicio | Primer día del periodo a consultar. |
| Fecha final | Último día del periodo a consultar. |
```

Pick the column header to fit what's actually being listed — `Campo |
Descripción` is the default, but `Requisito | Especificación`,
`Valor | Significado`, and `Campo | Valor por defecto` all show up depending on
context.

**Don't** convert feature-highlight lists, use-case/example lists,
requirement or warning checklists, worked step-by-step examples, or short
ranked-priority lists — these read better as prose bullets, and forcing them
into a table has already been explicitly reverted once by the project owner
(a short concept glossary went table → bold-label bullets, not the other
way). When a list is borderline, lean toward leaving it as bullets rather than
manufacturing a two-column table for content that isn't really tabular.

Two things worth double-checking whenever you do convert:
- **Read the whole list first.** A past mistake here was converting only the
  first chunk of items my detector/scan happened to catch and leaving the
  tail of the same list as stray un-converted bullets right after the new
  table. If you see a bullet sitting immediately below a table that looks
  like it belongs in it, it probably got missed.
- Cells can't contain a literal newline — use `<br>` for a line break inside
  one cell (e.g. stacking several `**Option**: text` fragments in a single
  "Tipo" cell).

## Breadcrumbs / menu paths

Every mention of a UI navigation path becomes backtick-wrapped with `>` as the
separator, regardless of how it was originally written —
`A/B/C`, `A → B → C`, `A\B`, hyphen-joined, whatever:

```
`Mantenimiento > Fichajes > Reglas de control de localización`
```

Watch for false positives before touching a `→` or `>`: an arrow used for
cause → effect logic ("Si el fichaje entra dentro del rango → se asigna el
turno") and a `>` used as a numeric comparison ("si el valor > límite") are
not breadcrumbs. Only convert sequences of menu/screen names.

## PRO/LITE feature badge

`docs/stylesheets/custom.css` defines `.fh-version-tag.hr-pro-mode` (gold) and
`.fh-version-tag.hr-lite-mode` (grey). Only the PRO badge has an established
usage pattern so far — don't invent LITE-badge markup without checking with
the user first, since there's no existing example to match against.

Replace plain-text annotations like "(Solo modo PRO)" / "(solo en modo PRO)"
with the badge:

```html
<!-- heading suffix / inline -->
<span class="fh-version-tag hr-pro-mode" title="Disponible en modo pro">Pro</span>

<!-- bullet prefix (needs the spacing classes or it crowds the text) -->
<span class="fh-version-tag hr-pro-mode no-margin margin-right-s" title="Disponible en modo pro">Pro</span>
```

Attach the badge to the heading/bullet that's *already there* describing the
PRO-only thing. Don't create a separate heading or bullet just to hold the
badge — an early pass in this project did that (a redundant "### Solo modo
PRO" sub-heading under each PRO-only section) and the project owner later
simplified it by merging the badge straight onto the parent heading instead.

## Images

- Never glue `![](...)` to the end of a text line or list item — give it its
  own line, with a blank line before it (indented to match the list item it
  illustrates, if any).
- Drop the Freshdesk-artifact italic wrapper around a standalone image:
  `_![](...)_ ` → `![](...)`.

## Artifacts to fix on sight

These come from the Freshdesk → pipeline → hand-edit history and show up
constantly. Fix them whenever you're touching a line that has one:

- `1\.` (escaped-period numbering) — breaks list parsing, see above.
- Curly/typographic quotes (`“…”`, `‘…’`) — replace with straight quotes
  (`"…"`, `'…'`). This is one of the most common fixes across the corpus;
  normalize on sight anywhere you're touching a line that has one, including
  inside admonitions and table cells.
- Text glued together with no space where an HTML tag boundary used to be —
  e.g. `ConfTabla: Objects` should split into a `Conf` label and a separate
  `Tabla: Objects` line; `Enabled = 1Tabla:` is missing a line break in the
  middle.
- A stray space before `:` or `,` — "Importante : Si..." → "Importante: Si...".
- "Sebastián HR" (with an accent) — the product name is "Sebastian HR", no
  accent. Always a typo, fix it.
- A heading marker with nothing after it but whitespace/`&nbsp;` (`###`,
  `####   `) — delete the line, don't leave an empty heading.
- Runs of multiple blank/whitespace-only lines between real content — collapse
  to exactly one blank line.

## Before considering a batch of edits done

Quick self-check, not a literal script (exact tooling varies by session):

- No heading exceeds H3; no heading skips a level from the file's H1.
- No two headings in one file share identical text.
- Every internal link (`[text](path.md)`) resolves to a file that actually
  exists — pages in this repo have been renamed before without every
  referencing link (especially in `docs/index.es.md`) getting updated, so this
  is a real, recurring failure mode, not a theoretical one.
- No leftover multi-blank-line runs.
- Every table you touched has its header separator row (`| --- | --- |`)
  immediately under the header row.

## Explicitly out of scope (don't freelance a rule here — ask)

Two things are known-inconsistent across the corpus with no house rule decided
yet. Don't invent one unilaterally while doing an unrelated edit:

1. **Bold vs. backtick-code for UI element/field names** — both are used
   across the corpus with no clear pattern yet.
2. **Generic opening sections** like "## Descripción General" / "##
   Introducción" — some pages have them, some don't, and normalizing this
   means judgment-heavy rewrites of each page's intro, not a mechanical rule.
