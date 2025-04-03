import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { RegisterModel } from '../models/RegisterModel';
import { LoginModel } from '../models/LoginModel';

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

}
