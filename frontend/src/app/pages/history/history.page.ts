import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { WorkoutSession } from '../../models/models';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonLoading, IonButtons, IonBackButton
} from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-history',
  templateUrl: './history.page.html',
  styleUrls: ['./history.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
    IonLoading, IonButtons, IonBackButton
  ]
})
export class HistoryPage implements OnInit {
  sessions: WorkoutSession[] = [];
  isLoading = true;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  async ngOnInit(): Promise<void> {
    await this.loadSessions();
  }

  async loadSessions(): Promise<void> {
    try {
      this.sessions = await this.api.getSessions();
    } catch (error) {
      console.error('Error loading sessions:', error);
    } finally {
      this.isLoading = false;
    }
  }

  viewSession(sessionId: number): void {
    console.log('View session:', sessionId);
  }

  goBack(): void {
    this.router.navigate(['/gym-selector']);
  }

  getSessionIcon(): string {
    return 'barbell-outline';
  }

  formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
}
