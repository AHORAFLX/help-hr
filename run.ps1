<#
.SYNOPSIS
    Lanzador interactivo de la migración de Freshdesk a MkDocs.

.DESCRIPTION
    Pregunta qué producto generar y con qué opciones, enseña la orden final y
    la ejecuta. Equivale a escribir "python migrate.py --product ... --flags"
    a mano, pero sin tener que recordar los flags ni cómo se llama cada
    producto.

    Uso:
        .\run.ps1

    Requiere Python 3.12 o superior y un .env con la cadena de conexión.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$MigrateScript = Join-Path $Root 'migrate.py'

# ---------------------------------------------------------------------------
# Pintado
# ---------------------------------------------------------------------------

function Write-Titulo {
    param([string]$Texto)
    Write-Host ''
    Write-Host ('  ' + $Texto) -ForegroundColor Cyan
    Write-Host ('  ' + ('-' * $Texto.Length)) -ForegroundColor DarkCyan
}

function Write-Aviso {
    param([string]$Texto)
    Write-Host ('  ' + $Texto) -ForegroundColor Yellow
}

function Write-Error2 {
    param([string]$Texto)
    Write-Host ('  ' + $Texto) -ForegroundColor Red
}

function Show-Cabecera {
    Clear-Host
    Write-Host ''
    Write-Host '  ==========================================================' -ForegroundColor Cyan
    Write-Host '    Freshdesk  ->  MkDocs      generacion de documentacion' -ForegroundColor Cyan
    Write-Host '  ==========================================================' -ForegroundColor Cyan
}

# ---------------------------------------------------------------------------
# Python
# ---------------------------------------------------------------------------

