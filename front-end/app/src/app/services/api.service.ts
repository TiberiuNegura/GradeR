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
      id: localStorage.getItem('id'),
      role: isTeacher ? 'true' : 'false'
    }
    
    return this.httpClient.post(`${this.server}subjects`, params);
  }

  public getGradesBySubject(id: number) {
    const params = {
      id: localStorage.getItem('id'),
      discipline_id: id
    };

    return this.httpClient.post<GradeModel[]>(`${this.server}grades/by-discipline`, params);
  }

  public getAllGradesForDiscipline(subjectId: number) {
    return this.httpClient.post(`${this.server}grades/by-discipline`, subjectId);
  }

  public addGrade(studentId: number, grade: number, subjectId: number) {
    const params = {
      id: studentId,
      discipline_id: subjectId,
      subjectValue: grade
    };

    return this.httpClient.post(`${this.server}grades/add`, params);
  }
  
  public updateGrade(gradeId: number, newGrade: number) {
    const params = {
      id: localStorage.getItem('id'),
      gradeValue: newGrade,
      gradeId: gradeId
    };

    return this.httpClient.post(`${this.server}grades/update`, params);
  }

  public deleteGrade(gradeId: number) {
    return this.httpClient.delete(`${this.server}grade/delete`);
  }
}
