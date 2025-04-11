import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { SubjectModel } from '../../models/SubjectModel';
import { catchError, forkJoin, map, of } from 'rxjs';
import { GradeModel } from '../../models/GradeModel';

interface SubjectWithGrades extends SubjectModel {
  grades: number[];
  average: number;
}

@Component({
  selector: 'app-home',
  imports: [
    FormsModule,
    CommonModule
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  isTeacher: boolean = true;

  allSubjects: SubjectModel[] = [];
  averageScore: number = 0;
  isLoading: boolean = true;
  subjectAverages: { [id: number]: number } = {};
  studentSubjectsWithGrades: SubjectWithGrades[] = []

  constructor(
    private router: Router,
    private route: ActivatedRoute,
    private api: ApiService
  ) { }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.isTeacher = params['role'] === 'true';
      this.fetchSubjects();
    });
  }

  fetchSubjects(): void {
    this.isLoading = true;
    this.api.getSubjects(this.isTeacher).subscribe({
      next: (data: any) => {
        this.allSubjects = data.subjects.map((s: any) => ({
          name: s.name,
          teacher: s.teacher,
          ownsSubject: s.owns_discipline,
          idDiscipline: s.id_discipline
        }));
        this.isLoading = false;

        if (!this.isTeacher) this.loadAverageScore();
      },
      error: err => {
        console.error('Failed to fetch subjects:', err);
        this.isLoading = false;
      }
    });
  }

  get studentSubjects(): SubjectModel[] {
    return (this.allSubjects || []).filter(subj => !subj.ownsSubject);
  }

  get teacherSubjects(): SubjectModel[] {
    console.log(this.allSubjects)
    return this.allSubjects;
  }

  loadAverageScore(): void {
    const gradeRequests = this.studentSubjects.map(subj =>
      this.api.getGradesBySubject(subj.idDiscipline).pipe(
        catchError(() => of([] as GradeModel[])),
        map((grades: GradeModel[]) => {
          // Log grade values and their types for debugging
          grades.forEach(g => {
            console.log(`Grade for subject ${subj.name}: value = ${g.value}, type = ${typeof g.value}`);
          });
          // Convert all grade values to numbers (in case they're strings)
          const gradeValues = grades.map(g => {
            let value = g.value;
            if (typeof value === 'string') {
              value = parseFloat(value);
            }
            return value;
          });
          return { subject: subj, grades: gradeValues };
        })
      )
    );

    forkJoin(gradeRequests).subscribe(subjectResults => {
      const subjectsWithAverages: SubjectWithGrades[] = subjectResults.map(({ subject, grades }) => {
        // Compute per-subject average
        const average = grades.length ? +(grades.reduce((a, b) => a + b, 0) / grades.length).toFixed(2) : 0;
        return { ...subject, grades, average };
      });

      // Save the computed per-subject averages into the component's property
      this.studentSubjectsWithGrades = subjectsWithAverages;

      // For overall semester average, average all grade numbers across subjects
      const allGrades = subjectsWithAverages.flatMap(subj => subj.grades);
      const totalAvg = allGrades.length ? +(allGrades.reduce((a, b) => a + b, 0) / allGrades.length).toFixed(2) : 0;
      this.averageScore = totalAvg;
    });
  }

  get standing(): { text: string; color: string } {
    const avg = this.averageScore;
    if (avg >= 9) return { text: 'Very Good', color: '#00c853' };
    if (avg >= 7) return { text: 'Good', color: '#ffc107' };
    return { text: 'Bad', color: '#f44336' };
  }

  goToSubject(subject: SubjectModel | SubjectWithGrades): void {
    if (!this.isTeacher) {
      this.router.navigate(['/student'], {
        queryParams: {
          id: subject.idDiscipline,
          name: subject.name,
          teacher: subject.teacher
        }
      });
    } else {
      this.router.navigate(['/teacher'], {
        queryParams: {
          id: subject.idDiscipline,
          name: subject.name,
          teacher: subject.teacher
        }
      });
    }
  }

}
