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
help          print this help

"@
}

function _Build
{
  Push-Location ..
  python -m build "PyCode"
  Pop-Location
}

function _Test
{
  Push-Location "tests"
  if (-not (Test-Path "./.venv"))
  {
    python -m venv .venv   
  }
  if ($IsWindows)
  {
    Invoke-Expression ".venv/Scripts/Activate.ps1" 
  }
  else
  {
    Invoke-Expression ".venv/bin/Activate.ps1" 
  }
  pip uninstall --yes pycode
  pip install ./dist/pycode-0.0.1-py3-none-any.whl
  python test.py
  Pop-Location
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
    _Build
    _Test
  }

  default
  {
    _Heading
    _Help
  }
}
