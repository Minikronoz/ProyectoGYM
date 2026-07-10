# FlexLog - Gym Training Tracker

App de tracking de entrenamientos de gym con soporte offline-first.

## Arquitectura

```
[ Ionic Mobile App ] <── HTTPS/REST ──> [ FastAPI Backend ] <── PostgreSQL ──> [ Render ]
```

## Proyecto

```
ProyectoGYM/
├── backend/                    # FastAPI API
│   ├── app/
│   │   ├── main.py            # Entry point
│   │   ├── config.py          # Settings
│   │   ├── database.py        # PostgreSQL connection
│   │   ├── dependencies.py     # Auth dependencies
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── routers/            # API endpoints
│   │   └── auth/               # JWT + Google OAuth
│   ├── docs/                   # Documentación
│   ├── seed_data.py            # Datos de prueba
│   ├── requirements.txt
│   └── README.md
└── frontend/                   # Ionic Angular
    ├── src/app/
    │   ├── pages/              # Login, GymSelector, WorkoutDay, ActiveWorkout, History
    │   ├── services/           # ApiService, SyncService
    │   └── models/             # TypeScript interfaces
    └── README.md
```

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Frontend | Ionic 7 + Angular 17 |
| Backend | FastAPI + Python |
| DB | PostgreSQL (Render) |
| Auth | Google OAuth + JWT |
| Hosting | Render (Python Web Service) |

## Backend - Setup Local

```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con DATABASE_URL de Render
python -m uvicorn app.main:app --reload
python seed_data.py  # Opcional: cargar tus datos
```

## Backend - Deploy en Render

1. Crear PostgreSQL instance en Render
2. Crear Web Service conectando a este repo
3. Configurar environment variables:
   - `DATABASE_URL` = PostgreSQL connection string (external)
   - `SECRET_KEY` = random string
   - `DEBUG=false`
   - `GOOGLE_CLIENT_ID` = de Google Cloud Console
   - `GOOGLE_CLIENT_SECRET` = de Google Cloud Console
4. Deploy!

## Frontend - Setup Local

```bash
cd frontend
npm install
npm start
# Abrir http://localhost:8100
```

## Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /auth/google/url | Obtener URL de Google OAuth |
| GET | /auth/callback | Callback de Google |
| GET | /gyms/ | Listar gimnasios |
| POST | /gyms/ | Crear gimnasio |
| GET | /exercises/ | Listar ejercicios |
| GET | /workouts/equipment/ | Listar equipamiento |
| GET | /workouts/equipment/{id}/last-set | Último set (pre-carga) |
| GET | /workouts/sessions/ | Listar sesiones |
| POST | /workouts/sessions/ | Crear sesión |
| POST | /workouts/sets/ | Crear set |
| POST | /sync/ | Sincronizar datos offline |
| GET | /analytics/progress/ | Ver progreso |

## Modelo de Datos

Ver [backend/docs/DATABASE_SCHEMA.md](backend/docs/DATABASE_SCHEMA.md)

## Características Principales

- Login con Google OAuth
- Selector de gym multi-sucursal
- Mapeo de máquinas locales con alias personales
- Pre-carga del último set usado por máquina
- Registro rápido con botones "Normal", "Fallo"
- Funciona offline (guarda localmente)
- Sincroniza cuando hay conexión
- Cálculo de volumen y progreso
