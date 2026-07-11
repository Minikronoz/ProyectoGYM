import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ServicioSupabase } from '../../services/supabase.service';
import { IonContent, IonSpinner } from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-auth-callback',
  template: `
    <ion-content class="ion-padding">
      <div class="ion-text-center ion-padding">
        <ion-spinner name="crescent"></ion-spinner>
        <p>Iniciando sesión...</p>
      </div>
    </ion-content>
  `,
  standalone: true,
  imports: [CommonModule, IonContent, IonSpinner]
})
export class AuthCallbackPage implements OnInit {
  constructor(
    private supabase: ServicioSupabase,
    private router: Router
  ) {}

  async ngOnInit() {
    try {
      await this.supabase.procesarCallbackAuth();
    } catch (error) {
      console.error('Error de autenticación:', error);
    }

    if (this.supabase.estaAutenticado) {
      this.router.navigateByUrl('/gym-selector', { replaceUrl: true });
    } else {
      this.router.navigateByUrl('/login', { replaceUrl: true });
    }
  }
}
