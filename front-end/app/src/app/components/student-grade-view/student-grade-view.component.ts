import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { CommonModule } from '@angular/common';
import { GradeCardComponent } from '../grade-card/grade-card.component';

@Component({
  selector: 'app-student-grade-view',
  imports: [
    CommonModule,
    GradeCardComponent
  ],
  templateUrl: './student-grade-view.component.html',
  styleUrl: './student-grade-view.component.css'
})
export class StudentGradeViewComponent implements OnInit {
  subjectId!: number;
  subjectName = '';
  teacher = '';
  grades: { value: number, date: string }[] = [];

  constructor(
    private route: ActivatedRoute,
    private api: ApiService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.queryParamMap.get('id');
    const name = this.route.snapshot.queryParamMap.get('name');
    const teacher = this.route.snapshot.queryParamMap.get('teacher');

    if (id) this.subjectId = +id;
    if (name) this.subjectName = name;
    if (teacher) this.teacher = teacher;

    this.loadGrades();
  }

  loadGrades(): void {
    const userId = localStorage.getItem('id');
    this.api.getGradesBySubject(this.subjectId).subscribe({
      next: (data: any) => {
        this.grades = data.map((g: any) => ({ value: +g.value, date: g.date }));
      },
      error: err => console.error('Failed to load grades', err)
    });
  }
}
