# FlexLog Frontend

App móvil para tracking de entrenamientos de gym.

## Stack

- **Angular 17** - Framework
- **Ionic 7** - UI components
- **TypeScript** - Lenguaje
- **Capacitor** - Mobile wrapper (futuro)

## Setup Local

1. Instalar dependencias:
```bash
cd frontend
npm install
```

2. Correr en desarrollo:
```bash
npm start
# o
ionic serve
```

3. Abrir en navegador:
```
http://localhost:8100
```

## Estructura

```
frontend/
├── src/
│   ├── app/
│   │   ├── pages/
│   │   │   ├── login/          # Login con Google
│   │   │   ├── gym-selector/   # Selector de gym
│   │   │   ├── workout-day/    # Día de entrenamiento
│   │   │   ├── active-workout/ # Workout activo
│   │   │   └── history/        # Historial
│   │   ├── services/
│   │   │   ├── api.service.ts  # Cliente HTTP
│   │   │   └── sync.service.ts # Sincronización offline
│   │   └── models/
│   │       └── models.ts       # Interfaces TypeScript
│   ├── index.html
│   └── main.ts
├── package.json
└── tsconfig.json
```

## Flujo de Usuario

1. **Login** → Autenticación con Google OAuth
2. **Gym Selector** → Seleccionar gym (Smart Fit Prat, etc)
3. **Workout Day** → Elegir máquinas para el día
4. **Active Workout** → Registrar series con pre-carga inteligente
5. **Sync** → Guardar localmente y sincronizar cuando hay conexión

## API Backend

El frontend se conecta a `http://localhost:8000` (backend FastAPI).

Para producción, cambiar `apiUrl` en `src/app/services/api.service.ts`.

## Características Principales

- Login con Google OAuth
- Selector de gym multi-sucursal
- Pre-carga del último set usado por máquina
- Registro rápido con botones "Calentamiento", "Normal", "Fallo"
- Funciona offline (guarda localmente)
- Sincroniza cuando hay conexión