function Get-Python {
    <#
        En una terminal abierta antes de instalar Python 3.12, "python" resuelve
        al stub de la Microsoft Store, que no sirve. Por eso se busca primero la
        instalacion concreta.
    #>
    $candidatos = @(
        (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'),
        (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'),
        'C:\Python312\python.exe'
    )

    foreach ($ruta in $candidatos) {
        if (Test-Path $ruta) { return $ruta }
    }

    $enPath = Get-Command python -ErrorAction SilentlyContinue
    if ($enPath) {
        $version = & $enPath.Source -c "import sys; print(sys.version_info >= (3, 12))" 2>$null
        if ($version -eq 'True') { return $enPath.Source }
    }

    return $null
}

# ---------------------------------------------------------------------------
# Menu de producto
# ---------------------------------------------------------------------------

function Get-Productos {
    param([string]$Python)

    Write-Host ''
    Write-Host '  Consultando productos en la base de datos...' -ForegroundColor DarkGray

    $salida = & $Python $MigrateScript --list-products
    if ($LASTEXITCODE -ne 0) { return $null }

    $productos = @()
    foreach ($linea in $salida) {
        $partes = $linea -split '\|'
        if ($partes.Count -eq 3) {
            $productos += [pscustomobject]@{
                Nombre     = $partes[0]
                Categorias = [int]$partes[1]
                Articulos  = [int]$partes[2]
            }
        }
    }
    return $productos
}

function Select-Producto {
    param([array]$Productos)

    Write-Titulo 'Que quieres generar'

    $ancho = ($Productos | ForEach-Object { $_.Nombre.Length } | Measure-Object -Maximum).Maximum
    $indice = 1
    foreach ($p in $Productos) {
        $etiqueta = $p.Nombre.PadRight($ancho)
        $numero = ('{0,2}' -f $indice)
        Write-Host ("   [$numero] ") -ForegroundColor Green -NoNewline
        Write-Host $etiqueta -NoNewline
        Write-Host ("   {0,5} articulos   {1,2} categorias" -f $p.Articulos, $p.Categorias) -ForegroundColor DarkGray
        $indice++
    }

    $totalArticulos = ($Productos | Measure-Object -Property Articulos -Sum).Sum
    Write-Host ''
    Write-Host '   [ T] ' -ForegroundColor Green -NoNewline
    Write-Host ('TODO'.PadRight($ancho)) -NoNewline
    Write-Host ("   {0,5} articulos   (--all)" -f $totalArticulos) -ForegroundColor DarkGray
    Write-Host '   [ C] ' -ForegroundColor Green -NoNewline
    Write-Host ('Una categoria concreta, por nombre'.PadRight($ancho)) -ForegroundColor Gray

    while ($true) {
        Write-Host ''
        $respuesta = (Read-Host '  Elige una opcion').Trim()

        if ($respuesta -eq '') { continue }

        if ($respuesta.ToUpper() -eq 'T') {
            return @{ Flags = @('--all'); Descripcion = 'todas las categorias' }
        }

        if ($respuesta.ToUpper() -eq 'C') {
            $nombre = (Read-Host '  Nombre de la categoria').Trim()
            if ($nombre -eq '') { continue }
            return @{
                Flags       = @('--categories', $nombre, '--category-contains')
                Descripcion = "categorias que contengan '$nombre'"
            }
        }

        $numero = 0
        if ([int]::TryParse($respuesta, [ref]$numero)) {
            if ($numero -ge 1 -and $numero -le $Productos.Count) {
                $elegido = $Productos[$numero - 1]
                return @{
                    Flags       = @('--product', $elegido.Nombre)
                    Descripcion = "el producto '$($elegido.Nombre)' ($($elegido.Articulos) articulos)"
                }
            }
        }

        Write-Error2 'Opcion no valida.'
    }
}

# ---------------------------------------------------------------------------
# Menu de opciones
# ---------------------------------------------------------------------------

function Select-Opciones {
    $opciones = @(
        [pscustomobject]@{
            Flag = '--prune-orphans'; Activa = $true
            Titulo = 'Limpiar los .md que sobran'
            Ayuda  = 'Borra los articulos eliminados en origen, movidos o renombrados'
        },
        [pscustomobject]@{
            Flag = '--include-drafts'; Activa = $false
            Titulo = 'Incluir borradores'
            Ayuda  = 'Publica tambien los articulos en estado borrador'
        },
        [pscustomobject]@{
            Flag = '--force'; Activa = $false
            Titulo = 'Regenerar todo'
            Ayuda  = 'Ignora el estado incremental: reescribe hasta lo no modificado'
        },
        [pscustomobject]@{
            Flag = '--clean-output'; Activa = $false
            Titulo = 'Vaciar docs/ antes de empezar'
            Ayuda  = 'Borra lo generado (conserva el tema y las portadas). Implica regenerar todo'
        },
        [pscustomobject]@{
            Flag = '--skip-link-repair'; Activa = $false
            Titulo = 'Saltar la reparacion de enlaces'
            Ayuda  = 'Mas rapido, pero deja los enlaces internos sin repasar'
        }
    )

    while ($true) {
        Write-Titulo 'Opciones'

        $indice = 1
        foreach ($o in $opciones) {
            if ($o.Activa) {
                $marca = '[x]'
                $color = 'Green'
            } else {
                $marca = '[ ]'
                $color = 'DarkGray'
            }
            Write-Host ("   $indice. ") -NoNewline
            Write-Host $marca -ForegroundColor $color -NoNewline
            Write-Host (' ' + $o.Titulo)
            Write-Host ('        ' + $o.Ayuda) -ForegroundColor DarkGray
            $indice++
        }

        Write-Host ''
        Write-Host '  Escribe un numero para activar o desactivar, o Enter para continuar.' -ForegroundColor DarkGray
        $respuesta = (Read-Host '  >').Trim()

        if ($respuesta -eq '') { break }

        $numero = 0
        if ([int]::TryParse($respuesta, [ref]$numero) -and $numero -ge 1 -and $numero -le $opciones.Count) {
            $opciones[$numero - 1].Activa = -not $opciones[$numero - 1].Activa
        } else {
            Write-Error2 'Opcion no valida.'
        }
    }

    $flags = @()
    foreach ($o in $opciones) {
        if ($o.Activa) { $flags += $o.Flag }
    }
    return $flags
}

# ---------------------------------------------------------------------------
# Programa
# ---------------------------------------------------------------------------

Show-Cabecera

$Python = Get-Python
if (-not $Python) {
    Write-Host ''
    Write-Error2 'No se encuentra Python 3.12 o superior.'
    Write-Host '  Instalalo y abre una terminal NUEVA: en una ya abierta, "python"' -ForegroundColor Gray
    Write-Host '  sigue resolviendo al stub de la Microsoft Store.' -ForegroundColor Gray
    exit 1
}

if (-not (Test-Path (Join-Path $Root '.env'))) {
    Write-Host ''
    Write-Error2 'Falta el fichero .env con la cadena de conexion.'
    Write-Host '  Copia .env.example a .env y rellenalo.' -ForegroundColor Gray
    exit 1
}

$productos = Get-Productos -Python $Python
if (-not $productos -or $productos.Count -eq 0) {
    Write-Host ''
    Write-Error2 'No se ha podido leer la lista de productos.'
    Write-Host '  Revisa la cadena de conexion del .env y que SQL Server responda.' -ForegroundColor Gray
    exit 1
}

$seleccion = Select-Producto -Productos $productos
$flags = Select-Opciones

$argumentos = @($MigrateScript) + $seleccion.Flags + $flags

# --- Resumen antes de tocar nada -------------------------------------------
Write-Titulo 'Resumen'
Write-Host '   Se va a generar: ' -NoNewline
Write-Host $seleccion.Descripcion -ForegroundColor White

if ($flags -contains '--clean-output') {
    Write-Host ''
    Write-Aviso 'OJO: --clean-output borra lo generado y obliga a regenerarlo todo.'
}
if ($flags -contains '--include-drafts') {
    Write-Aviso 'OJO: se publicaran tambien los borradores.'
}
if ($flags -notcontains '--prune-orphans') {
    Write-Host '   Los ficheros que sobren solo se listaran, no se borraran.' -ForegroundColor DarkGray
}

Write-Host ''
Write-Host '   Orden: ' -ForegroundColor DarkGray -NoNewline
Write-Host ('python ' + (($argumentos | ForEach-Object {
    if ($_ -match '\s') { '"' + $_ + '"' } else { $_ }
}) -join ' ')) -ForegroundColor Gray

Write-Host ''
$confirmacion = (Read-Host '  Adelante? (S/n)').Trim()
if ($confirmacion -ne '' -and $confirmacion.ToUpper() -ne 'S') {
    Write-Host ''
    Write-Host '  Cancelado. No se ha tocado nada.' -ForegroundColor DarkGray
    exit 0
}

# --- A trabajar ------------------------------------------------------------
Write-Host ''
Write-Host '  ----------------------------------------------------------' -ForegroundColor DarkCyan
$inicio = Get-Date

Push-Location $Root
try {
    & $Python $argumentos
    $codigo = $LASTEXITCODE
} finally {
    Pop-Location
}

$duracion = (Get-Date) - $inicio
Write-Host '  ----------------------------------------------------------' -ForegroundColor DarkCyan
Write-Host ('  Duracion: {0:hh\:mm\:ss}' -f $duracion) -ForegroundColor DarkGray

if ($codigo -eq 0) {
    Write-Host ''
    Write-Host '  Terminado sin incidencias.' -ForegroundColor Green
} else {
    Write-Host ''
    Write-Aviso 'Terminado CON incidencias. Mira el parte de arriba y los logs:'
    Write-Host ('  ' + (Join-Path $Root 'logs')) -ForegroundColor Gray
}

Write-Host ''
Write-Host '  Para ver el resultado en el navegador:' -ForegroundColor DarkGray
Write-Host '      mkdocs serve' -ForegroundColor Gray
Write-Host ''

exit $codigo
