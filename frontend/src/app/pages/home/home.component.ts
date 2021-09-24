import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '@auth0/auth0-angular';
import { switchMap } from 'rxjs/operators'
import { from } from 'rxjs'

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  constructor(private auth: AuthService,
              private router: Router
    ) { }

  ngOnInit(): void {
  }

  login(): void {
        this.auth.loginWithRedirect({appState: {target: '/app/clients'}})
  }
}
