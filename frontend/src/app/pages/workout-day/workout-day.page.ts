import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioSupabase, EquipoGimnasio, SesionEntrenamiento } from '../../services/supabase.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonList, IonItem, IonLabel, IonLoading, IonButtons, IonBackButton,
  IonInput, IonCheckbox
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
    IonInput, IonCheckbox
  ]
})
export class DiaEntrenamientoPage implements OnInit {
  gimnasioId!: number;
  equipos: EquipoGimnasio[] = [];
  sesionesRecientes: SesionEntrenamiento[] = [];
  equiposSeleccionadosIds: number[] = [];
  fechaEntrenamiento: string = new Date().toISOString();
  notasEntrenamiento: string = '';
  cargando = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private supabase: ServicioSupabase
  ) {}

  async ngOnInit(): Promise<void> {
    this.gimnasioId = Number(this.route.snapshot.queryParams['gimnasioId']);
    await this.cargarDatos();
  }

  async cargarDatos(): Promise<void> {
    try {
      this.equipos = await this.supabase.obtenerEquipos(this.gimnasioId);
      this.sesionesRecientes = await this.supabase.obtenerSesiones(this.gimnasioId);
      this.sesionesRecientes = this.sesionesRecientes.slice(0, 5);
    } catch (error) {
      console.error('Error al cargar datos:', error);
    } finally {
      this.cargando = false;
    }
  }

  toggleEquipo(equipoId: number): void {
    const index = this.equiposSeleccionadosIds.indexOf(equipoId);
    if (index > -1) {
      this.equiposSeleccionadosIds.splice(index, 1);
    } else {
      this.equiposSeleccionadosIds.push(equipoId);
    }
  }

  estaSeleccionado(equipoId: number): boolean {
    return this.equiposSeleccionadosIds.includes(equipoId);
  }

  obtenerFechaHoy(): string {
    const hoy = new Date();
    return hoy.toLocaleDateString('es-ES', {
      weekday: 'long',
      day: 'numeric',
      month: 'long'
    });
  }

  formatearFecha(fechaStr: string): string {
    const fecha = new Date(fechaStr);
    return fecha.toLocaleDateString('es-ES', {
      weekday: 'short',
      day: 'numeric',
      month: 'short'
    });
  }

  async comenzarEntrenamiento(): Promise<void> {
    if (this.equiposSeleccionadosIds.length === 0) return;

    const sesion = {
      id: 0,
      usuario_id: '',
      gimnasio_id: this.gimnasioId,
      fecha: new Date().toISOString().split('T')[0],
      notas_generales: this.notasEntrenamiento,
      id_cliente: crypto.randomUUID(),
      creado_en: new Date().toISOString(),
      actualizado_en: new Date().toISOString(),
      series: []
    };

    this.router.navigate(['/active-workout'], {
      queryParams: {
        gimnasioId: this.gimnasioId,
        equiposIds: this.equiposSeleccionadosIds.join(','),
        datosSesion: JSON.stringify(sesion)
      }
    });
  }

  async continuarSesionAnterior(sesionId: number): Promise<void> {
    const sesionCompleta = await this.supabase.obtenerSesion(sesionId);
    if (sesionCompleta && sesionCompleta.series) {
      const equiposIds = [...new Set(sesionCompleta.series.map((s: any) => s.equipo_gimnasio_id))];

      this.router.navigate(['/active-workout'], {
        queryParams: {
          gimnasioId: this.gimnasioId,
          equiposIds: equiposIds.join(','),
          datosSesion: JSON.stringify(sesionCompleta)
        }
      });
    }
  }

  verHistorial(): void {
    this.router.navigate(['/history']);
  }

  irAtras(): void {
    this.router.navigate(['/gym-selector']);
  }
}
