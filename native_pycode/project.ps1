$project = Split-Path -Path (Get-Location) -Leaf

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

function install_build_system()
{
  $conda = (Get-Command conda -ErrorAction SilentlyContinue)  
  if ($null -eq $conda)
  {
    Write-Error "conda is not installed or available in PATH. install it first."
    return
  } else
  {
    activate_conda
    conda create -n devel conda
    conda activate devel
    conan profile detect --force
    conan install . --output-folder=build --build=missing -s compiler.cppstd=20 -s build_type=Debug
    download_python "3.10.0" "amd64" 
    conda deactivate
  }
}


function build([string[]] $arg_list)
{
  check_n_pop_directory("build")
  cmake -G"Ninja" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_TOOLCHAIN_FILE="conan_toolchain.cmake" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON $arg_list ..
  cmake --build .
  Pop-Location
}

function run
{
  check_n_pop_directory("build")
  $command = './' + $project
  Invoke-Expression $command
  Pop-Location
}

switch ($args[0])
{
  "install"
  {
    install_build_system
  }

  "conda"
  {
    activate_conda
  }

  "build"
  {
    build($args[1..($args.Length)])
  }

  "run"
  {
    build($args[1..($args.Length)])
    run
  }

  "clean"
  {
    Remove-Item -Force -Recurse -Path "./build"
  }

  "python"
  {
    download_python "3.10.0" "amd64" 
  }

  default
  {
    run
  }
}
