import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './pages/home/home.component';
import { ReportListComponent } from './pages/report-list/report-list.component';
import { ReportComponent } from './pages/report/report.component';
import { ClientListComponent } from './pages/client-list/client-list.component';
import { ClientComponent } from './pages/client/client.component';
import { ContactListComponent } from './pages/contact-list/contact-list.component';
import { ContactComponent } from './pages/contact/contact.component';
import { environment as env } from '../environments/environment'
import { AuthModule, AuthHttpInterceptor } from '@auth0/auth0-angular';
import { Error403Component } from './pages/error403/error403.component';
import { Error404Component } from './pages/error404/error404.component';
import { AppContainerComponent } from './components/app-container/app-container.component';
import { NavPanelComponent } from './components/nav-panel/nav-panel.component'

// Services
import { ApiService } from './api.service'


@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ReportListComponent,
    ReportComponent,
    ClientListComponent,
    ClientComponent,
    ContactListComponent,
    ContactComponent,
    Error403Component,
    Error404Component,
    AppContainerComponent,
    NavPanelComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    AuthModule.forRoot({
      ... env.auth
    })
  ],
  providers: [
    ApiService,
    { provide: HTTP_INTERCEPTORS, useClass: AuthHttpInterceptor, multi: true },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
