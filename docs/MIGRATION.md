# Migración a Supabase - FlexLog

## Resumen

Se migró de un backend FastAPI en Render a Supabase para autenticación y base de datos.

## Cambios Principales

### Arquitectura Anterior
```
[App Ionic] → [Backend FastAPI] → [PostgreSQL en Render]
```

### Nueva Arquitectura
```
[App Ionic] → [Supabase] (Auth + Database + Realtime)
```

## Archivos Creados/Modificados

### Archivos Nuevos
- `supabase/esquema.sql` - DDL completo con tablas, RLS y triggers en español
- `frontend/src/app/services/supabase.service.ts` - Cliente Supabase en español

### Archivos Eliminados
- `frontend/src/app/services/api.service.ts` - Reemplazado por supabase.service.ts
- `frontend/src/app/services/sync.service.ts` - Ya no necesario
- `frontend/src/app/pages/auth-success/` - Ya no necesario
- `frontend/src/app/pages/auth-error/` - Ya no necesario
- `frontend/src/app/models/models.ts` - Tipos ahora en supabase.service.ts

### Archivos Modificados (en español)
- `frontend/package.json` - Añadido @supabase/supabase-js
- `frontend/src/app/pages/login/login.page.ts`
- `frontend/src/app/pages/gym-selector/gym-selector.page.ts`
- `frontend/src/app/pages/workout-day/workout-day.page.ts`
- `frontend/src/app/pages/active-workout/active-workout.page.ts`
- `frontend/src/app/pages/history/history.page.ts`
- `frontend/src/app/app.routes.ts` - Nueva ruta /auth/callback
- `frontend/src/environments/environment.ts`

## Pasos de Configuración

### 1. Crear Proyecto en Supabase

1. Ir a https://supabase.com
2. Crear nuevo proyecto
3. Esperar a que termine el provisioning

### 2. Ejecutar Esquema SQL

1. En Supabase Dashboard → SQL Editor
2. Copiar y pegar el contenido de `supabase/esquema.sql`
3. Ejecutar

### 3. Configurar Google OAuth

1. Ir a Authentication → Providers → Google
2. Habilitar Google OAuth
3. Ingresar Client ID y Client Secret de Google Cloud Console
4. En "Authorized redirect URI" agregar:
   - Desarrollo: `http://localhost:4200/auth/callback`
   - Producción: `https://tu-dominio.com/auth/callback`

### 4. Obtener Credenciales

En Supabase → Settings → API:
- Project URL: `https://xyzxyz.supabase.co`
- anon/public key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### 5. Actualizar Frontend

En `frontend/src/environments/environment.ts`:
```typescript
export const environment = {
  production: false,
  supabaseUrl: 'https://xyzxyz.supabase.co',
  supabaseAnonKey: 'tu-anon-key-aqui'
};
```

### 6. Instalar Dependencias

```bash
cd frontend
npm install
npm start
```

## Base de Datos

### Tablas Creadas (en español)

| Tabla | Descripción |
|-------|-------------|
| perfiles | Perfiles de usuario (extiende auth.users) |
| gimnasios | Gimnasios |
| ejercicios | Biblioteca de ejercicios |
| equipos_gimnasio | Máquinas/equipo en cada gimnasio |
| sesiones_entrenamiento | Sesiones de entrenamiento |
| series_ejercicios | Series individuales |

### Seguridad (RLS)

Todas las tablas tienen Row Level Security habilitado:
- Usuarios solo ven/manipulan sus propios datos
- Perfil solo accesible por el propio usuario
- Sesiones y series filtradas por usuario_id

### Triggers Automáticos

- `crear_perfil_automatico`: Crea perfil automáticamente al registrarse
- `actualizar_timestamp`: Actualiza timestamp en cambios

## Autenticación

El flujo ahora es:
1. Usuario clickea "Iniciar sesión con Google"
2. Redirect a Google OAuth
3. Google redirige a `/auth/callback`
4. Supabase maneja el token
5. Página callback procesa y guarda sesión

## Deploy

### Frontend (Netlify/Vercel)
```bash
cd frontend
npm run build
# Subir carpeta www/ a Netlify/Vercel
```

### Variables de Entorno de Producción
Configurar en Netlify/Vercel:
- `supabaseUrl`: URL del proyecto Supabase
- `supabaseAnonKey`: anon key pública

## Comandos Útiles

```bash
# Verificar que todo compila
cd frontend
npm install
npm run build

# Ver logs de Supabase
# Supabase Dashboard → Logs
```
