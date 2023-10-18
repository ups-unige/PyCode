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

build         create PyCode package wheel
test          run tests
venv          start testing environment
help          print this help

"@
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
  _Venv
  Push-Location ..
  pip install -q build hatchling
  python -m build -n -w "PyCode"
  Pop-Location
  pip uninstall --yes pycode
  pip install -q ./dist/pycode-0.0.1-py3-none-any.whl
}

function _Test
{
  _Venv
  python tests/test.py
  deactivate
}

switch($args[0])
{

  "help"
  {
    _Help
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

  default
  {
    _Heading
    _Help
  }
}
