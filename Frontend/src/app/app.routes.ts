import { Routes } from '@angular/router';
import { ChatComponent } from './pages/chat/chat.component';
import { PlansComponent } from './pages/plans/plans.component';
import { AppComponent } from './app.component';

export const routes: Routes = [
  { path: '', redirectTo: 'chat', pathMatch: 'full' },
  { path: 'chat', component: ChatComponent },
  { path: 'plans', component: PlansComponent }
];
