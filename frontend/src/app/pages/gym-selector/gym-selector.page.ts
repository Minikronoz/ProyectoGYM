import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServicioSupabase } from '../../services/supabase.service';
import { Gimnasio } from '../../services/supabase.service';
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
export class GimnasioSelectorPage implements OnInit {
  gimnasios: Gimnasio[] = [];
  gimnasioSeleccionadoId: number | null = null;
  nombreUsuario: string = '';
  cargando = true;

  constructor(
    private supabase: ServicioSupabase,
    private router: Router
  ) {}

  async ngOnInit(): Promise<void> {
    await this.cargarGimnasios();
    const usuario = this.supabase.usuario;
    if (usuario) {
      this.nombreUsuario = usuario.nombre_completo || usuario.email;
    }
  }

  async cargarGimnasios(): Promise<void> {
    try {
      this.gimnasios = await this.supabase.obtenerGimnasios();
      if (this.gimnasios.length === 0) {
        const gimnasioPredeterminado = await this.supabase.crearGimnasio({
          nombre: 'Smart Fit',
          sucursal: 'Prat',
          direccion: 'Prat, Chile'
        });
        this.gimnasios = [gimnasioPredeterminado];
      }
    } catch (error) {
      console.error('Error al cargar gimnasios:', error);
    } finally {
      this.cargando = false;
    }
  }

  seleccionarGimnasio(gimnasioId: number): void {
    this.gimnasioSeleccionadoId = gimnasioId;
  }

  comenzarEntrenamiento(): void {
    if (this.gimnasioSeleccionadoId) {
      this.router.navigate(['/workout-day'], {
        queryParams: { gimnasioId: this.gimnasioSeleccionadoId }
      });
    }
  }

  verHistorial(): void {
    this.router.navigate(['/history']);
  }

  async cerrarSesion(): Promise<void> {
    await this.supabase.cerrarSesion();
    this.router.navigate(['/login']);
  }
}
