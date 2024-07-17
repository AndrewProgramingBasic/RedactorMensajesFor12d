@echo off

REM UpToGit 0.1 (Windows)
REM Actualiza fácilmente tu repositorio Git
REM (CC) 2011 Alfonso Saavedra "Son Link"
REM http://sonlinkblog.blogspot.com
REM Bajo licencia GNU/GPL

REM Comprobamos si el directorio actual es un repositorio Git
if not exist ".git" (
    echo Esta carpeta no contiene un repositorio Git
    goto :eof
)

REM Comprobamos si se pasaron parámetros
if "%~1"=="" (
    echo UpToGit: ¡Error! No se le ha pasado ningún parámetro
    echo uptogit fichero1 fichero2 ... ficheroN
    goto :eof
)

REM Recorremos los parámetros para comprobar si existen
for %%f in (%*) do (
    if not exist "%%f" (
        echo UpToGit: El archivo o directorio %%f no existe
        goto :eof
    )
)

REM Indicamos a Git los archivos a subir (usando "" para rutas con espacios)
git add %*

REM Pedimos el mensaje del commit
set /p TXT=Introduce el mensaje del commit:
git commit -m "%TXT%"

REM Subimos los archivos
git push
