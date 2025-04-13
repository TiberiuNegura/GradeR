import { Component, OnInit } from '@angular/core';
import { GradeModel } from '../../models/GradeModel';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-teacher-grade-view',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './teacher-grade-view.component.html',
  styleUrls: ['./teacher-grade-view.component.css']
})
export class TeacherGradeViewComponent implements OnInit {
  subjectId!: number;
  subjectName = '';
  teacher = '';
  search = '';
  grades: GradeModel[] = [];
  filteredGrades: GradeModel[] = [];
  ownsSubject: boolean = false;

  studentNames: string[] = [];

  newGrade = { studentId: '', value: '' };
  editingGradeId: number | null = null;
  updatedValue = '';

  constructor(
    private route: ActivatedRoute,
    private api: ApiService
  ) { }

  ngOnInit(): void {
    const id = this.route.snapshot.queryParamMap.get('id');
    const name = this.route.snapshot.queryParamMap.get('name');
    const teacher = this.route.snapshot.queryParamMap.get('teacher');
    const ownsSubject = this.route.snapshot.queryParamMap.get('subjectTeacher');

    if (id) this.subjectId = +id;
    if (name) this.subjectName = name;
    if (teacher) this.teacher = teacher;
    if(ownsSubject) this.ownsSubject = ownsSubject == 'true';

    this.loadGrades();
    this.loadStudentsName();

    console.log('ownsSubject?', this.ownsSubject);
  }

  loadGrades(): void {
    this.api.getAllGradesForDiscipline(this.subjectId).subscribe({
      next: (grades: any[]) => {
        const parsedGrades = grades.map(g => ({
          id: g.id,
          value: typeof g.value === 'string' ? parseFloat(g.value) : g.value,
          name: g.name,
          date: g.date,
        }));
  
        this.grades = parsedGrades;
        this.filteredGrades = parsedGrades;
      },
      error: err => console.error('Failed to load grades', err)
    });
  }
  

  loadStudentsName(): void {
    this.api.getAllStudentNames().subscribe({
      next: data => {
        this.studentNames = data;
      },
      error: err => console.error('Failed to get all students names', err)
    })
  }

  filterGrades(): void {
    // If you want to add filtering by student ID (since no name), update this accordingly
    const term = this.search.trim();
    this.filteredGrades = this.grades.filter(g =>
      g.name.toString().includes(term) || g.value.toString().includes(term)
    );
  }

  addGrade(): void {
    const studentId = parseInt(this.newGrade.studentId);
    const value = parseFloat(this.newGrade.value);

    if (!studentId || !value || isNaN(studentId) || isNaN(value)) {
      console.error('Invalid input');
      return;
    }

    this.api.addGrade(studentId, value, this.subjectId).subscribe({
      next: () => {
        this.newGrade = { studentId: '', value: '' };
        this.loadGrades();
      },
      error: err => console.error('Failed to add grade', err)
    });
  }

  startEdit(grade: GradeModel): void {
    this.editingGradeId = grade.id;
    this.updatedValue = grade.value.toString();
  }

  cancelEdit(): void {
    this.editingGradeId = null;
    this.updatedValue = '';
  }

  updateGrade(gradeId: number): void {
    const newValue = parseFloat(this.updatedValue);

    if (!newValue || isNaN(newValue)) {
      console.error('Invalid value');
      return;
    }
    console.log(newValue)
    this.api.updateGrade(gradeId, newValue).subscribe({
      next: () => {
        this.editingGradeId = null;
        this.updatedValue = '';
        this.loadGrades();
      },
      error: err => console.error('Failed to update grade', err)
    });
  }

  deleteGrade(gradeId: number): void {
    this.api.deleteGrade(gradeId).subscribe({
      next: () => this.loadGrades(),
      error: err => console.error('Failed to delete grade', err)
    });
  }
}
