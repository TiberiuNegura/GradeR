import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RegisterModel } from '../models/RegisterModel';
import { LoginModel } from '../models/LoginModel';
import { GradeModel } from '../models/GradeModel';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public server: string = 'http://localhost:5000/api/'

  public register(data: RegisterModel) {
    return this.httpClient.post(`${this.server}register`, data);
  }

  public login(data: LoginModel) {
    return this.httpClient.post(`${this.server}login`, data);
  }

  public getSubjects(isTeacher: boolean) {
    const params = {
      id: this.getIdFromSession(),
      role: isTeacher ? 'true' : 'false'
    }
    
    return this.httpClient.post(`${this.server}subjects`, params);
  }

  public getGradesBySubject(id: number) {
    const params = {
      id: this.getIdFromSession(),
      discipline_id: id
    };

    return this.httpClient.post<GradeModel[]>(`${this.server}grades/by-discipline-student`, params);
  }

  public getAllGradesForDiscipline(subjectId: number) {
    const params = {
      id: this.getIdFromSession(),
      discipline_id: subjectId
    }

    return this.httpClient.post<GradeModel[]>(`${this.server}grades/by-discipline-teacher`, params);
  }

  public addGrade(studentId: number, grade: number, subjectId: number) {
    const params = {
      teacher_id: this.getIdFromSession(),
      student_id: studentId,
      discipline_id: subjectId,
      value: grade
    };

    return this.httpClient.post(`${this.server}grades/add`, params);
  }
  
  public updateGrade(gradeId: number, newGrade: number) {
    const params = {
      id: this.getIdFromSession(),
      value: newGrade,
      gradeId: gradeId,
      date: new Date().toISOString()
    };

    return this.httpClient.put(`${this.server}grades/${gradeId}`, params);
  }

  public deleteGrade(gradeId: number) {
    return this.httpClient.delete(`${this.server}grades/${gradeId}`);
  }

  public getAllStudentNames() {
    return this.httpClient.get<string[]>(`${this.server}students/name`);
  }

  private getIdFromSession(): number{ 
    return parseInt(localStorage.getItem('id') ?? '0', 10)
  }
}
