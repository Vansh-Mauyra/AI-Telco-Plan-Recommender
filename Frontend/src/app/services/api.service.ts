import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class ApiService {

  private base = environment.apiBaseUrl;

  constructor(private http: HttpClient) {}

  getAllPlans() {
    return this.http.get<any>(`${this.base}/plans`);
  }

  chat(message: string, userId?: string) {
    console.log('API chat called');
    return this.http.post<any>(`${this.base}/chat`, {
      message,
      user_id: userId
    });
  }
}
