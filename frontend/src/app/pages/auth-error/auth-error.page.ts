import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-auth-error',
  template: `
    <ion-content class="ion-padding">
      <div class="ion-text-center ion-padding">
        <ion-icon name="alert-circle-outline" size="large" color="danger"></ion-icon>
        <h2>Error de autenticación</h2>
        <p>No se pudo iniciar sesión con Google.</p>
        <ion-button expand="block" routerLink="/login">
          Volver al login
        </ion-button>
      </div>
    </ion-content>
  `,
  standalone: true,
  imports: [CommonModule, IonicModule]
})
export class AuthErrorPage {}
