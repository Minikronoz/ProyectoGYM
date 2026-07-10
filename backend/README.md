# FlexLog Backend

API REST para tracking de entrenamientos de gym.

## Stack

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos (Render)
- **Google OAuth** - Autenticación

## Setup Local

1. Crear ambiente virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. Crear PostgreSQL en Render:
   - Crear cuenta en [Render](https://render.com)
   - Crear PostgreSQL instance (Free tier)
   - Copiar Internal Database URL a `DATABASE_URL` en .env

5. Correr servidor:
```bash
uvicorn app.main:app --reload
```

6. Seed data (opcional):
```bash
python seed_data.py
```

## Endpoints Principales

### Auth
- `POST /auth/register` - Registro
- `POST /auth/login` - Login
- `GET /auth/google/url` - URL de Google OAuth
- `GET /auth/callback` - Callback de Google
- `GET /auth/me` - Usuario actual

### Gimnasios
- `GET /gyms/` - Listar gyms
- `POST /gyms/` - Crear gym
- `GET /gyms/{id}` - Ver gym
- `PUT /gyms/{id}` - Actualizar gym
- `DELETE /gyms/{id}` - Eliminar gym

### Ejercicios
- `GET /exercises/` - Listar ejercicios
- `POST /exercises/` - Crear ejercicio
- `GET /exercises/{id}` - Ver ejercicio
- `PUT /exercises/{id}` - Actualizar ejercicio
- `DELETE /exercises/{id}` - Eliminar ejercicio

### Workouts
- `GET /workouts/sessions/` - Listar sesiones
- `POST /workouts/sessions/` - Crear sesión
- `GET /workouts/sessions/{id}` - Ver sesión con sets
- `POST /workouts/sets/` - Crear set
- `GET /workouts/equipment/` - Listar equipamiento
- `POST /workouts/equipment/` - Crear mapping equipo
- `GET /workouts/equipment/{id}/last-set` - Último set de equipo

### Sync
- `POST /sync/` - Sincronizar sesiones offline

### Analytics
- `GET /analytics/progress/` - Progreso por ejercicio

## Deploy en Render

1. Fork/clone este repo
2. Crear Web Service en Render
3. Conectar con tu repo de GitHub
4. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Añadir environment variables desde .env
6. Deploy!

## API Docs

Cuando `DEBUG=true`, accede a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
