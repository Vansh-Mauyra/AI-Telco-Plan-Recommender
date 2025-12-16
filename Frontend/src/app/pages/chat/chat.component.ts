import {
  Component,
  ViewChild,
  ElementRef,
  AfterViewChecked,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ApiService } from '../../services/api.service';
import { Plan } from '../../../model/plan.model';
import { catchError, timeout, of } from 'rxjs';

@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [CommonModule, FormsModule, MatCardModule, MatButtonModule],
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent implements AfterViewChecked {
  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

  input = '';
  messages: { type: 'user' | 'bot'; text: string }[] = [
    { type: 'bot', text: 'Welcome! How can I help you today?' },
  ];
  loading = false;
  isInitial = true;

  constructor(private api: ApiService) {}

  ngAfterViewChecked() {
    if (this.isInitial) {
      this.scrollToBottom();
    }
  }

  sendMessage() {
    const msg = this.input.trim();
    if (!msg) return;

    if (this.isInitial) {
      this.isInitial = false;
    }

    // Add user message
    this.messages.push({ type: 'user', text: msg });
    this.input = '';
    this.loading = true;

    // Call backend
    this.api
      .chat(msg)
      .pipe(
        timeout(10000),
        catchError((err) => {
          console.error(err);
          this.messages.push({ type: 'bot', text: 'Error contacting server.' });
          this.loading = false;
          return of(null);
        })
      )
      .subscribe((res) => {
        if (res) {
          let botText = '';

          if (res.type === 'GENERIC') {
            // Generic / FAQ / chit-chat
            botText = res.answer;
          } else if (res.type === 'RECOMMENDATION') {
            // Recommendation flow
            botText = 'Here’s what I found to help you:';

            if (res.plans && res.plans.length) {
              const planText = (res.plans as Plan[])
                .map((p) => `${p.plan_name} - ₹${p.monthly_fee ?? p.price}`)
                .join('\n');

              botText += `\n\nRecommended Plans:\n${planText}`;
            }
          }
          this.messages.push({ type: 'bot', text: botText });
        }
        this.loading = false;
      });
  }

  private scrollToBottom() {
    try {
      this.messagesContainer.nativeElement.scrollTop =
        this.messagesContainer.nativeElement.scrollHeight;
    } catch {}
  }
}
