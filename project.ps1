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
help          print this help

"@
}

function _Build
{
  Push-Location ..
  python -m build "PyCode"
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

  default
  {
    _Heading
    _Help
  }
}
