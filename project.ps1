function _Heading
{
  Write-Host @"

********************************************************************************
*                                                                              *
*                               PYCODE TEST SCRIPT                             *
*                              University of Genova                            *
*                                                                              *
********************************************************************************

"@
}

function _Help
{
  Write-Host @"

USAGE:
./project.ps1 COMMAND [ARGS]

Available COMMANDs:

init          initialize the poetry and the building environment
build         create PyCode package wheel
test          run tests
venv          start testing environment
poetry        start poetry environment
tui           run the tui tool
help          print this help

"@
}

function _Init {
  if (-not (Test-Path "./.poetry"))
  {
    python -m venv .poetry
    ./.poetry/Scripts/Activate.ps1
    pip install -U pip setuptools
    $env:SETUPTOOLS_USE_DISTUTILS="stdlib"
    pip install poetry
    poetry init
    poetry update
    deactivate
  }
}

function _Poetry {
    $env:SETUPTOOLS_USE_DISTUTILS="stdlib"
    ./.poetry/Scripts/Activate.ps1
}

function _Venv {
  if (-not (Test-Path "./.venv"))
  {
    python -m venv ./.venv   
  }
  if ($IsWindows)
  {
    Invoke-Expression "./.venv/Scripts/Activate.ps1" 
  } else
  {
    Invoke-Expression "./.venv/bin/Activate.ps1" 
  }
}

function _Build
{
  _Init
  _Poetry
  poetry build
  deactivate
  _Venv
  pip uninstall --yes pycode
  pip install -q ./dist/pycode-0.1.0-py3-none-any.whl
}

function _Test
{
  _Venv
  python tests/test.py
  deactivate
}

function _Tui
{
  _Venv
  Start-Process powershell -ArgumentList  '-command "python ./tools/tui.py"'
  deactivate
}

function _Gui
{
  _Venv
  python ./tools/main.py
  deactivate
}

switch($args[0])
{

  "help"
  {
    _Help
  }

  "init" {
    _Init
  }

  "build"
  {
    _Build
  }

  "test"
  {
    _Test
  }

  "venv"
  {
    _Venv
  }

  "poetry" {
    _Poetry
  }

  "tui"
  {
    _Tui
  }

  "gui"
  {
    _Gui
  }

  default
  {
    _Heading
    _Help
  }
}
