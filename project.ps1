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

function _Build
{
  Push-Location ..
  python -m build "PyCode"
  Pop-Location
}

function _Test
{
  param(
    [Boolean]$Build,
    [Boolean]$JustStartVenv
  )
  if ($build)
  {
    _Build
  }
  if (-not (Test-Path "./tests/.venv"))
  {
    python -m venv ./tests/.venv   
  }
  if ($IsWindows)
  {
    Invoke-Expression "./tests/.venv/Scripts/Activate.ps1" 
  } else
  {
    Invoke-Expression "./tests/.venv/bin/Activate.ps1" 
  }
  pip uninstall --yes pycode
  pip install ./dist/pycode-0.0.1-py3-none-any.whl
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
    Invoke-Expression "./tests/.venv/Scripts/Activate.ps1"
  }

  default
  {
    _Heading
    _Help
  }
}
