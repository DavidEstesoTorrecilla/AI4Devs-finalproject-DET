#!/bin/bash

# Script para setup local del proyecto EMASAI
# Ejecutar con: bash infrastructure/scripts/setup-local.sh

echo "🚀 Iniciando setup de EMASAI..."

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado. Instala Node.js 18+ primero."
    exit 1
fi

echo "✅ Node.js instalado: $(node --version)"

# Verificar pnpm
if ! command -v pnpm &> /dev/null; then
    echo "📦 Instalando pnpm..."
    npm install -g pnpm
fi

echo "✅ pnpm instalado: $(pnpm --version)"

# Instalar dependencias
echo "📦 Instalando dependencias..."
pnpm install

# Copiar archivos .env
echo "📝 Copiando archivos de configuración..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Archivo .env creado en raíz"
fi

if [ ! -f "apps/backend/.env" ]; then
    cp apps/backend/.env.example apps/backend/.env
    echo "✅ Archivo .env creado en backend"
fi

if [ ! -f "apps/frontend/.env" ]; then
    cp apps/frontend/.env.example apps/frontend/.env
    echo "✅ Archivo .env creado en frontend"
fi

# Docker setup
echo "🐳 Iniciando servicios Docker (PostgreSQL y Redis)..."
docker-compose up -d postgres redis

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté listo..."
sleep 5

# Generar cliente Prisma
echo "🔧 Generando cliente Prisma..."
pnpm --filter backend prisma:generate

# Ejecutar migraciones
echo "🗄️ Ejecutando migraciones de base de datos..."
pnpm --filter backend prisma:migrate

# Seed data (opcional)
echo "🌱 ¿Deseas cargar datos de prueba? (s/n)"
read -r response
if [[ "$response" =~ ^[Ss]$ ]]; then
    pnpm --filter backend prisma:seed
    echo "✅ Datos de prueba cargados"
fi

echo ""
echo "✅ Setup completado!"
echo ""
echo "📚 Próximos pasos:"
echo "  1. Revisa los archivos .env y configura tus credenciales"
echo "  2. Ejecuta: pnpm dev (para iniciar backend y frontend)"
echo "  3. Backend: http://localhost:3001"
echo "  4. Frontend: http://localhost:5173"
echo "  5. API Docs: http://localhost:3001/api/docs"
echo "  6. Prisma Studio: pnpm prisma:studio"
echo ""
