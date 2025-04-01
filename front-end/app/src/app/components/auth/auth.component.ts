import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

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
  
  constructor(private router: Router) {}

  switchForm(formType: 'login' | 'register') {
    this.activeForm = formType;
  }

  onSubmit(formType: string, formData: any) {
    console.log(`${formType} form submitted:`, formData);
    // to be implemented
    this.router.navigate(['/home']);
  }
}
