import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ServicioSupabase, EquipoGimnasio, SerieEjercicio, SesionEntrenamiento } from '../../services/supabase.service';
import { CommonModule } from '@angular/common';
import {
  IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon,
  IonLoading, IonButtons, IonAlert, IonLabel
} from '@ionic/angular/standalone';

interface EquipoConSeries {
  equipo: EquipoGimnasio;
  series: SerieEjercicio[];
  numeroSerieActual: number;
  ultimaSerie: SerieEjercicio | null;
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
export class EntrenamientoActivoPage implements OnInit {
  gimnasioId!: number;
  equiposIds: number[] = [];
  sesion!: SesionEntrenamiento;
  equiposConSeries: EquipoConSeries[] = [];
  indiceEquipoActual = 0;
  guardando = false;
  mostrarConfirmarFinalizar = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private supabase: ServicioSupabase
  ) {}

  async ngOnInit(): Promise<void> {
    this.gimnasioId = Number(this.route.snapshot.queryParams['gimnasioId']);
    const equiposIdsStr = this.route.snapshot.queryParams['equiposIds'];
    const datosSesionStr = this.route.snapshot.queryParams['datosSesion'];

    this.equiposIds = equiposIdsStr.split(',').map(Number);
    this.sesion = JSON.parse(datosSesionStr);

    await this.cargarEquiposConUltimasSeries();
  }

  async cargarEquiposConUltimasSeries(): Promise<void> {
    const equipos = await this.supabase.obtenerEquipos(this.gimnasioId);
    const equiposSeleccionados = equipos.filter(eq => this.equiposIds.includes(eq.id));

    this.equiposConSeries = [];

    for (const eq of equiposSeleccionados) {
      const ultimaSerie = await this.supabase.obtenerUltimaSerieParaEquipo(eq.id);
      this.equiposConSeries.push({
        equipo: eq,
        series: [],
        numeroSerieActual: 1,
        ultimaSerie: ultimaSerie
      });
    }
  }

  get equipoActual(): EquipoConSeries | null {
    return this.equiposConSeries[this.indiceEquipoActual] || null;
  }

  get totalSeries(): number {
    return this.equiposConSeries.reduce((acc, eq) => acc + eq.series.length, 0);
  }

  agregarSerie(indiceEquipo: number, peso: number, reps: number, esFalla: boolean = false, notas: string = ''): void {
    const eq = this.equiposConSeries[indiceEquipo];
    const nuevaSerie: SerieEjercicio = {
      id: 0,
      sesion_entrenamiento_id: 0,
      equipo_gimnasio_id: eq.equipo.id,
      numero_serie: eq.numeroSerieActual,
      tipo_serie: esFalla ? 'falla' : 'normal',
      valor_peso: peso,
      cantidad_reps: reps,
      hasta_falla: esFalla,
      notas_serie: notas,
      id_cliente: crypto.randomUUID(),
      creado_en: new Date().toISOString()
    };

    eq.series.push(nuevaSerie);
    eq.numeroSerieActual++;
  }

  irAEquipo(indice: number): void {
    this.indiceEquipoActual = indice;
  }

  irSiguiente(): void {
    if (this.indiceEquipoActual < this.equiposConSeries.length - 1) {
      this.indiceEquipoActual++;
    }
  }

  irAnterior(): void {
    if (this.indiceEquipoActual > 0) {
      this.indiceEquipoActual--;
    }
  }

  obtenerDisplaySerie(set: SerieEjercicio): string {
    const unidad = set.tipo_unidad || this.equipoActual?.equipo.tipo_unidad || 'kg';
    return `${set.valor_peso}${unidad} × ${set.cantidad_reps}`;
  }

  obtenerDisplayUltimaSerie(): string {
    const ultima = this.equipoActual?.ultimaSerie;
    if (!ultima) return '';
    const unidad = ultima.tipo_unidad || this.equipoActual?.equipo.tipo_unidad || 'kg';
    return `Última: ${ultima.valor_peso}${unidad} × ${ultima.cantidad_reps}`;
  }

  async finalizarEntrenamiento(): Promise<void> {
    this.guardando = true;
    this.mostrarConfirmarFinalizar = false;

    try {
      const sesionCreada = await this.supabase.crearSesion({
        usuario_id: this.supabase.usuario?.id || '',
        gimnasio_id: this.gimnasioId,
        fecha: this.sesion.fecha,
        notas_generales: this.sesion.notas_generales,
        id_cliente: this.sesion.id_cliente
      });

      for (const eq of this.equiposConSeries) {
        for (const serie of eq.series) {
          await this.supabase.crearSerie({
            sesion_entrenamiento_id: sesionCreada.id,
            equipo_gimnasio_id: serie.equipo_gimnasio_id,
            numero_serie: serie.numero_serie,
            tipo_serie: serie.tipo_serie,
            valor_peso: serie.valor_peso,
            cantidad_reps: serie.cantidad_reps,
            hasta_falla: serie.hasta_falla,
            notas_serie: serie.notas_serie,
            id_cliente: serie.id_cliente
          });
        }
      }

      this.router.navigate(['/gym-selector']);
    } catch (error) {
      console.error('Error al guardar entrenamiento:', error);
      this.router.navigate(['/gym-selector']);
    } finally {
      this.guardando = false;
    }
  }

  irAtras(): void {
    if (this.totalSeries > 0) {
      this.mostrarConfirmarFinalizar = true;
    } else {
      this.router.navigate(['/workout-day'], {
        queryParams: { gimnasioId: this.gimnasioId }
      });
    }
  }

  get cancelarBotones() {
    return [
      { text: 'Cancelar', role: 'cancel', handler: () => this.mostrarConfirmarFinalizar = false },
      { text: 'Descartar', role: 'destructive', handler: () => this.router.navigate(['/workout-day'], { queryParams: { gimnasioId: this.gimnasioId } }) },
      { text: 'Guardar', handler: () => this.finalizarEntrenamiento() }
    ];
  }

  cancelarFinalizar(): void {
    this.mostrarConfirmarFinalizar = false;
  }

  descartarYSalir(): void {
    this.router.navigate(['/workout-day'], {
      queryParams: { gimnasioId: this.gimnasioId }
    });
  }
}
