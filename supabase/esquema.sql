-- FlexLog - Esquema de Base de Datos para Supabase
-- Ejecuta esto en el SQL Editor de Supabase

-- Habilitar extensión UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- TABLAS
-- ============================================

-- Tabla de perfiles de usuario (extiende auth.users de Supabase)
CREATE TABLE public.perfiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    nombre_completo TEXT,
    google_id TEXT,
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de gimnasios
CREATE TABLE public.gimnasios (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    sucursal TEXT,
    direccion TEXT,
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de ejercicios (biblioteca global)
CREATE TABLE public.ejercicios (
    id SERIAL PRIMARY KEY,
    nombre_tecnico TEXT NOT NULL,
    grupo_muscular TEXT NOT NULL,
    descripcion TEXT,
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de equipos/maquinarias en cada gimnasio
CREATE TABLE public.equipos_gimnasio (
    id SERIAL PRIMARY KEY,
    gimnasio_id INTEGER NOT NULL REFERENCES public.gimnasios(id) ON DELETE CASCADE,
    ejercicio_id INTEGER NOT NULL REFERENCES public.ejercicios(id) ON DELETE CASCADE,
    alias_personalizado TEXT NOT NULL,
    tipo_unidad TEXT NOT NULL DEFAULT 'kg',
    peso_equivalente_placa NUMERIC(5,2),
    creado_por_usuario_id UUID REFERENCES public.perfiles(id) ON DELETE SET NULL,
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de sesiones de entrenamiento
CREATE TABLE public.sesiones_entrenamiento (
    id SERIAL PRIMARY KEY,
    usuario_id UUID NOT NULL REFERENCES public.perfiles(id) ON DELETE CASCADE,
    gimnasio_id INTEGER NOT NULL REFERENCES public.gimnasios(id) ON DELETE CASCADE,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    notas_generales TEXT,
    id_cliente UUID DEFAULT uuid_generate_v4(),
    creado_en TIMESTAMPTZ DEFAULT NOW(),
    actualizado_en TIMESTAMPTZ DEFAULT NOW()
);

-- Tabla de series de ejercicios
CREATE TABLE public.series_ejercicios (
    id SERIAL PRIMARY KEY,
    sesion_entrenamiento_id INTEGER NOT NULL REFERENCES public.sesiones_entrenamiento(id) ON DELETE CASCADE,
    equipo_gimnasio_id INTEGER NOT NULL REFERENCES public.equipos_gimnasio(id) ON DELETE CASCADE,
    numero_serie INTEGER NOT NULL,
    tipo_serie TEXT NOT NULL DEFAULT 'normal',
    valor_peso NUMERIC(7,2) NOT NULL,
    cantidad_reps INTEGER NOT NULL,
    hasta_falla BOOLEAN DEFAULT FALSE,
    notas_serie TEXT,
    id_cliente UUID DEFAULT uuid_generate_v4(),
    creado_en TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- ÍNDICES
-- ============================================

CREATE INDEX idx_equipos_gimnasio_gimnasio_id ON public.equipos_gimnasio(gimnasio_id);
CREATE INDEX idx_equipos_gimnasio_ejercicio_id ON public.equipos_gimnasio(ejercicio_id);
CREATE INDEX idx_sesiones_usuario_id ON public.sesiones_entrenamiento(usuario_id);
CREATE INDEX idx_sesiones_gimnasio_id ON public.sesiones_entrenamiento(gimnasio_id);
CREATE INDEX idx_sesiones_fecha ON public.sesiones_entrenamiento(fecha);
CREATE INDEX idx_series_sesion_id ON public.series_ejercicios(sesion_entrenamiento_id);
CREATE INDEX idx_series_equipo_id ON public.series_ejercicios(equipo_gimnasio_id);

-- ============================================
-- SEGURIDAD A NIVEL DE FILA (RLS)
-- ============================================

ALTER TABLE public.perfiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.gimnasios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ejercicios ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.equipos_gimnasio ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sesiones_entrenamiento ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.series_ejercicios ENABLE ROW LEVEL SECURITY;

-- Perfiles: usuarios pueden ver/editar solo su propio perfil
CREATE POLICY "Los usuarios pueden ver su propio perfil"
    ON public.perfiles FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Los usuarios pueden actualizar su propio perfil"
    ON public.perfiles FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Los usuarios pueden insertar su propio perfil"
    ON public.perfiles FOR INSERT
    WITH CHECK (auth.uid() = id);

-- Gimnasios: todos los usuarios autenticados pueden ver gyms
CREATE POLICY "Usuarios autenticados pueden ver gimnasios"
    ON public.gimnasios FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Usuarios autenticados pueden crear gimnasios"
    ON public.gimnasios FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Ejercicios: todos los usuarios autenticados pueden ver ejercicios
CREATE POLICY "Usuarios autenticados pueden ver ejercicios"
    ON public.ejercicios FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Usuarios autenticados pueden crear ejercicios"
    ON public.ejercicios FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Equipos de gimnasio: usuarios pueden ver equipos de su gimnasio
CREATE POLICY "Usuarios pueden ver equipos"
    ON public.equipos_gimnasio FOR SELECT
    TO authenticated
    USING (true);

CREATE POLICY "Usuarios pueden insertar equipos"
    ON public.equipos_gimnasio FOR INSERT
    TO authenticated
    WITH CHECK (true);

CREATE POLICY "Usuarios pueden actualizar sus propios equipos"
    ON public.equipos_gimnasio FOR UPDATE
    TO authenticated
    USING (creado_por_usuario_id = auth.uid());

-- Sesiones de entrenamiento: usuarios solo ven/manejan sus propias sesiones
CREATE POLICY "Usuarios pueden ver sus propias sesiones"
    ON public.sesiones_entrenamiento FOR SELECT
    TO authenticated
    USING (usuario_id = auth.uid());

CREATE POLICY "Usuarios pueden crear sus propias sesiones"
    ON public.sesiones_entrenamiento FOR INSERT
    TO authenticated
    WITH CHECK (usuario_id = auth.uid());

CREATE POLICY "Usuarios pueden actualizar sus propias sesiones"
    ON public.sesiones_entrenamiento FOR UPDATE
    TO authenticated
    USING (usuario_id = auth.uid());

CREATE POLICY "Usuarios pueden eliminar sus propias sesiones"
    ON public.sesiones_entrenamiento FOR DELETE
    TO authenticated
    USING (usuario_id = auth.uid());

-- Series de ejercicios: usuarios manejan series a través de sus sesiones
CREATE POLICY "Usuarios pueden ver series a través de sus sesiones"
    ON public.series_ejercicios FOR SELECT
    TO authenticated
    USING (
        sesion_entrenamiento_id IN (
            SELECT id FROM public.sesiones_entrenamiento WHERE usuario_id = auth.uid()
        )
    );

CREATE POLICY "Usuarios pueden crear series a través de sus sesiones"
    ON public.series_ejercicios FOR INSERT
    TO authenticated
    WITH CHECK (
        sesion_entrenamiento_id IN (
            SELECT id FROM public.sesiones_entrenamiento WHERE usuario_id = auth.uid()
        )
    );

CREATE POLICY "Usuarios pueden actualizar series a través de sus sesiones"
    ON public.series_ejercicios FOR UPDATE
    TO authenticated
    USING (
        sesion_entrenamiento_id IN (
            SELECT id FROM public.sesiones_entrenamiento WHERE usuario_id = auth.uid()
        )
    );

CREATE POLICY "Usuarios pueden eliminar series a través de sus sesiones"
    ON public.series_ejercicios FOR DELETE
    TO authenticated
    USING (
        sesion_entrenamiento_id IN (
            SELECT id FROM public.sesiones_entrenamiento WHERE usuario_id = auth.uid()
        )
    );

-- ============================================
-- FUNCIONES Y TRIGGERS
-- ============================================

-- Auto-crear perfil cuando un usuario se registra
CREATE OR REPLACE FUNCTION public.crear_perfil_automatico()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.perfiles (id, email, nombre_completo, google_id)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.raw_user_meta_data->>'name'),
        NEW.raw_user_meta_data->>'sub'
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger para crear perfil automáticamente
CREATE OR REPLACE TRIGGER al_crear_usuario_auth
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.crear_perfil_automatico();

-- Auto-actualizar timestamp actualizado_en
CREATE OR REPLACE FUNCTION public.actualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.actualizado_en = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER actualizar_perfiles_timestamp
    BEFORE UPDATE ON public.perfiles
    FOR EACH ROW EXECUTE FUNCTION public.actualizar_timestamp();

CREATE TRIGGER actualizar_gimnasios_timestamp
    BEFORE UPDATE ON public.gimnasios
    FOR EACH ROW EXECUTE FUNCTION public.actualizar_timestamp();

CREATE TRIGGER actualizar_equipos_timestamp
    BEFORE UPDATE ON public.equipos_gimnasio
    FOR EACH ROW EXECUTE FUNCTION public.actualizar_timestamp();

CREATE TRIGGER actualizar_sesiones_timestamp
    BEFORE UPDATE ON public.sesiones_entrenamiento
    FOR EACH ROW EXECUTE FUNCTION public.actualizar_timestamp();

-- ============================================
-- DATOS DE EJEMPLO (opcional)
-- ============================================

-- Gimnasios de ejemplo
INSERT INTO public.gimnasios (nombre, sucursal, direccion) VALUES
('Smart Fit Prat', 'Prat', 'Av. Prat 123, Santiago'),
('Smart Fit Centro', 'Centro', 'Ahumada 456, Santiago'),
('Elysium Gym', 'Premium', 'Av. Providencia 789, Santiago');

-- Ejercicios de ejemplo
INSERT INTO public.ejercicios (nombre_tecnico, grupo_muscular, descripcion) VALUES
('Press de Banca', 'pecho', 'Press de banca con barra'),
('Press Inclinado con Mancuernas', 'pecho', 'Press inclinado con mancuernas'),
('Aperturas en Polea', 'pecho', 'Aperturas en máquina de poleas'),
('Jalón al Pecho', 'espalda', 'Jalón al pecho con agarre amplio'),
('Remo Sentado en Polea', 'espalda', 'Remo sentado en polea baja'),
('Remo en T', 'espalda', 'Remo bent over con barra en T'),
('Press Militar', 'hombros', 'Press de hombros de pie con barra'),
('Elevaciones Laterales', 'hombros', 'Elevaciones laterales con mancuernas'),
('Extensión de Tríceps en Polea', 'tríceps', 'Extensión de tríceps en polea alta'),
('Fondos en Paralelas', 'tríceps', 'Fondos en barras paralelas'),
('Curl de Bíceps', 'bíceps', 'Curl con mancuernas');

-- Equipos de ejemplo para Smart Fit Prat (gimnasio_id = 1)
-- Primero verificamos que existan los gyms y ejercicios
DO $$
DECLARE
    gym_1_id INTEGER;
    gym_2_id INTEGER;
    ejercicio_1 INTEGER;
    ejercicio_2 INTEGER;
    ejercicio_3 INTEGER;
    ejercicio_4 INTEGER;
    ejercicio_5 INTEGER;
    ejercicio_6 INTEGER;
    ejercicio_7 INTEGER;
    ejercicio_8 INTEGER;
    ejercicio_9 INTEGER;
    ejercicio_10 INTEGER;
    ejercicio_11 INTEGER;
BEGIN
    -- Obtener IDs de gyms
    SELECT id INTO gym_1_id FROM public.gimnasios WHERE nombre = 'Smart Fit Prat' LIMIT 1;
    SELECT id INTO gym_2_id FROM public.gimnasios WHERE nombre = 'Smart Fit Centro' LIMIT 1;

    -- Obtener IDs de ejercicios
    SELECT id INTO ejercicio_1 FROM public.ejercicios WHERE nombre_tecnico = 'Press de Banca' LIMIT 1;
    SELECT id INTO ejercicio_2 FROM public.ejercicios WHERE nombre_tecnico = 'Press Inclinado con Mancuernas' LIMIT 1;
    SELECT id INTO ejercicio_3 FROM public.ejercicios WHERE nombre_tecnico = 'Aperturas en Polea' LIMIT 1;
    SELECT id INTO ejercicio_4 FROM public.ejercicios WHERE nombre_tecnico = 'Jalón al Pecho' LIMIT 1;
    SELECT id INTO ejercicio_5 FROM public.ejercicios WHERE nombre_tecnico = 'Remo Sentado en Polea' LIMIT 1;
    SELECT id INTO ejercicio_6 FROM public.ejercicios WHERE nombre_tecnico = 'Remo en T' LIMIT 1;
    SELECT id INTO ejercicio_7 FROM public.ejercicios WHERE nombre_tecnico = 'Press Militar' LIMIT 1;
    SELECT id INTO ejercicio_8 FROM public.ejercicios WHERE nombre_tecnico = 'Elevaciones Laterales' LIMIT 1;
    SELECT id INTO ejercicio_9 FROM public.ejercicios WHERE nombre_tecnico = 'Extensión de Tríceps en Polea' LIMIT 1;
    SELECT id INTO ejercicio_10 FROM public.ejercicios WHERE nombre_tecnico = 'Fondos en Paralelas' LIMIT 1;
    SELECT id INTO ejercicio_11 FROM public.ejercicios WHERE nombre_tecnico = 'Curl de Bíceps' LIMIT 1;

    -- Insertar equipos para Smart Fit Prat
    IF gym_1_id IS NOT NULL AND ejercicio_1 IS NOT NULL THEN
        INSERT INTO public.equipos_gimnasio (gimnasio_id, ejercicio_id, alias_personalizado, tipo_unidad) VALUES
        (gym_1_id, ejercicio_1, 'Press de Banca', 'kg'),
        (gym_1_id, ejercicio_2, 'Press Inclinado', 'kg'),
        (gym_1_id, ejercicio_3, 'Polea Alta Pecho', 'kg'),
        (gym_1_id, ejercicio_4, 'Jalón Dorsal', 'kg'),
        (gym_1_id, ejercicio_5, 'Remo Bajo', 'kg'),
        (gym_1_id, ejercicio_6, 'Remo T', 'kg'),
        (gym_1_id, ejercicio_7, 'Press Militar', 'kg'),
        (gym_1_id, ejercicio_8, 'Elev Lateral', 'kg'),
        (gym_1_id, ejercicio_9, 'Tríceps Polea', 'kg'),
        (gym_1_id, ejercicio_10, 'Fondos', 'kg'),
        (gym_1_id, ejercicio_11, 'Curl Bíceps', 'kg');
    END IF;

    -- Insertar equipos para Smart Fit Centro (algunos)
    IF gym_2_id IS NOT NULL AND ejercicio_1 IS NOT NULL THEN
        INSERT INTO public.equipos_gimnasio (gimnasio_id, ejercicio_id, alias_personalizado, tipo_unidad) VALUES
        (gym_2_id, ejercicio_1, 'Press Banca', 'kg'),
        (gym_2_id, ejercicio_4, 'Jalón Pecho', 'kg'),
        (gym_2_id, ejercicio_5, 'Remo Sentado', 'kg'),
        (gym_2_id, ejercicio_7, 'Press Hombros', 'kg'),
        (gym_2_id, ejercicio_9, 'Tríceps', 'kg');
    END IF;
END $$;
