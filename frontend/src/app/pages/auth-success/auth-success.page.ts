import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Storage } from '@ionic/storage-angular';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-auth-success',
  template: `
    <ion-content class="ion-padding">
      <div class="ion-text-center ion-padding">
        <ion-spinner name="crescent"></ion-spinner>
        <p>Iniciando sesión...</p>
      </div>
    </ion-content>
  `,
  standalone: true,
  imports: [CommonModule, IonicModule]
})
export class AuthSuccessPage implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private storage: Storage
  ) {}

  async ngOnInit() {
    const token = this.route.snapshot.queryParamMap.get('token');
    const error = this.route.snapshot.queryParamMap.get('error');

    if (token) {
      await this.storage.set('access_token', token);
      this.router.navigateByUrl('/gym-selector', { replaceUrl: true });
    } else if (error) {
      this.router.navigateByUrl('/login', { replaceUrl: true });
    } else {
      this.router.navigateByUrl('/login', { replaceUrl: true });
    }
  }
}
