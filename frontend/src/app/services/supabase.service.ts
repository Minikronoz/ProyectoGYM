import { Injectable } from '@angular/core';
import { createClient, SupabaseClient, Session } from '@supabase/supabase-js';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Perfil {
  id: string;
  email: string;
  nombre_completo: string;
  google_id: string;
  creado_en: string;
}

export interface Gimnasio {
  id: number;
  nombre: string;
  sucursal: string;
  direccion: string;
  creado_en: string;
}

export interface Ejercicio {
  id: number;
  nombre_tecnico: string;
  grupo_muscular: string;
  descripcion: string;
}

export interface EquipoGimnasio {
  id: number;
  gimnasio_id: number;
  ejercicio_id: number;
  alias_personalizado: string;
  tipo_unidad: string;
  peso_equivalente_placa: number;
  creado_por_usuario_id: string;
  creado_en: string;
  nombre_gimnasio?: string;
  nombre_ejercicio?: string;
  grupo_muscular?: string;
}

export interface SesionEntrenamiento {
  id: number;
  usuario_id: string;
  gimnasio_id: number;
  fecha: string;
  notas_generales: string;
  id_cliente: string;
  creado_en: string;
  actualizado_en: string;
  series?: SerieEjercicio[];
}

export interface SerieEjercicio {
  id: number;
  sesion_entrenamiento_id: number;
  equipo_gimnasio_id: number;
  numero_serie: number;
  tipo_serie: string;
  valor_peso: number;
  cantidad_reps: number;
  hasta_falla: boolean;
  notas_serie: string;
  id_cliente: string;
  creado_en: string;
  alias_equipo?: string;
  nombre_ejercicio?: string;
  tipo_unidad?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ServicioSupabase {
  private cliente: SupabaseClient;
  private _sesion: Session | null = null;
  private sesionSubject = new BehaviorSubject<Session | null>(null);

  constructor() {
    const supabaseUrl = environment.supabaseUrl;
    const supabaseKey = environment.supabaseAnonKey;

    this.cliente = createClient(supabaseUrl, supabaseKey, {
      auth: {
        persistSession: true,
        autoRefreshToken: true,
      }
    });

    this.iniciarSesion();
  }

  private async iniciarSesion(): Promise<void> {
    const { data } = await this.cliente.auth.getSession();
    this._sesion = data.session;
    this.sesionSubject.next(this._sesion);

    this.cliente.auth.onAuthStateChange((event, session) => {
      this._sesion = session;
      this.sesionSubject.next(session);
    });
  }

  get sesion(): Session | null {
    return this._sesion;
  }

  get sesion$(): Observable<Session | null> {
    return this.sesionSubject.asObservable();
  }

  get usuario(): Perfil | null {
    if (!this._sesion?.user) return null;
    return this._sesion.user.user_metadata as Perfil;
  }

  get estaAutenticado(): boolean {
    return !!this._sesion?.access_token;
  }

  // Métodos de autenticación
  async iniciarSesionConGoogle(): Promise<void> {
    const { data, error } = await this.cliente.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`
      }
    });

    if (error) throw error;
  }

  async manejarCallbackAuth(): Promise<void> {
    const { data, error } = await this.cliente.auth.getSession();
    if (error) throw error;
    this._sesion = data.session;
    this.sesionSubject.next(data.session);
  }

  async obtenerSesionDesdeUrl(): Promise<void> {
    const { data, error } = await this.cliente.auth.getSession();
    if (error) throw error;
    this._sesion = data.session;
    this.sesionSubject.next(data.session);
  }

  async procesarCallbackAuth(): Promise<void> {
    const { data, error } = await this.cliente.auth.getSession();
    if (error) throw error;

    if (data.session) {
      this._sesion = data.session;
      this.sesionSubject.next(data.session);
      return;
    }

    return new Promise<void>((resolve, reject) => {
      const timeout = setTimeout(() => {
        subscription?.unsubscribe();
        reject(new Error('Timeout esperando sesión'));
      }, 10000);

      const { data: { subscription } } = this.cliente.auth.onAuthStateChange((event, session) => {
        if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED' || session?.access_token) {
          this._sesion = session;
          this.sesionSubject.next(session);
          clearTimeout(timeout);
          subscription.unsubscribe();
          resolve();
        }
      });
    });
  }

  async cerrarSesion(): Promise<void> {
    const { error } = await this.cliente.auth.signOut();
    if (error) throw error;
    this._sesion = null;
    this.sesionSubject.next(null);
  }

  // Gimnasios
  async obtenerGimnasios(): Promise<Gimnasio[]> {
    const { data, error } = await this.cliente
      .from('gimnasios')
      .select('*')
      .order('nombre');

    if (error) throw error;
    return data || [];
  }

  async crearGimnasio(gimnasio: Partial<Gimnasio>): Promise<Gimnasio> {
    const { data, error } = await this.cliente
      .from('gimnasios')
      .insert(gimnasio)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  // Ejercicios
  async obtenerEjercicios(): Promise<Ejercicio[]> {
    const { data, error } = await this.cliente
      .from('ejercicios')
      .select('*')
      .order('grupo_muscular');

    if (error) throw error;
    return data || [];
  }

  async crearEjercicio(ejercicio: Partial<Ejercicio>): Promise<Ejercicio> {
    const { data, error } = await this.cliente
      .from('ejercicios')
      .insert(ejercicio)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  // Equipos de gimnasio
  async obtenerEquipos(gimnasioId?: number): Promise<EquipoGimnasio[]> {
    let query = this.cliente
      .from('equipos_gimnasio')
      .select(`
        *,
        gimnasio:gimnasios(nombre),
        ejercicio:ejercicios(nombre_tecnico, grupo_muscular)
      `);

    if (gimnasioId) {
      query = query.eq('gimnasio_id', gimnasioId);
    }

    const { data, error } = await query;

    if (error) throw error;

    return (data || []).map(item => ({
      ...item,
      nombre_gimnasio: (item.gimnasio as any)?.nombre,
      nombre_ejercicio: (item.ejercicio as any)?.nombre_tecnico,
      grupo_muscular: (item.ejercicio as any)?.grupo_muscular
    }));
  }

  async crearEquipo(equipo: Partial<EquipoGimnasio>): Promise<EquipoGimnasio> {
    const { data, error } = await this.cliente
      .from('equipos_gimnasio')
      .insert(equipo)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async obtenerUltimaSerieParaEquipo(equipoId: number): Promise<SerieEjercicio | null> {
    const { data, error } = await this.cliente
      .from('series_ejercicios')
      .select('*')
      .eq('equipo_gimnasio_id', equipoId)
      .order('creado_en', { ascending: false })
      .limit(1);

    if (error && error.code !== 'PGRST116') throw error;
    return data && data.length > 0 ? data[0] : null;
  }

  // Sesiones de entrenamiento
  async obtenerSesiones(gimnasioId?: number): Promise<SesionEntrenamiento[]> {
    let query = this.cliente
      .from('sesiones_entrenamiento')
      .select(`
        *,
        gimnasio:gimnasios(nombre),
        series:series_ejercicios(*)
      `)
      .order('fecha', { ascending: false });

    if (gimnasioId) {
      query = query.eq('gimnasio_id', gimnasioId);
    }

    const { data, error } = await query;

    if (error) throw error;
    return data || [];
  }

  async obtenerSesion(sesionId: number): Promise<SesionEntrenamiento | null> {
    const { data, error } = await this.cliente
      .from('sesiones_entrenamiento')
      .select(`
        *,
        gimnasio:gimnasios(*),
        series:series_ejercicios(*)
      `)
      .eq('id', sesionId)
      .single();

    if (error) throw error;
    return data;
  }

  async crearSesion(sesion: Partial<SesionEntrenamiento>): Promise<SesionEntrenamiento> {
    const { data, error } = await this.cliente
      .from('sesiones_entrenamiento')
      .insert(sesion)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async actualizarSesion(sesionId: number, actualizaciones: Partial<SesionEntrenamiento>): Promise<SesionEntrenamiento> {
    const { data, error } = await this.cliente
      .from('sesiones_entrenamiento')
      .update(actualizaciones)
      .eq('id', sesionId)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async eliminarSesion(sesionId: number): Promise<void> {
    const { error } = await this.cliente
      .from('sesiones_entrenamiento')
      .delete()
      .eq('id', sesionId);

    if (error) throw error;
  }

  // Series de ejercicios
  async crearSerie(serie: Partial<SerieEjercicio>): Promise<SerieEjercicio> {
    const { data, error } = await this.cliente
      .from('series_ejercicios')
      .insert(serie)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async actualizarSerie(serieId: number, actualizaciones: Partial<SerieEjercicio>): Promise<SerieEjercicio> {
    const { data, error } = await this.cliente
      .from('series_ejercicios')
      .update(actualizaciones)
      .eq('id', serieId)
      .select()
      .single();

    if (error) throw error;
    return data;
  }

  async eliminarSerie(serieId: number): Promise<void> {
    const { error } = await this.cliente
      .from('series_ejercicios')
      .delete()
      .eq('id', serieId);

    if (error) throw error;
  }

  // Progreso/Análisis
  async obtenerProgreso(gimnasioId?: number, ejercicioId?: number): Promise<any[]> {
    let query = this.cliente
      .from('series_ejercicios')
      .select(`
        *,
        sesion_entrenamiento:sesiones_entrenamiento(fecha, gimnasio_id),
        equipo:equipos_gimnasio(
          id,
          alias_personalizado,
          tipo_unidad,
          ejercicio:ejercicios(nombre_tecnico)
        )
      `)
      .order('creado_en');

    if (gimnasioId) {
      query = query.eq('sesion_entrenamiento.gimnasio_id', gimnasioId);
    }

    if (ejercicioId) {
      query = query.eq('equipo.ejercicio_id', ejercicioId);
    }

    const { data, error } = await query;

    if (error) throw error;
    return data || [];
  }
}
