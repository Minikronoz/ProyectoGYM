import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServicioSupabase, SesionEntrenamiento } from '../../services/supabase.service';
import { CommonModule } from '@angular/common';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonList, IonItem, IonLabel, IonLoading, IonButtons, IonBackButton
} from '@ionic/angular/standalone';

@Component({
  selector: 'app-history',
  templateUrl: './history.page.html',
  styleUrls: ['./history.page.scss'],
  standalone: true,
  imports: [
    CommonModule,
    IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
    IonList, IonItem, IonLabel, IonLoading, IonButtons, IonBackButton
  ]
})
export class HistorialPage implements OnInit {
  sesiones: SesionEntrenamiento[] = [];
  cargando = true;

  constructor(
    private supabase: ServicioSupabase,
    private router: Router
  ) {}

  async ngOnInit(): Promise<void> {
    await this.cargarSesiones();
  }

  async cargarSesiones(): Promise<void> {
    try {
      this.sesiones = await this.supabase.obtenerSesiones();
    } catch (error) {
      console.error('Error al cargar sesiones:', error);
    } finally {
      this.cargando = false;
    }
  }

  verSesion(sesionId: number): void {
    console.log('Ver sesión:', sesionId);
  }

  irAtras(): void {
    this.router.navigate(['/gym-selector']);
  }

  obtenerIconoSesion(): string {
    return 'barbell-outline';
  }

  formatearFecha(fechaStr: string): string {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
}
