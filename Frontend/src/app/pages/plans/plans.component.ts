import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ApiService } from '../../services/api.service';
import { Plan } from '../../../model/plan.model';

@Component({
  selector: 'app-plans',
  templateUrl: './plans.component.html',
  styleUrls: ['./plans.component.css'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule
  ],
  encapsulation: ViewEncapsulation.None
})
export class PlansComponent implements OnInit {
  plansByCategory: { [category: string]: Plan[] } = {};
  categories: string[] = [];
  selectedCategory: string | null = null;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getAllPlans().subscribe(res => {
      this.plansByCategory = res;
      this.categories = Object.keys(res);
      this.selectedCategory = this.categories[0]; // default selected
    });
  }

  selectCategory(category: string) {
    this.selectedCategory = category;
  }
}
