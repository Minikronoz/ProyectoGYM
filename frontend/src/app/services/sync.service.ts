import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage-angular';
import { v4 as uuidv4 } from 'uuid';
import { SyncSessionData, SyncSetData, WorkoutSession, ExerciseSet, SetType } from '../models/models';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class SyncService {
  private readonly STORAGE_KEY = 'pending_sync_sessions';

  constructor(
    private storage: Storage,
    private api: ApiService
  ) {}

  async addLocalSession(session: WorkoutSession): Promise<void> {
    const pending = await this.getPendingSessions();
    const sessionData = this.toSyncSessionData(session);
    pending.push(sessionData);
    await this.storage.set(this.STORAGE_KEY, JSON.stringify(pending));
  }

  async getPendingSessions(): Promise<SyncSessionData[]> {
    const data = await this.storage.get(this.STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  }

  async clearPendingSessions(): Promise<void> {
    await this.storage.remove(this.STORAGE_KEY);
  }

  async syncAll(): Promise<{success: boolean, syncedCount: number}> {
    const pending = await this.getPendingSessions();
    if (pending.length === 0) {
      return { success: true, syncedCount: 0 };
    }

    try {
      const response = await this.api.syncWorkouts({
        sessions: pending,
        client_created_at: new Date().toISOString()
      });

      if (response.total_sets_synced > 0) {
        await this.clearPendingSessions();
        return { success: true, syncedCount: response.total_sets_synced };
      }
      return { success: false, syncedCount: 0 };
    } catch (error) {
      console.error('Sync failed:', error);
      return { success: false, syncedCount: 0 };
    }
  }

  async hasPendingSync(): Promise<boolean> {
    const pending = await this.getPendingSessions();
    return pending.length > 0;
  }

  private toSyncSessionData(session: WorkoutSession): SyncSessionData {
    const sets: SyncSetData[] = (session.sets || []).map(set => ({
      client_set_id: uuidv4(),
      gym_equipment_id: set.gym_equipment_id,
      set_number: set.set_number,
      set_type: set.set_type || SetType.NORMAL,
      weight_value: set.weight_value,
      reps_count: set.reps_count,
      is_to_failure: set.is_to_failure,
      set_notes: set.set_notes
    }));

    return {
      client_session_id: session.client_id || uuidv4(),
      gym_id: session.gym_id,
      date: session.date,
      general_notes: session.general_notes,
      sets
    };
  }
}
