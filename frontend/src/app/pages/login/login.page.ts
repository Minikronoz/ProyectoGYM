import { Component } from '@angular/core';
import { ServicioSupabase } from '../../services/supabase.service';
import { IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon, IonList, IonItem, IonLabel } from '@ionic/angular/standalone';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [IonHeader, IonToolbar, IonTitle, IonContent, IonButton, IonIcon, IonList, IonItem, IonLabel]
})
export class LoginPage {
  constructor(private supabase: ServicioSupabase) {}

  async iniciarSesionConGoogle(): Promise<void> {
    await this.supabase.iniciarSesionConGoogle();
  }
}
