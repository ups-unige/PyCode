$project = Split-Path -Path (Get-Location) -Leaf

function build([string[]] $arg_list) {
  New-Item -Type Directory -Path build -ErrorAction Ignore
    Push-Location build
    cmake -G"Ninja" -DCMAKE_EXPORT_COMPILE_COMMANDS=ON $arg_list ..
    cmake --build .
  Pop-Location
}

function run {
  Push-Location build
    $command = './' + $project
    Invoke-Expression $command
  Pop-Location
}

switch ($args[0]) {
  "build" {
    build($args[1..($args.Length)])
  }

  "run" {
    build($args[1..($args.Length)])
      run
  }

  "clean" {
    Remove-Item -Force -Recurse -Path "./build"
  }

  default {
    run
  }
}
