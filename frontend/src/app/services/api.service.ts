import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { Observable, from, switchMap, firstValueFrom } from 'rxjs';
import {
  AuthResponse,
  User,
  Gym,
  Exercise,
  GymEquipment,
  WorkoutSession,
  ExerciseSet,
  SyncRequest,
  SyncResponse,
  ProgressResponse
} from '../models/models';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'https://proyectogym-3nun.onrender.com';

  constructor(
    private http: HttpClient,
    private storage: Storage
  ) {
    this.initStorage();
  }

  private async initStorage(): Promise<void> {
    await this.storage.create();
  }

  private async getAuthHeaders(): Promise<HttpHeaders> {
    const token = await this.storage.get('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  // Auth
  async loginWithGoogle(): Promise<void> {
    const googleAuthUrl = await firstValueFrom(this.http.get<{url: string}>(`${this.apiUrl}/auth/google/url`));
    window.location.href = googleAuthUrl.url;
  }

  async handleGoogleCallback(code: string): Promise<AuthResponse> {
    const response = await firstValueFrom(this.http.get<AuthResponse>(`${this.apiUrl}/auth/callback?code=${code}`));
    await this.storage.set('access_token', response.access_token);
    await this.storage.set('user', response.user);
    return response;
  }

  async getCurrentUser(): Promise<User | null> {
    const token = await this.storage.get('access_token');
    if (!token) return null;
    try {
      const headers = await this.getAuthHeaders();
      return await firstValueFrom(this.http.get<User>(`${this.apiUrl}/auth/me`, { headers }));
    } catch {
      await this.logout();
      return null;
    }
  }

  async logout(): Promise<void> {
    await this.storage.remove('access_token');
    await this.storage.remove('user');
  }

  async isAuthenticated(): Promise<boolean> {
    const token = await this.storage.get('access_token');
    return !!token;
  }

  // Gyms
  async getGyms(): Promise<Gym[]> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.get<Gym[]>(`${this.apiUrl}/gyms/`, { headers }));
  }

  async createGym(gym: Partial<Gym>): Promise<Gym> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.post<Gym>(`${this.apiUrl}/gyms/`, gym, { headers }));
  }

  // Exercises
  async getExercises(muscleGroup?: string): Promise<Exercise[]> {
    const headers = await this.getAuthHeaders();
    const params = muscleGroup ? `?muscle_group=${muscleGroup}` : '';
    return firstValueFrom(this.http.get<Exercise[]>(`${this.apiUrl}/exercises/${params}`, { headers }));
  }

  async createExercise(exercise: Partial<Exercise>): Promise<Exercise> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.post<Exercise>(`${this.apiUrl}/exercises/`, exercise, { headers }));
  }

  // Equipment
  async getEquipment(gymId?: number): Promise<GymEquipment[]> {
    const headers = await this.getAuthHeaders();
    const params = gymId ? `?gym_id=${gymId}` : '';
    return firstValueFrom(this.http.get<GymEquipment[]>(`${this.apiUrl}/workouts/equipment/${params}`, { headers }));
  }

  async createEquipment(equipment: Partial<GymEquipment>): Promise<GymEquipment> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.post<GymEquipment>(`${this.apiUrl}/workouts/equipment/`, equipment, { headers }));
  }

  async getLastSetForEquipment(equipmentId: number): Promise<ExerciseSet | null> {
    const headers = await this.getAuthHeaders();
    try {
      return await firstValueFrom(this.http.get<ExerciseSet>(`${this.apiUrl}/workouts/equipment/${equipmentId}/last-set`, { headers }));
    } catch {
      return null;
    }
  }

  // Workout Sessions
  async getSessions(gymId?: number): Promise<WorkoutSession[]> {
    const headers = await this.getAuthHeaders();
    const params = gymId ? `?gym_id=${gymId}` : '';
    return firstValueFrom(this.http.get<WorkoutSession[]>(`${this.apiUrl}/workouts/sessions/${params}`, { headers }));
  }

  async getSession(sessionId: number): Promise<WorkoutSession> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.get<WorkoutSession>(`${this.apiUrl}/workouts/sessions/${sessionId}`, { headers }));
  }

  async createSession(session: Partial<WorkoutSession>): Promise<WorkoutSession> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.post<WorkoutSession>(`${this.apiUrl}/workouts/sessions/`, session, { headers }));
  }

  async createSet(set: Partial<ExerciseSet>): Promise<ExerciseSet> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.post<ExerciseSet>(`${this.apiUrl}/workouts/sets/`, set, { headers }));
  }

  // Sync
  async syncWorkouts(syncData: SyncRequest): Promise<SyncResponse> {
    const headers = await this.getAuthHeaders();
    return firstValueFrom(this.http.post<SyncResponse>(`${this.apiUrl}/sync/`, syncData, { headers }));
  }

  // Analytics
  async getProgress(gymId?: number, exerciseId?: number): Promise<ProgressResponse> {
    const headers = await this.getAuthHeaders();
    let params = '';
    if (gymId) params += `gym_id=${gymId}&`;
    if (exerciseId) params += `exercise_id=${exerciseId}&`;
    const url = params ? `${this.apiUrl}/analytics/progress/?${params}` : `${this.apiUrl}/analytics/progress/`;
    return firstValueFrom(this.http.get<ProgressResponse>(url, { headers }));
  }
}
