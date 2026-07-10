import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { GymEquipment, WorkoutSession } from '../../models/models';
import { v4 as uuidv4 } from 'uuid';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonList, IonItem, IonLabel, IonLoading, IonButtons, IonBackButton,
  IonDatetime, IonInput, IonCheckbox
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-workout-day',
  templateUrl: './workout-day.page.html',
  styleUrls: ['./workout-day.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
    IonList, IonItem, IonLabel, IonLoading, IonButtons, IonBackButton,
    IonDatetime, IonInput, IonCheckbox
  ]
})
export class WorkoutDayPage implements OnInit {
  gymId!: number;
  equipment: GymEquipment[] = [];
  recentSessions: WorkoutSession[] = [];
  selectedEquipmentIds: number[] = [];
  workoutDate: string = new Date().toISOString().split('T')[0];
  workoutNotes: string = '';
  isLoading = true;
  session: WorkoutSession | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private api: ApiService
  ) {}

  async ngOnInit(): Promise<void> {
    this.gymId = Number(this.route.snapshot.queryParams['gymId']);
    await this.loadData();
  }

  async loadData(): Promise<void> {
    try {
      this.equipment = await this.api.getEquipment(this.gymId);
      this.recentSessions = await this.api.getSessions(this.gymId);
      this.recentSessions = this.recentSessions.slice(0, 5);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      this.isLoading = false;
    }
  }

  toggleEquipment(equipmentId: number): void {
    const index = this.selectedEquipmentIds.indexOf(equipmentId);
    if (index > -1) {
      this.selectedEquipmentIds.splice(index, 1);
    } else {
      this.selectedEquipmentIds.push(equipmentId);
    }
  }

  isSelected(equipmentId: number): boolean {
    return this.selectedEquipmentIds.includes(equipmentId);
  }

  async startWorkout(): Promise<void> {
    if (this.selectedEquipmentIds.length === 0) return;

    this.session = {
      id: 0,
      user_id: 0,
      gym_id: this.gymId,
      date: this.workoutDate,
      general_notes: this.workoutNotes,
      is_synced: false,
      client_id: uuidv4(),
      created_at: new Date().toISOString(),
      sets: []
    };

    this.router.navigate(['/active-workout'], {
      queryParams: {
        gymId: this.gymId,
        equipmentIds: this.selectedEquipmentIds.join(','),
        sessionData: JSON.stringify(this.session)
      }
    });
  }

  async continuePreviousSession(sessionId: number): Promise<void> {
    const fullSession = await this.api.getSession(sessionId);
    fullSession.client_id = uuidv4();
    fullSession.date = new Date().toISOString().split('T')[0];
    fullSession.is_synced = false;
    fullSession.sets = [];

    this.router.navigate(['/active-workout'], {
      queryParams: {
        gymId: this.gymId,
        equipmentIds: fullSession.sets?.map(s => s.gym_equipment_id).join(',') || '',
        sessionData: JSON.stringify(fullSession)
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/gym-selector']);
  }
}
