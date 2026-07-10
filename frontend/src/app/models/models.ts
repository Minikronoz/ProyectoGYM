export interface User {
  id: number;
  email: string;
  name: string;
  google_id: string;
  created_at: string;
}

export interface Gym {
  id: number;
  name: string;
  branch: string;
  address?: string;
  created_at: string;
}

export interface Exercise {
  id: number;
  technical_name: string;
  target_muscle_group: string;
  description?: string;
}

export interface GymEquipment {
  id: number;
  gym_id: number;
  exercise_id: number;
  custom_alias: string;
  unit_type: UnitType;
  plate_weight_equivalent?: number;
  created_by_user_id?: number;
  created_at: string;
  gym_name?: string;
  exercise_name?: string;
  target_muscle_group?: string;
}

export enum UnitType {
  KG = 'kg',
  LBS = 'lbs',
  PLATES = 'plates',
  BODYWEIGHT = 'bodyweight',
  PER_SIDE_KG = 'per_side_kg'
}

export enum SetType {
  WARMUP = 'warmup',
  NORMAL = 'normal',
  FAILURE = 'failure',
  DROP_SET = 'drop_set'
}

export interface WorkoutSession {
  id: number;
  user_id: number;
  gym_id: number;
  date: string;
  general_notes?: string;
  is_synced: boolean;
  client_id?: string;
  created_at: string;
  updated_at?: string;
  sets?: ExerciseSet[];
}

export interface ExerciseSet {
  id: number;
  workout_session_id: number;
  gym_equipment_id: number;
  set_number: number;
  set_type: SetType;
  weight_value: number;
  reps_count: number;
  is_to_failure: boolean;
  set_notes?: string;
  created_at?: string;
  equipment_alias?: string;
  exercise_name?: string;
  unit_type?: string;
}

export interface SyncSetData {
  client_set_id: string;
  gym_equipment_id: number;
  set_number: number;
  set_type: SetType;
  weight_value: number;
  reps_count: number;
  is_to_failure: boolean;
  set_notes?: string;
}

export interface SyncSessionData {
  client_session_id: string;
  gym_id: number;
  date: string;
  general_notes?: string;
  sets: SyncSetData[];
}

export interface SyncRequest {
  sessions: SyncSessionData[];
  client_created_at?: string;
}

export interface SyncResponse {
  synced_sessions: {
    client_session_id: string;
    server_session_id: number;
    synced_sets: number;
    status: string;
  }[];
  total_sets_synced: number;
  sync_timestamp: string;
}

export interface ProgressDataPoint {
  date: string;
  total_volume: number;
  max_weight: number;
  total_reps: number;
  total_sets: number;
}

export interface ExerciseProgress {
  exercise_id: number;
  exercise_name: string;
  gym_equipment_id: number;
  equipment_alias: string;
  data_points: ProgressDataPoint[];
}

export interface ProgressResponse {
  user_id: number;
  gym_id?: number;
  exercise_id?: number;
  from_date?: string;
  to_date?: string;
  progress: ExerciseProgress[];
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
