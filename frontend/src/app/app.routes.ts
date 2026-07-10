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
    path: 'gym-selector',
    loadComponent: () => import('./pages/gym-selector/gym-selector.page').then(m => m.GymSelectorPage)
  },
  {
    path: 'workout-day',
    loadComponent: () => import('./pages/workout-day/workout-day.page').then(m => m.WorkoutDayPage)
  },
  {
    path: 'active-workout',
    loadComponent: () => import('./pages/active-workout/active-workout.page').then(m => m.ActiveWorkoutPage)
  },
  {
    path: 'history',
    loadComponent: () => import('./pages/history/history.page').then(m => m.HistoryPage)
  },
  {
    path: 'auth/success',
    loadComponent: () => import('./pages/auth-success/auth-success.page').then(m => m.AuthSuccessPage)
  },
  {
    path: 'auth/error',
    loadComponent: () => import('./pages/auth-error/auth-error.page').then(m => m.AuthErrorPage)
  },
  {
    path: '**',
    redirectTo: 'login'
  }
];
