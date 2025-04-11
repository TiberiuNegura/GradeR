import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { LoginModel } from '../../models/LoginModel';
import { RegisterModel } from '../../models/RegisterModel';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-auth',
  imports: [
    CommonModule,
    FormsModule
  ],
  templateUrl: './auth.component.html',
  styleUrl: './auth.component.css'
})
export class AuthComponent {
  activeForm: 'login' | 'register' = 'login';

  loginModel: LoginModel = {
    email: '',
    password: ''
  };

  registerModel: RegisterModel = {
    lastName: '',
    firstName: '',
    email: '',
    password: '',
    role: false,
  };

  confirmPwd: string = '';
  passwordMismatch: boolean = false;


  constructor(
    private router: Router,
    private api: ApiService
  ) { }

  switchForm(formType: 'login' | 'register') {
    this.activeForm = formType;
  }

  onSubmit() {
    console.log(`${this.activeForm} form submitted`);

    if (this.activeForm == 'login') {
      console.log(`email: ${this.loginModel.email}, pwd; ${this.loginModel.password}`);
      this.api.login(this.loginModel)
        .subscribe({
          next: (data: any) => {
            let isTeacher: boolean = data.isTeacher == 'true';
            localStorage.setItem('id', data.userId);
            this.router.navigate(['/home'], { queryParams: { role: isTeacher } });
          },
          error: (err) => {
            console.error(err);
          }
        });
    } else {
      if (this.registerModel.password != this.confirmPwd) {
        this.passwordMismatch = true;
        console.error("passwords do not match");
        return;
      } else {
        this.passwordMismatch = false;
      }

      this.api.register(this.registerModel)
        .subscribe({
          next: (data: any) => {
            this.router.navigate(['/home'], { queryParams: { role: this.registerModel.role } });
            localStorage.setItem('id', data.userId)
          },
          error: (err) => {
            console.error(err);
          }

        });
    }
  }
}
