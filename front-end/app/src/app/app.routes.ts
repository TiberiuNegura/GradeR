import { Routes } from '@angular/router';
import { AuthComponent } from './components/auth/auth.component';
import { HomeComponent } from './components/home/home.component';
import { StudentGradeViewComponent } from './components/student-grade-view/student-grade-view.component';
import { TeacherGradeViewComponent } from './components/teacher-grade-view/teacher-grade-view.component';

export const routes: Routes = [
    { path: 'auth', component: AuthComponent },
    { path: 'home', component: HomeComponent },
    { path: 'student', component: StudentGradeViewComponent },
    { path: 'teacher', component: TeacherGradeViewComponent },
    { path: '', redirectTo: '/auth', pathMatch: 'full' },
    { path: '**', redirectTo: '/auth' },
];
