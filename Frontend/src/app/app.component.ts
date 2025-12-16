import { Component, OnInit } from '@angular/core';
import { RouterOutlet, Router, RouterLink, RouterLinkActive, NavigationEnd } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    MatToolbarModule,
    MatButtonModule,
    RouterLink,        // <-- Required for routerLink
    RouterLinkActive   // <-- Required for routerLinkActive
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  isDarkMode = false;
  isChatPage = false;

  constructor(private router: Router) {}

  ngOnInit(): void {
    // Restore theme
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      this.enableDarkMode();
    }

    // Detect current route (for chat-only UI changes)
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        this.isChatPage = event.urlAfterRedirects.includes('/chat');
      }
    });
  }

  toggleTheme(): void {
    this.isDarkMode ? this.disableDarkMode() : this.enableDarkMode();
  }

  private enableDarkMode(): void {
    document.body.classList.add('dark-theme');
    localStorage.setItem('theme', 'dark');
    this.isDarkMode = true;
  }

  private disableDarkMode(): void {
    document.body.classList.remove('dark-theme');
    localStorage.setItem('theme', 'light');
    this.isDarkMode = false;
  }
}
