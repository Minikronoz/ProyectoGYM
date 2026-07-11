import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login.page').then(m => m.LoginPage)
  },
  {
    path: 'auth/callback',
    loadComponent: () => import('./pages/auth-callback/auth-callback.page').then(m => m.AuthCallbackPage)
  },
  {
    path: 'gym-selector',
    loadComponent: () => import('./pages/gym-selector/gym-selector.page').then(m => m.GimnasioSelectorPage)
  },
  {
    path: 'workout-day',
    loadComponent: () => import('./pages/workout-day/workout-day.page').then(m => m.DiaEntrenamientoPage)
  },
  {
    path: 'active-workout',
    loadComponent: () => import('./pages/active-workout/active-workout.page').then(m => m.EntrenamientoActivoPage)
  },
  {
    path: 'history',
    loadComponent: () => import('./pages/history/history.page').then(m => m.HistorialPage)
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];
