import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { SyncService } from '../../services/sync.service';
import { GymEquipment, ExerciseSet, WorkoutSession, SetType } from '../../models/models';
import { CommonModule } from '@angular/common';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonLoading, IonButtons, IonAlert, IonLabel
} from '@ionic/angular/standalone';

interface EquipmentWithSets {
  equipment: GymEquipment;
  sets: ExerciseSet[];
  currentSetNumber: number;
  lastSet: ExerciseSet | null;
}

@Component({
  selector: 'app-active-workout',
  templateUrl: './active-workout.page.html',
  styleUrls: ['./active-workout.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
    IonLoading, IonButtons, IonAlert, IonLabel
  ]
})
export class ActiveWorkoutPage implements OnInit {
  gymId!: number;
  equipmentIds: number[] = [];
  session!: WorkoutSession;
  equipmentWithSets: EquipmentWithSets[] = [];
  currentEquipmentIndex = 0;
  isSaving = false;
  showFinishConfirm = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private api: ApiService,
    private syncService: SyncService
  ) {}

  async ngOnInit(): Promise<void> {
    this.gymId = Number(this.route.snapshot.queryParams['gymId']);
    const equipmentIdsStr = this.route.snapshot.queryParams['equipmentIds'];
    const sessionDataStr = this.route.snapshot.queryParams['sessionData'];

    this.equipmentIds = equipmentIdsStr.split(',').map(Number);
    this.session = JSON.parse(sessionDataStr);

    await this.loadEquipmentWithLastSets();
  }

  async loadEquipmentWithLastSets(): Promise<void> {
    const equipment = await this.api.getEquipment(this.gymId);
    const selectedEquipment = equipment.filter(eq => this.equipmentIds.includes(eq.id));

    this.equipmentWithSets = [];

    for (const eq of selectedEquipment) {
      const lastSet = await this.api.getLastSetForEquipment(eq.id);
      this.equipmentWithSets.push({
        equipment: eq,
        sets: [],
        currentSetNumber: 1,
        lastSet: lastSet
      });
    }
  }

  get currentEquipment(): EquipmentWithSets | null {
    return this.equipmentWithSets[this.currentEquipmentIndex] || null;
  }

  get totalSets(): number {
    return this.equipmentWithSets.reduce((acc, eq) => acc + eq.sets.length, 0);
  }

  addSet(equipmentIndex: number, weight: number, reps: number, isFailure: boolean = false, notes: string = ''): void {
    const eq = this.equipmentWithSets[equipmentIndex];
    const newSet: ExerciseSet = {
      id: 0,
      workout_session_id: 0,
      gym_equipment_id: eq.equipment.id,
      set_number: eq.currentSetNumber,
      set_type: isFailure ? SetType.FAILURE : SetType.NORMAL,
      weight_value: weight,
      reps_count: reps,
      is_to_failure: isFailure,
      set_notes: notes,
      equipment_alias: eq.equipment.custom_alias,
      exercise_name: eq.equipment.exercise_name
    };

    eq.sets.push(newSet);
    eq.currentSetNumber++;
  }

  goToEquipment(index: number): void {
    this.currentEquipmentIndex = index;
  }

  goNext(): void {
    if (this.currentEquipmentIndex < this.equipmentWithSets.length - 1) {
      this.currentEquipmentIndex++;
    }
  }

  goPrevious(): void {
    if (this.currentEquipmentIndex > 0) {
      this.currentEquipmentIndex--;
    }
  }

  getSetDisplay(set: ExerciseSet): string {
    const unit = set.unit_type || this.currentEquipment?.equipment.unit_type || 'kg';
    return `${set.weight_value}${unit} × ${set.reps_count}`;
  }

  getLastSetDisplay(): string {
    const last = this.currentEquipment?.lastSet;
    if (!last) return '';
    const unit = last.unit_type || this.currentEquipment?.equipment.unit_type || 'kg';
    return `Última: ${last.weight_value}${unit} × ${last.reps_count}`;
  }

  async finishWorkout(): Promise<void> {
    this.isSaving = true;
    this.showFinishConfirm = false;

    try {
      const session = {
        ...this.session,
        sets: this.equipmentWithSets.flatMap(eq => eq.sets)
      };

      await this.syncService.addLocalSession(session);

      const syncResult = await this.syncService.syncAll();
      this.router.navigate(['/gym-selector']);
    } catch (error) {
      console.error('Error saving workout:', error);
      this.router.navigate(['/gym-selector']);
    } finally {
      this.isSaving = false;
    }
  }

  goBack(): void {
    if (this.totalSets > 0) {
      this.showFinishConfirm = true;
    } else {
      this.router.navigate(['/workout-day'], {
        queryParams: { gymId: this.gymId }
      });
    }
  }

  cancelFinish(): void {
    this.showFinishConfirm = false;
  }

  discardAndExit(): void {
    this.router.navigate(['/workout-day'], {
      queryParams: { gymId: this.gymId }
    });
  }
}
