import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { ApiService } from '../../services/api.service';

interface Message {
  from: 'user' | 'bot';
  text: string;
  plans?: any[];
}

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,          
    MatButtonModule,
    MatInputModule,
    MatCardModule
  ],
})
export class ChatComponent {

  input = '';
  messages: Message[] = [];

  constructor(private api: ApiService) {}

  send() {
    if (!this.input.trim()) return;

    this.messages.push({ from: 'user', text: this.input });

    this.api.chat(this.input).subscribe(res => {
      this.messages.push({
        from: 'bot',
        text: res.answer,
        plans: res.plans
      });
    });

    this.input = '';
  }
}
