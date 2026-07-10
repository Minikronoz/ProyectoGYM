import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date
from decimal import Decimal

from app.database import SessionLocal
from app.models.user import User
from app.models.gym import Gym
from app.models.exercise import Exercise
from app.models.gym_equipment import GymEquipment, UnitType
from app.models.workout_session import WorkoutSession
from app.models.exercise_set import ExerciseSet, SetType


def seed_data():
    db = SessionLocal()

    if db.query(User).count() > 0:
        print("Database already has data. Skipping seed.")
        db.close()
        return

    print("Seeding database with user's training data...")

    user = User(email="user@flexlog.app", name="FlexLog User")
    db.add(user)
    db.flush()

    gyms_data = [
        {"name": "Smart Fit", "branch": "Prat", "address": "Prat, Chile"},
        {"name": "Smart Fit", "branch": "Santiago Centro", "address": "Santiago, Chile"},
        {"name": "Elysium", "branch": "Principal", "address": "Chile"}
    ]
    gyms = {}
    for g_data in gyms_data:
        gym = Gym(**g_data)
        db.add(gym)
        db.flush()
        gyms[g_data["name"] + " " + (g_data["branch"] or "")] = gym

    exercises_data = [
        {"technical_name": "Pectoral Fly Machine", "target_muscle_group": "Pecho", "description": "Máquina de apertura de pecho"},
        {"technical_name": "Press de Pecho Sentado Convergente", "target_muscle_group": "Pecho", "description": "Press de pecho en máquina convergente"},
        {"technical_name": "Press Inclinado con Mancuernas", "target_muscle_group": "Pecho", "description": "Press inclinado con dumbbells"},
        {"technical_name": "Remo Sentado en Máquina", "target_muscle_group": "Espalda", "description": "Máquina de tirar para adelante"},
        {"technical_name": "Press de Hombros Sentado con Mancuernas", "target_muscle_group": "Hombros", "description": "Press militar con dumbbells a 90 grados"},
        {"technical_name": "Elevaciones Laterales con Mancuernas", "target_muscle_group": "Hombros", "description": "Lateral raises sentada inclinado"},
        {"technical_name": "Press de Banca con Barra", "target_muscle_group": "Pecho", "description": "Bench press con barra"},
        {"technical_name": "Fondos en Banco (Flexiones Asistidas)", "target_muscle_group": "Pecho", "description": "Flexiones en colchoneta"},
        {"technical_name": "Tríceps Polea Alta en V", "target_muscle_group": "Tríceps", "description": "Tríceps pushdown con agarre V"},
        {"technical_name": "Extensión de Tríceps sobre la Cabeza", "target_muscle_group": "Tríceps", "description": "Katana o french press"},
        {"technical_name": "Elevaciones Frontales", "target_muscle_group": "Hombros", "description": "Front raises con polea"},
    ]
    exercises = {}
    for e_data in exercises_data:
        exercise = Exercise(**e_data)
        db.add(exercise)
        db.flush()
        exercises[e_data["technical_name"]] = exercise

    smartfit_prat = gyms["Smart Fit Prat"]

    equipment_data = [
        {
            "gym": smartfit_prat,
            "exercise": exercises["Pectoral Fly Machine"],
            "custom_alias": "Máquina fly (Smart Fit Prat)",
            "unit_type": UnitType.KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Press de Pecho Sentado Convergente"],
            "custom_alias": "Máquina naranja primer piso (asiento 5-6)",
            "unit_type": UnitType.PER_SIDE_KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Press de Banca con Barra"],
            "custom_alias": "Banco plano barra",
            "unit_type": UnitType.PER_SIDE_KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Remo Sentado en Máquina"],
            "custom_alias": "Máquina de tirar para adelante (poleas)",
            "unit_type": UnitType.PER_SIDE_KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Press de Hombros Sentado con Mancuernas"],
            "custom_alias": "Máquina de hombro levantar",
            "unit_type": UnitType.PER_SIDE_KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Elevaciones Laterales con Mancuernas"],
            "custom_alias": "Mancuernas elevaciones laterales",
            "unit_type": UnitType.KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Tríceps Polea Alta en V"],
            "custom_alias": "Tríceps polea agarre V",
            "unit_type": UnitType.KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Extensión de Tríceps sobre la Cabeza"],
            "custom_alias": "Ejercicio katana",
            "unit_type": UnitType.KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Press Inclinado con Mancuernas"],
            "custom_alias": "Banco inclinado 90° mancuernas",
            "unit_type": UnitType.KG,
            "plate_weight_equivalent": None
        },
        {
            "gym": smartfit_prat,
            "exercise": exercises["Fondos en Banco (Flexiones Asistidas)"],
            "custom_alias": "Flexiones colchoneta",
            "unit_type": UnitType.BODYWEIGHT,
            "plate_weight_equivalent": None
        }
    ]

    equipment_map = {}
    for eq_data in equipment_data:
        eq = GymEquipment(**eq_data, created_by_user_id=user.id)
        db.add(eq)
        db.flush()
        key = eq_data["custom_alias"]
        equipment_map[key] = eq

    def create_set(session, equipment, set_num, set_type_str, weight, reps, is_failure=False, notes=None):
        set_type = SetType.WARMUP if "calentamiento" in (notes or "").lower() or "pre" in (notes or "").lower() else SetType.NORMAL
        if "kmiedo" in (notes or "").lower():
            set_type = SetType.NORMAL
        if is_failure:
            set_type = SetType.FAILURE

        return ExerciseSet(
            workout_session_id=session.id,
            gym_equipment_id=equipment.id,
            set_number=set_num,
            set_type=set_type,
            weight_value=Decimal(str(weight)),
            reps_count=reps,
            is_to_failure=is_failure,
            set_notes=notes
        )

    sessions_data = [
        {
            "date": date(2024, 5, 22),
            "gym": smartfit_prat,
            "notes": "Pecho - Día de pecho",
            "sets": [
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 1, "weight": 15, "reps": 12, "notes": "pre calentamiento"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 2, "weight": 20, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 3, "weight": 20, "reps": 8, "notes": "segunda"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 4, "weight": 25, "reps": 8, "notes": "tercera"},

                {"equipment": "Banco inclinado 90° mancuernas", "set_num": 1, "weight": 5, "reps": 12, "notes": "calentamiento"},
                {"equipment": "Banco inclinado 90° mancuernas", "set_num": 2, "weight": 7.5, "reps": 8, "notes": "primera"},
                {"equipment": "Banco inclinado 90° mancuernas", "set_num": 3, "weight": 10, "reps": 8, "notes": "segunda"},
                {"equipment": "Banco inclinado 90° mancuernas", "set_num": 4, "weight": 10, "reps": 8, "notes": "tercera"},

                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 1, "weight": 12, "reps": 12, "notes": "pre calentamiento"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 2, "weight": 30, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 3, "weight": 40, "reps": 8, "notes": "segunda"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 4, "weight": 50, "reps": 8, "notes": "tercera al fallo", "is_failure": True},

                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 1, "weight": 10, "reps": 12, "notes": "pre calentamiento"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 2, "weight": 15, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 3, "weight": 15, "reps": 8, "notes": "segunda"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 4, "weight": 15, "reps": 8, "notes": "tercera"},
            ]
        },
        {
            "date": date(2024, 5, 27),
            "gym": smartfit_prat,
            "notes": "Pecho/Hombro/Tríceps",
            "sets": [
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 1, "weight": 10, "reps": 12, "notes": "calentamiento"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 2, "weight": 25, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 3, "weight": 30, "reps": 12, "notes": "segunda x12"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 4, "weight": 30, "reps": 15, "notes": "tercera al fallo x15", "is_failure": True},

                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 1, "weight": 5, "reps": 12, "notes": "calentamiento 5kg por lado"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 2, "weight": 5, "reps": 8, "notes": "primera 5kg por lado"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 3, "weight": 7.5, "reps": 8, "notes": "segunda 7.5kg por lado"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 4, "weight": 7.5, "reps": 8, "notes": "tercera 7.5kg por lado"},

                {"equipment": "Banco plano barra", "set_num": 1, "weight": 0, "reps": 8, "notes": "primera sin peso"},
                {"equipment": "Banco plano barra", "set_num": 2, "weight": 0, "reps": 8, "notes": "segunda sin peso"},
                {"equipment": "Banco plano barra", "set_num": 3, "weight": 0, "reps": 8, "notes": "tercera sin peso"},

                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 1, "weight": 10, "reps": 10, "notes": "primera 10kg por lado"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 2, "weight": 10, "reps": 10, "notes": "segunda 10kg por lado"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 3, "weight": 10, "reps": 6, "notes": "tercera al fallo 10kg por lado", "is_failure": True},

                {"equipment": "Máquina de hombro levantar", "set_num": 1, "weight": 0, "reps": 10, "notes": "primera sin peso"},
                {"equipment": "Máquina de hombro levantar", "set_num": 2, "weight": 0, "reps": 10, "notes": "segunda sin peso"},
                {"equipment": "Máquina de hombro levantar", "set_num": 3, "weight": 0, "reps": 10, "notes": "tercera sin peso"},

                {"equipment": "Mancuernas elevaciones laterales", "set_num": 1, "weight": 5, "reps": 10, "notes": "primera"},
                {"equipment": "Mancuernas elevaciones laterales", "set_num": 2, "weight": 5, "reps": 10, "notes": "segunda"},
                {"equipment": "Mancuernas elevaciones laterales", "set_num": 3, "weight": 5, "reps": 10, "notes": "tercera"},

                {"equipment": "Tríceps polea agarre V", "set_num": 1, "weight": 15, "reps": 12, "notes": "primera"},
                {"equipment": "Tríceps polea agarre V", "set_num": 2, "weight": 20, "reps": 12, "notes": "segunda"},
                {"equipment": "Tríceps polea agarre V", "set_num": 3, "weight": 20, "reps": 12, "notes": "tercera"},

                {"equipment": "Ejercicio katana", "set_num": 1, "weight": 2.5, "reps": 8, "notes": "primera"},
                {"equipment": "Ejercicio katana", "set_num": 2, "weight": 2.5, "reps": 8, "notes": "segunda"},
                {"equipment": "Ejercicio katana", "set_num": 3, "weight": 2.5, "reps": 8, "notes": "tercera"},
            ]
        },
        {
            "date": date(2024, 6, 3),
            "gym": smartfit_prat,
            "notes": "Pecho",
            "sets": [
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 1, "weight": 19, "reps": 12, "notes": "calentamiento"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 2, "weight": 24, "reps": 12, "notes": "primera"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 3, "weight": 29, "reps": 14, "notes": "segunda"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 4, "weight": 29, "reps": 15, "notes": "tercera hasta el fallo", "is_failure": True},

                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 1, "weight": 5, "reps": 12, "notes": "calentamiento 5kg por lado"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 2, "weight": 10, "reps": 8, "notes": "primera 10kg por lado"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 3, "weight": 10, "reps": 8, "notes": "segunda 10kg por lado"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 4, "weight": 10, "reps": 8, "notes": "tercera 10kg por lado"},

                {"equipment": "Banco plano barra", "set_num": 1, "weight": 0, "reps": 8, "notes": "calentamiento sin peso"},
                {"equipment": "Banco plano barra", "set_num": 2, "weight": 5, "reps": 8, "notes": "primera 5kg por lado kmiedo"},
                {"equipment": "Banco plano barra", "set_num": 3, "weight": 7.5, "reps": 8, "notes": "segunda 7.5kg por lado"},
                {"equipment": "Banco plano barra", "set_num": 4, "weight": 7.5, "reps": 10, "notes": "tercera 7.5kg por lado x10"},

                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 1, "weight": 10, "reps": 12, "notes": "primera 10kg por lado"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 2, "weight": 15, "reps": 8, "notes": "segunda 15kg por lado"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 3, "weight": 15, "reps": 8, "notes": "tercera 15kg por lado"},

                {"equipment": "Máquina de hombro levantar", "set_num": 1, "weight": 5, "reps": 8, "notes": "primera 5kg por lado"},
                {"equipment": "Máquina de hombro levantar", "set_num": 2, "weight": 7.5, "reps": 9, "notes": "segunda 7.5kg por lado"},
                {"equipment": "Máquina de hombro levantar", "set_num": 3, "weight": 7.5, "reps": 8, "notes": "tercera 7.5kg por lado"},

                {"equipment": "Mancuernas elevaciones laterales", "set_num": 1, "weight": 7.5, "reps": 8, "notes": "primera"},
                {"equipment": "Mancuernas elevaciones laterales", "set_num": 2, "weight": 7.5, "reps": 8, "notes": "segunda"},
                {"equipment": "Mancuernas elevaciones laterales", "set_num": 3, "weight": 7.5, "reps": 8, "notes": "tercera"},

                {"equipment": "Tríceps polea agarre V", "set_num": 1, "weight": 15, "reps": 12, "notes": "primera"},
                {"equipment": "Tríceps polea agarre V", "set_num": 2, "weight": 20, "reps": 12, "notes": "segunda"},
                {"equipment": "Tríceps polea agarre V", "set_num": 3, "weight": 25, "reps": 12, "notes": "tercera"},

                {"equipment": "Ejercicio katana", "set_num": 1, "weight": 2.5, "reps": 8, "notes": "primera"},
                {"equipment": "Ejercicio katana", "set_num": 2, "weight": 5, "reps": 8, "notes": "segunda"},
                {"equipment": "Ejercicio katana", "set_num": 3, "weight": 5, "reps": 8, "notes": "tercera"},

                {"equipment": "Flexiones colchoneta", "set_num": 1, "weight": 0, "reps": 7, "notes": "primera 4 sin apoyo y 3 cn apoyo rodillas"},
                {"equipment": "Flexiones colchoneta", "set_num": 2, "weight": 0, "reps": 5, "notes": "segunda 5 cn apoyo rodillas"},
            ]
        },
        {
            "date": date(2024, 6, 10),
            "gym": smartfit_prat,
            "notes": "Pecho",
            "sets": [
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 1, "weight": 20, "reps": 12, "notes": "calentamiento"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 2, "weight": 30, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 3, "weight": 30, "reps": 9, "notes": "segunda"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 4, "weight": 35, "reps": 12, "notes": "tercera hasta el fallo x12", "is_failure": True},

                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 1, "weight": 5, "reps": 12, "notes": "calentamiento"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 2, "weight": 10, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 3, "weight": 10, "reps": 8, "notes": "segunda"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 4, "weight": 10, "reps": 8, "notes": "tercera"},

                {"equipment": "Banco plano barra", "set_num": 1, "weight": 5, "reps": 8, "notes": "calentamiento 5kg por lado"},
                {"equipment": "Banco plano barra", "set_num": 2, "weight": 7.5, "reps": 9, "notes": "primera 7.5kg por lado"},
                {"equipment": "Banco plano barra", "set_num": 3, "weight": 7.5, "reps": 8, "notes": "segunda 7.5kg por lado"},
                {"equipment": "Banco plano barra", "set_num": 4, "weight": 10, "reps": 8, "notes": "tercera 10kg por lado"},

                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 1, "weight": 10, "reps": 12, "notes": "primera"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 2, "weight": 15, "reps": 8, "notes": "segunda"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 3, "weight": 15, "reps": 7, "notes": "tercera hasta el fallo", "is_failure": True},

                {"equipment": "Mancuernas elevaciones laterales", "set_num": 1, "weight": 5, "reps": 12, "notes": "primera"},
                {"equipment": "Mancuernas elevaciones laterales", "set_num": 2, "weight": 5, "reps": 12, "notes": "segunda"},
                {"equipment": "Mancuernas elevaciones laterales", "set_num": 3, "weight": 5, "reps": 12, "notes": "tercera"},

                {"equipment": "Máquina de hombro levantar", "set_num": 1, "weight": 5, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina de hombro levantar", "set_num": 2, "weight": 10, "reps": 7, "notes": "segunda"},
                {"equipment": "Máquina de hombro levantar", "set_num": 3, "weight": 10, "reps": 7, "notes": "tercera"},

                {"equipment": "Tríceps polea agarre V", "set_num": 1, "weight": 15, "reps": 8, "notes": "primera (luego 6 con 12kg)"},
                {"equipment": "Tríceps polea agarre V", "set_num": 2, "weight": 15, "reps": 7, "notes": "segunda (luego 3 con 12kg)"},
                {"equipment": "Tríceps polea agarre V", "set_num": 3, "weight": 15, "reps": 4, "notes": "tercera (luego 2 con 12kg)"},


                {"equipment": "Flexiones colchoneta", "set_num": 1, "weight": 0, "reps": 5, "notes": "primera sin apoyo 4 y con apoyo 1"},
                {"equipment": "Flexiones colchoneta", "set_num": 2, "weight": 0, "reps": 1, "notes": "segunda sin apoyo y con apoyo 1"},
            ]
        },
        {
            "date": date(2024, 6, 23),
            "gym": smartfit_prat,
            "notes": "Pecho - Smart Fit Prat",
            "sets": [
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 1, "weight": 19, "reps": 8, "notes": "calentamiento"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 2, "weight": 29, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 3, "weight": 34, "reps": 13, "notes": "segunda"},
                {"equipment": "Máquina fly (Smart Fit Prat)", "set_num": 4, "weight": 34, "reps": 15, "notes": "tercera hasta el fallo", "is_failure": True},

                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 1, "weight": 5, "reps": 12, "notes": "calentamiento"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 2, "weight": 10, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 3, "weight": 10, "reps": 8, "notes": "segunda"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 4, "weight": 10, "reps": 8, "notes": "tercera"},

                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 1, "weight": 5, "reps": 8, "notes": "calentamiento 5kg por lado press banca"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 2, "weight": 10, "reps": 8, "notes": "primera 10kg x8"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 3, "weight": 10, "reps": 8, "notes": "segunda 10kg x8"},
                {"equipment": "Máquina naranja primer piso (asiento 5-6)", "set_num": 4, "weight": 10, "reps": 8, "notes": "tercera 10kg x8 hasta el fallo", "is_failure": True},

                {"equipment": "Máquina de hombro levantar", "set_num": 1, "weight": 10, "reps": 8, "notes": "primera (bajar lento subir controlado)"},
                {"equipment": "Máquina de hombro levantar", "set_num": 2, "weight": 10, "reps": 9, "notes": "segunda"},
                {"equipment": "Máquina de hombro levantar", "set_num": 3, "weight": 10, "reps": 8, "notes": "tercera hasta el fallo", "is_failure": True},

                {"equipment": "Tríceps polea agarre V", "set_num": 1, "weight": 15, "reps": 12, "notes": "primera"},
                {"equipment": "Tríceps polea agarre V", "set_num": 2, "weight": 25, "reps": 12, "notes": "segunda"},
                {"equipment": "Tríceps polea agarre V", "set_num": 3, "weight": 25, "reps": 12, "notes": "tercera"},
                {"equipment": "Tríceps polea agarre V", "set_num": 4, "weight": 25, "reps": 11, "notes": "cuarta hasta el fallo", "is_failure": True},

                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 1, "weight": 15, "reps": 8, "notes": "primera"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 2, "weight": 15, "reps": 7, "notes": "segunda"},
                {"equipment": "Máquina de tirar para adelante (poleas)", "set_num": 3, "weight": 15, "reps": 7, "notes": "tercera"},

                {"equipment": "Flexiones colchoneta", "set_num": 1, "weight": 0, "reps": 3, "notes": "primera 2 sin apoyo 1 con apoyo"},
                {"equipment": "Flexiones colchoneta", "set_num": 2, "weight": 0, "reps": 3, "notes": "segunda 3 sin apoyo"},
                {"equipment": "Flexiones colchoneta", "set_num": 3, "weight": 0, "reps": 5, "notes": "tercera 4 sin apoyo 1 con apoyo"},
            ]
        }
    ]

    for session_data in sessions_data:
        session = WorkoutSession(
            user_id=user.id,
            gym_id=session_data["gym"].id,
            date=session_data["date"],
            general_notes=session_data["notes"],
            is_synced=True
        )
        db.add(session)
        db.flush()

        for set_info in session_data["sets"]:
            equipment = equipment_map.get(set_info["equipment"])
            if equipment:
                s = create_set(
                    session=session,
                    equipment=equipment,
                    set_num=set_info["set_num"],
                    set_type_str="normal",
                    weight=set_info["weight"],
                    reps=set_info["reps"],
                    is_failure=set_info.get("is_failure", False),
                    notes=set_info.get("notes")
                )
                db.add(s)

    db.commit()
    print("Seed data created successfully!")
    print(f"  - User: {user.email}")
    print(f"  - Gyms: {len(gyms)}")
    print(f"  - Exercises: {len(exercises)}")
    print(f"  - Equipment mappings: {len(equipment_map)}")
    print(f"  - Training sessions: {len(sessions_data)}")
    db.close()


if __name__ == "__main__":
    seed_data()
