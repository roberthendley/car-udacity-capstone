import { Component, OnInit } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-nav-panel',
  templateUrl: './nav-panel.component.html',
  styleUrls: ['./nav-panel.component.css']
})
export class NavPanelComponent implements OnInit {

  constructor(public auth: AuthService) { }

  ngOnInit(): void {
  }

  logout(): void {
    this.auth.logout()
  }

}
