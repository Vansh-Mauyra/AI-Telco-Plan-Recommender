import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { ApiService } from '../../services/api.service';
import { Plan } from '../../../model/plan.model';
import { catchError } from 'rxjs';
import { of } from 'rxjs';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatCardModule, MatInputModule, MatButtonModule],
  templateUrl: './chat.component.html'
  
})

export class ChatComponent {
  input = '';
  messages: { type: 'user' | 'bot'; text: string }[] = [];
  loading = false;
  

  constructor(private api: ApiService) {}

  sendMessage() {
    const msg = this.input.trim();
    if (!msg) return;

    // Add user message
    this.messages.push({ type: 'user', text: msg });
    this.input = '';
    this.loading = true;

    // Call backend
    this.api.chat(msg).pipe(
      catchError(err => {
        console.error(err);
        this.messages.push({ type: 'bot', text: 'Error contacting server.' });
        this.loading = false;
        return of(null);
      })
    ).subscribe(res => {
      if (res) {
      // Combine answer + plans in a single bot message
      let botText = 'Here’s what I found to help you:';
      if (res.plans && res.plans.length) {
        const planText = (res.plans as Plan[])
          .map(p => `${p.plan_name} - ₹${p.monthly_fee}`)
          .join('\n');
        botText = `\n\nRecommended Plans:\n${planText}`;
      }

      this.messages.push({ type: 'bot', text: botText });
    }
    this.loading = false;
    });
  }
}
