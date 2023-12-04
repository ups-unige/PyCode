################################################################################
#                             PYCODE UTILITY SCRIPT                            
#                              Università di Genova                            
#                                                                              
# Initialize, build and run the PyCode or the CodePP libraries and binaries.
# The requirements for using this script are:
# - powershell (the cross platform version should be valid if not on Windows)
# - a C++ compiler with the c++ standard 20 support (i've used mingw-w64)
# - CMake
# - ninja
# - anaconda3
# - Qt6 framework installed or an open source qt licence credentials

################################################################################
#                           ENVIRONMENT VARIABLES
################################################################################

$ErrorActionPreference = 'Stop'
# $this_dir = (Get-Location).Path
$project = Split-Path -Path (Get-Location) -Leaf
# modify the following variable to point to the qt6 install folder
$env:Qt6_ROOT="D:\Qt\6.6.0\mingw_64\"

################################################################################
#                                  UTITITIES
################################################################################

# Check if a directory exists and create it if not. Then pop its location
function Script:check_n_pop_directory([String]$name)
{
  New-Item -Type Directory -Path $name -ErrorAction Ignore
  Push-Location $name
}

# Run a python command with the build python interpreter
function Script:PythonCommand([String]$command)
{
  if (-not (Get-Item -Path "build/python39._pth"))
  {
    DownloadPython "3.9.0" "amd64" 
  }
  build/python $command
}

# This function permit to avoid adding the conda initialization on the default
# script that starts with the shell saving a slowdown on each shells start
function Script:ActivateConda()
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

function Script:Heading
{
  Write-Host @"

********************************************************************************
*                                                                              *
*                             PYCODE UTILITY SCRIPT                            *
*                              Università di Genova                            *
*                                                                              *
********************************************************************************

"@
}

function Script:Help
{
  Write-Host @"

USAGE:
./project.ps1 COMMAND [ARGS]

Available COMMANDs:

init                            initialize or reset the development environment
build [-PyCode/-CodePP/-All]    create PyCode package wheel
gui                             run the gui tool
tui                             run the tui tool (not updated anymore)
help                            print this help

"@
}


################################################################################
#                                  GET RESOURCES
################################################################################

# Download and install an embeddable python distribution in the build folder
# to be used for the embedded python interpreter in CodePP. Also installs pip
# so that the required libraries could be installed
function Script:DownloadPython([string]$python_version, [string]$os_version)
{
  $python_url=  "https://www.python.org/ftp/python/$python_version/python-$python_version-embed-$os_version.zip"
  Invoke-WebRequest -Uri $python_url -OutFile python.zip
  Expand-Archive -path python.zip -DestinationPath "build" -Force
  Invoke-WebRequest -Uri "https://bootstrap.pypa.io/get-pip.py" -OutFile build/get-pip.py
  ./build/python ./build/get-pip.py
  Add-Content -Path "build\python$(($python_version -replace '[^0-9]','').Substring(0, 2))._pth" -Value "Lib/site-packages"
}

# Installation of the Qt6 framework locally in the development environment
function Script:InstallQt([string]$qt_installer_version, [string]$os_version)
{
  switch ($os_version)
  {
    "windows"
    {
      $qt_installer_suffix = "exe"
    }
    "linux"
    {
      $qt_installer_suffix = "run"
    }
    "macos"
    {
      $qt_installer_suffix = "dmg"
    }
  }
  $qt_url = "https://d13lb3tujbc8s0.cloudfront.net/onlineinstallers/qt-unified-$os_version-x64-$qt_installer_version-online.$qt_installer_suffix"
  Invoke-WebRequest -Uri $qt_url -OutFile qt_installer.exe
  ./qt_installer
}

################################################################################
#                               INIT ENVIRONMENTS
################################################################################
# this will get conan to install binaries and artifacts locally
$env:CONAN_HOME="$((Get-Location).Path)/devel/conan"
# i don't remember this one. maybe it's used by poetry to compile wheels with 
# mingw_w64
$env:SETUPTOOLS_USE_DISTUTILS="stdlib"

# Clean the development environment
function Script:DevelClean
{
  Remove-Item -Force -Recurse -Path "./devel" -ErrorAction Ignore
}

# Create a conda environment and install conan and poetry in it
function Script:DevelConda
{
  Script:ActivateConda
  conda create -y -p "./devel" python=3.9 conan poetry setuptools
  conda activate "./devel"
}

function Script:PoetryClean
{
  Remove-Item -Path ".venv" -Force -ErrorAction Ignore -Recurse
}

# Initialize the development environment installing:
# - conan: to get the c++ libraries and dependencies
# - python embeddable: to let the interpreter being included in CodePP
# - poetry: to build the PyCode distribution package
function Script:Init
{
  DevelClean
  $conda = (Get-Command conda -ErrorAction SilentlyContinue)  
  if ($null -eq $conda)
  {
    Write-Error "conda is not installed or available in PATH. install it first."
    return
  } else
  {
    DevelConda

    conan profile detect --force
    conan install . --output-folder=build --build=missing -s compiler.cppstd=20 -s build_type=Debug

    DownloadPython "3.9.0" "amd64" 
  }
}

################################################################################
#                                   TASKS
################################################################################
# 
# to build the project it's necessary the anaconda package manager. it is used
# to download the python interpreter and libraries and to download conan, a C++
# package manager used to get the C++ libraries


function Script:BuildPyCode
{
  poetry build
  build/python -m pip uninstall --yes pycode
  build/python -m pip install -q ./dist/pycode-0.1.0-py3-none-any.whl
}

function Script:BuildCodePP
{
  Script:check_n_pop_directory("build")
  conan profile detect --force
  conan install . --output-folder=build --build=missing -s compiler.cppstd=20 -s build_type=Debug
  cmake -G"Ninja" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON $arg_list ..
  cmake --build .
  Pop-Location
}

function Script:Build
{
  ActivateConda
  conda activate "./devel"

  $arguments = $args[0] -split " "

  foreach ($arg in $arguments)
  {
    if ($arg -match "-*$")
    {
      if ($arg -eq "-All")
      {
        BuildPyCode
        BuildCodePP
        return
      }

      if ($arg -eq "-Pycode")
      {
        BuildPyCode
      }

      if ($arg -eq "-CodePP")
      {
        BuildCodePP
      }
    }
  }
}

function Script:Run
{
  check_n_pop_directory("build")
  $command = './' + $project
  Invoke-Expression $command
  Pop-Location
}

function Script:Tui
{
  _Venv
  Start-Process powershell -ArgumentList  '-command "python ./tools/tui.py"'
  deactivate
}

function Script:Gui
{
  _Venv
  python ./tools/main.py
  deactivate
}

try
{
  switch($args[0])
  {

    "help"
    {
      Help
    }

    "init"
    {
      Init
    }

    "build"
    {
      Build $args[1..($args.Length)]
    }

    "qt"
    {
      InstallQt "4.6.1" "windows"
    }

    "clean"
    {
      Remove-Item -Force -Recurse -Path "./build"
    }

    "tui"
    {
      PythonCommand "tools/tui.py"
    }

    "gui"
    {
      PythonCommand "tools/main.py"
    }

    default
    {
      Heading
      Help
    }
  }
} catch
{
  Pop-Location
  Write-Output $_
}
