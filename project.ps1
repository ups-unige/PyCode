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

function _Help {
  Write-Host @"

USAGE:
./project.ps1 COMMAND [ARGS]

Available COMMANDs:

test          run PyCode tests
help          print this help

"@
}

switch($args[0])
{

  "help" {
    _Help
  }

  default
  {
    _Heading
    _Help
  }
}
