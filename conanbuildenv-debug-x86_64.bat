@echo off
chcp 65001 > nul
setlocal
echo @echo off > "%~dp0/deactivate_conanbuildenv-debug-x86_64.bat"
echo echo Restoring environment >> "%~dp0/deactivate_conanbuildenv-debug-x86_64.bat"
for %%v in (PATH) do (
    set foundenvvar=
    for /f "delims== tokens=1,2" %%a in ('set') do (
        if /I "%%a" == "%%v" (
            echo set "%%a=%%b">> "%~dp0/deactivate_conanbuildenv-debug-x86_64.bat"
            set foundenvvar=1
        )
    )
    if not defined foundenvvar (
        echo set %%v=>> "%~dp0/deactivate_conanbuildenv-debug-x86_64.bat"
    )
)
endlocal


set "PATH=C:\Users\leonardo\.conan2\p\ninjae2ad385cd85df\p\bin;C:\Users\leonardo\.conan2\p\cmake98309fcbb52ab\p\bin;%PATH%"