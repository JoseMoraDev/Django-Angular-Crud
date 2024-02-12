import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Emitters } from '../emitters/emitters';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit{
  message = 'You are not logged in';

  constructor(
    private http: HttpClient
  ){}



  ngOnInit(): void {

      this.http.get('http://localhost:8000/api/user', {withCredentials: true}).subscribe(
        {

          next: (res: any) => (
            console.log(res), this.message = `Hi ${res.name}`,
            Emitters.authEmitter.emit(true)
            ),

          error: (error: any) => (
            console.log(error),
            this.message = 'You are not logged in',
            Emitters.authEmitter.emit(false)
            )

        }
      );
  }
}
