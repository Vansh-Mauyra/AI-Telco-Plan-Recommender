import { Component } from '@angular/core';import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, MatToolbarModule, MatButtonModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {

  constructor(private router: Router) {}

  // navigate to plans page
  goToPlans() {
    this.router.navigate(['/plans']);
  }

  // navigate to chats page
  goToChat(){
    this.router.navigate(['/chat']);
  }
}