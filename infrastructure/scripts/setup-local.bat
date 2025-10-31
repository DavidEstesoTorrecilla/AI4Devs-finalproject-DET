@echo off
REM Script para setup local del proyecto EMASAI en Windows
REM Ejecutar con: infrastructure\scripts\setup-local.bat

echo Iniciando setup de EMASAI...

REM Verificar Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js no esta instalado. Instala Node.js 18+ primero.
    exit /b 1
)

echo Node.js instalado
node --version

REM Verificar pnpm
where pnpm >nul 2>nul
if %errorlevel% neq 0 (
    echo Instalando pnpm...
    npm install -g pnpm
)

echo pnpm instalado
pnpm --version

REM Instalar dependencias
echo Instalando dependencias...
pnpm install

REM Copiar archivos .env
echo Copiando archivos de configuracion...
if not exist ".env" (
    copy .env.example .env
    echo Archivo .env creado en raiz
)

if not exist "apps\backend\.env" (
    copy apps\backend\.env.example apps\backend\.env
    echo Archivo .env creado en backend
)

if not exist "apps\frontend\.env" (
    copy apps\frontend\.env.example apps\frontend\.env
    echo Archivo .env creado en frontend
)

REM Docker setup
echo Iniciando servicios Docker (PostgreSQL y Redis)...
docker-compose up -d postgres redis

REM Esperar a que PostgreSQL este listo
echo Esperando a que PostgreSQL este listo...
timeout /t 5 /nobreak >nul

REM Generar cliente Prisma
echo Generando cliente Prisma...
pnpm --filter backend prisma:generate

REM Ejecutar migraciones
echo Ejecutando migraciones de base de datos...
pnpm --filter backend prisma:migrate

echo.
echo Setup completado!
echo.
echo Proximos pasos:
echo   1. Revisa los archivos .env y configura tus credenciales
echo   2. Ejecuta: pnpm dev (para iniciar backend y frontend)
echo   3. Backend: http://localhost:3001
echo   4. Frontend: http://localhost:5173
echo   5. API Docs: http://localhost:3001/api/docs
echo   6. Prisma Studio: pnpm prisma:studio
echo.

pause
