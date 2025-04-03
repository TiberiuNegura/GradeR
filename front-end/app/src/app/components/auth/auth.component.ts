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
          next: () => {
            // i need to query user's role here
            this.router.navigate(['/home'], { queryParams: { role: false } });
          },
          error: (err) => {
            console.error(err);
            this.router.navigate(['/home'], { queryParams: { role: false } });
          }

        });
    } else {
      if (this.registerModel.password != this.confirmPwd) {
        console.error("passwords do not match");
      }
      console.log(
        `email: ${this.registerModel.email}\n
        pwd: ${this.registerModel.password}\n
        first name: ${this.registerModel.firstName}\n
        last name: ${this.registerModel.lastName}\n
        role: ${this.registerModel.role}
        `);
      this.api.register(this.registerModel)
        .subscribe({
          next: () => {
            this.router.navigate(['/home']);
            this.router.navigate(['/home'], { queryParams: { role: this.registerModel.role } });

          },
          error: (err) => {
            console.error(err);
            this.router.navigate(['/home'], { queryParams: { role: this.registerModel.role } });
          }

        });
    }

    // untill the backend is full up
  }
}
