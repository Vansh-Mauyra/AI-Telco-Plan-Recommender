import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatExpansionModule } from '@angular/material/expansion';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-plans',
  templateUrl: './plans.component.html',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,        
    MatExpansionModule    
  ],
})
export class PlansComponent implements OnInit {

  plansByCategory: any = {};
  categories: string[] = [];

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getAllPlans().subscribe(res => {
      this.plansByCategory = res;
      this.categories = Object.keys(res);
    });
  }
}
