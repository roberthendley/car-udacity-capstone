import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-app-container',
  templateUrl: './app-container.component.html',
  styleUrls: ['./app-container.component.css']
})
export class AppContainerComponent implements OnInit {

  constructor(public authService: AuthService) { }

  ngOnInit(): void {
  }

  logout(): void {
    this.authService.logout()
  }

}
