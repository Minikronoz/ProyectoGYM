# FlexLog - Modelo de Datos

## Diagrama Entidad-Relación

```
┌─────────────┐       ┌──────────────────┐       ┌─────────────────┐
│    users    │       │      gyms        │       │   exercises    │
├─────────────┤       ├──────────────────┤       ├─────────────────┤
│ id (PK)     │       │ id (PK)          │       │ id (PK)         │
│ email       │       │ name             │       │ technical_name  │
│ name        │       │ branch           │       │ target_muscle   │
│ google_id   │       │ address          │       │ description     │
│ created_at  │       │ created_at       │       │                 │
└─────────────┘       └──────────────────┘       └─────────────────┘
        │                      │                         │
        │                      │                         │
        ▼                      ▼                         │
┌─────────────────────────────────────┐                  │
│         gym_equipment               │◄─────────────────┘
├─────────────────────────────────────┤
│ id (PK)                             │
│ gym_id (FK) ────────────────────────┘
│ exercise_id (FK)
│ custom_alias
│ unit_type (ENUM: kg, lbs, plates, bodyweight, per_side_kg)
│ plate_weight_equivalent
│ created_by_user_id (FK)
│ created_at
└─────────────────────────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────────────────────────┐
│        workout_sessions             │
├─────────────────────────────────────┤
│ id (PK)                             │
│ user_id (FK) ───────────► users      │
│ gym_id (FK) ───────────► gyms        │
│ date                                │
│ general_notes                       │
│ is_synced                           │
│ client_id                           │
│ created_at                          │
│ updated_at                          │
└─────────────────────────────────────┘
        │
        │ 1:N
        ▼
┌─────────────────────────────────────┐
│          exercise_sets              │
├─────────────────────────────────────┤
│ id (PK)                             │
│ workout_session_id (FK)             │
│ gym_equipment_id (FK)               │
│ set_number                          │
│ set_type (ENUM: warmup, normal,     │
│            failure, drop_set)       │
│ weight_value (DECIMAL)              │
│ reps_count (INT)                    │
│ is_to_failure (BOOLEAN)              │
│ set_notes                           │
│ created_at                          │
└─────────────────────────────────────┘
```

## Tablas

### users
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INT PK | ID único |
| email | VARCHAR(255) | Email único |
| name | VARCHAR(255) | Nombre |
| google_id | VARCHAR(255) | ID de Google OAuth |
| created_at | TIMESTAMP | Fecha de creación |

### gyms
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INT PK | ID único |
| name | VARCHAR(100) | Nombre del gym (ej. "Smart Fit") |
| branch | VARCHAR(100) | Sucursal (ej. "Prat") |
| address | TEXT | Dirección |
| created_at | TIMESTAMP | Fecha de creación |

### exercises
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INT PK | ID único |
| technical_name | VARCHAR(100) | Nombre técnico del ejercicio |
| target_muscle_group | VARCHAR(50) | Grupo muscular |
| description | TEXT | Descripción |

### gym_equipment
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INT PK | ID único |
| gym_id | INT FK | Gimnasio |
| exercise_id | INT FK | Ejercicio base |
| custom_alias | VARCHAR(150) | Alias local (ej. "Máquina naranja primer piso") |
| unit_type | ENUM | Tipo de unidad (kg, per_side_kg, plates, bodyweight) |
| plate_weight_equivalent | DECIMAL(5,2) | Peso por placa si aplica |
| created_by_user_id | INT FK | Usuario que lo creó |
| created_at | TIMESTAMP | Fecha de creación |

### workout_sessions
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INT PK | ID único |
| user_id | INT FK | Usuario |
| gym_id | INT FK | Gimnasio |
| date | DATE | Fecha del entrenamiento |
| general_notes | TEXT | Notas generales |
| is_synced | BOOLEAN | Si está sincronizado |
| client_id | VARCHAR(100) | ID del cliente (para sync offline) |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Última actualización |

### exercise_sets
| Columna | Tipo | Descripción |
|---------|------|-------------|
| id | INT PK | ID único |
| workout_session_id | INT FK | Sesión de entrenamiento |
| gym_equipment_id | INT FK | Equipamiento del gym |
| set_number | INT | Número de serie |
| set_type | ENUM | Tipo (warmup, normal, failure, drop_set) |
| weight_value | DECIMAL(6,2) | Peso (valor plano, la unidad depende del equipo) |
| reps_count | INT | Repeticiones |
| is_to_failure | BOOLEAN | Entrenó hasta el fallo |
| set_notes | VARCHAR(255) | Notas (ej. "kmiedo", "subir controlado") |
| created_at | TIMESTAMP | Fecha de creación |

## Unit Types (unit_type)

| Valor | Descripción | Ejemplo |
|-------|-------------|---------|
| `kg` | Kilogramos totales | 30kg en máquina de poleas |
| `per_side_kg` | Kilogramos por lado | 10kg por lado = 20kg total |
| `plates` | Número de placas | "Quinta placa" = 5 |
| `bodyweight` | Peso corporal | Flexiones |
| `lbs` | Libras | 45lbs barra |

## Set Types (set_type)

| Valor | Descripción |
|-------|-------------|
| `warmup` | Calentamiento |
| `normal` | Serie normal |
| `failure` | Serie al fallo |
| `drop_set` | Serie descendente |
