import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-grade-card',
  imports: [
    FormsModule,
    CommonModule
  ],
  templateUrl: './grade-card.component.html',
  styleUrl: './grade-card.component.css'
})
export class GradeCardComponent {
  @Input() subjectName!: string;
  @Input() value!: number;
  @Input() teacher!: string;
  @Input() date!: string;

  get gradeClass(): string {
    if (this.value >= 9) return 'grade-a';
    if (this.value >= 7) return 'grade-b';
    return 'grade-c';
  }
}
