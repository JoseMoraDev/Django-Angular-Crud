import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormGroup, FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    HttpClientModule
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  form: FormGroup

  constructor(
    private formBuilder: FormBuilder,
    private http: HttpClient,
    private router: Router
  ){}

  ngOnInit(): void{
    this.form = this.formBuilder.group(
      {
        email: '',
        password: ''
      }
    )
  }

  submit(){
    this.http.post(
      'http://localhost:8000/api/login/',
      this.form.getRawValue(), { withCredentials: true} //! gets cookies from backend
    ).subscribe(
      () => this.router.navigate(['/'])
    )
  }
}
