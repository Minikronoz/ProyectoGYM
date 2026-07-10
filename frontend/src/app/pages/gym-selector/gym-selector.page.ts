import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { Gym } from '../../models/models';
import { CommonModule } from '@angular/common';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonList, IonItem, IonLabel, IonLoading, IonButtons
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-gym-selector',
  templateUrl: './gym-selector.page.html',
  styleUrls: ['./gym-selector.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
    IonList, IonItem, IonLabel, IonLoading, IonButtons
  ]
})
export class GymSelectorPage implements OnInit {
  gyms: Gym[] = [];
  selectedGymId: number | null = null;
  userName: string = '';
  isLoading = true;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  async ngOnInit(): Promise<void> {
    await this.loadGyms();
    const user = await this.api.getCurrentUser();
    if (user) {
      this.userName = user.name || user.email;
    }
  }

  async loadGyms(): Promise<void> {
    try {
      this.gyms = await this.api.getGyms();
      if (this.gyms.length === 0) {
        const defaultGym = await this.api.createGym({
          name: 'Smart Fit',
          branch: 'Prat',
          address: 'Prat, Chile'
        });
        this.gyms = [defaultGym];
      }
    } catch (error) {
      console.error('Error loading gyms:', error);
    } finally {
      this.isLoading = false;
    }
  }

  selectGym(gymId: number): void {
    this.selectedGymId = gymId;
  }

  startWorkout(): void {
    if (this.selectedGymId) {
      this.router.navigate(['/workout-day'], {
        queryParams: { gymId: this.selectedGymId }
      });
    }
  }

  viewHistory(): void {
    this.router.navigate(['/history']);
  }

  async logout(): Promise<void> {
    await this.api.logout();
    this.router.navigate(['/login']);
  }
}
