$project = Split-Path -Path (Get-Location) -Leaf

################################################################################
#                                  UTITITIES
################################################################################

function check_n_pop_directory([String]$name)
{
  New-Item -Type Directory -Path $name -ErrorAction Ignore
  Push-Location $name
}

function install_conda()
{
}

function activate_conda()
{
  if ( $IsWindows )
  {
    conda shell.powershell hook | Out-String |Invoke-Expression
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

################################################################################
#                                  BUILD
################################################################################
# 
# to build the project it's necessary the anaconda package manager. it is used
# to download the python interpreter and libraries and to download conan, a C++
# package manager used to get the C++ libraries

function install_system()
{
  $conda = (Get-Command conda -ErrorAction SilentlyContinue)  
  if ($null -eq $conda)
  {
    Write-Error "conda is not installed or available in PATH. install it first."
    return
  } else
  {
    activate_conda
    conda create -n conan conan
    conan activate conan
    conan profile detect --force
    conan install . --output-folder=build --build=missing
    conda deactivate
  }
}


function build([string[]] $arg_list)
{
  check_n_pop_directory("build")
  cmake -G"Ninja" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON $arg_list ..
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

function download_python([string]$python_version, [string]$os_version)
{
  $python_url=  "https://www.python.org/ftp/python/$python_version/python-$python_version-embed-$os_version.zip"
  Invoke-WebRequest -Uri $python_url -OutFile python.zip
  Expand-Archive -path python.zip -DestinationPath build
}

function build_python()
{
  check_n_pop_directory("build")
  check_n_pop_directory("python")
  # download python source code from git
  git clone https://github.com/python/cpython
  Pop-Location
  Pop-Location
}

switch ($args[0])
{
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
