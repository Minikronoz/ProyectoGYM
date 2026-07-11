import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { appConfig } from './app/app.config';
import { addIcons } from 'ionicons';
import {
  arrowBack, arrowForward, chevronBack, chevronForward,
  chevronForwardOutline, chevronBackOutline,
  calendarOutline, documentTextOutline, barbellOutline, barbell,
  timeOutline, play, logOutOutline, businessOutline, checkmarkCircle,
  checkmarkCircleOutline, flame, chatbubbleOutline, logoGoogle,
  flashOutline, cloudOfflineOutline, add, addCircle, remove, removeCircle,
  close, save, trash, fitness, ellipsisVertical, ellipsisHorizontal
} from 'ionicons/icons';

addIcons({
  'arrow-back': arrowBack,
  'arrow-forward': arrowForward,
  'chevron-back': chevronBack,
  'chevron-forward': chevronForward,
  'chevron-forward-outline': chevronForwardOutline,
  'chevron-back-outline': chevronBackOutline,
  'calendar-outline': calendarOutline,
  'document-text-outline': documentTextOutline,
  'barbell-outline': barbellOutline,
  'barbell': barbell,
  'time-outline': timeOutline,
  'play': play,
  'log-out-outline': logOutOutline,
  'business-outline': businessOutline,
  'checkmark-circle': checkmarkCircle,
  'checkmark-circle-outline': checkmarkCircleOutline,
  'flame': flame,
  'chatbubble-outline': chatbubbleOutline,
  'logo-google': logoGoogle,
  'flash-outline': flashOutline,
  'cloud-offline-outline': cloudOfflineOutline,
  'add': add,
  'add-circle': addCircle,
  'remove': remove,
  'remove-circle': removeCircle,
  'close': close,
  'save': save,
  'trash': trash,
  'fitness': fitness,
  'ellipsis-vertical': ellipsisVertical,
  'ellipsis-horizontal': ellipsisHorizontal
});

bootstrapApplication(AppComponent, appConfig)
  .catch(err => console.log(err));
