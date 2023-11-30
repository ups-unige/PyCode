################################################################################
#                           ENVIRONMENT VARIABLES
################################################################################

$project = Split-Path -Path (Get-Location) -Leaf
$env:SETUPTOOLS_USE_DISTUTILS="stdlib"

################################################################################
#                                  UTITITIES
################################################################################

function check_n_pop_directory([String]$name)
{
  New-Item -Type Directory -Path $name -ErrorAction Ignore
  Push-Location $name
}

function activate_conda()
{
  if ( $IsWindows )
  {
    conda shell.powershell hook | Out-String | Invoke-Expression
  } elseif ( $IsLinux )
  {
    Write-Information "TODO"
    return
  } else
  {
    Write-Information "TODO"
    return
  }
}

function download_python([string]$python_version, [string]$os_version)
{
  $python_url=  "https://www.python.org/ftp/python/$python_version/python-$python_version-embed-$os_version.zip"
  Invoke-WebRequest -Uri $python_url -OutFile python.zip
  Expand-Archive -path python.zip -DestinationPath build
}



################################################################################
#                                   TASKS
################################################################################
# 
# to build the project it's necessary the anaconda package manager. it is used
# to download the python interpreter and libraries and to download conan, a C++
# package manager used to get the C++ libraries




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
tui           run the tui tool
help          print this help

"@
}

function _Init
{
  $conda = (Get-Command conda -ErrorAction SilentlyContinue)  
  if ($null -eq $conda)
  {
    Write-Error "conda is not installed or available in PATH. install it first."
    return
  } else
  {
    activate_conda
    conda create -n devel conan poetry setuptools
    conda activate devel
    conan profile detect --force
    conan install . --output-folder=build --build=missing -s compiler.cppstd=20 -s build_type=Debug
    poetry init
    poetry update
    download_python "3.10.0" "amd64" 
    conda deactivate
  }
}

function _Venv
{
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
  check_n_pop_directory("build")
  cmake -G"Ninja" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON $arg_list ..
  cmake --build .
  Pop-Location
  poetry build
  _Venv
  pip uninstall --yes pycode
  pip install -q ./dist/pycode-0.1.0-py3-none-any.whl
}

function _Run
{
  check_n_pop_directory("build")
  $command = './' + $project
  Invoke-Expression $command
  Pop-Location
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

  "init"
  {
    _Init
  }

  "build"
  {
    _Build($args[1..($args.Length)])
  }

  "run" {
    build($args[1..($args.Length)])
    run
  }

  "python"
  {
    download_python "3.10.0" "amd64" 
  }

  "clean"
  {
    Remove-Item -Force -Recurse -Path "./build"
  }

  "test"
  {
    _Test
  }

  "venv"
  {
    _Venv
  }

  "poetry"
  {
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

  "conda"
  {
    activate_conda
  }

  default
  {
    _Heading
    _Help
  }
}
