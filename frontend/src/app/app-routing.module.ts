import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Auth0 Auth Guard
import { AuthGuard } from '@auth0/auth0-angular';

// Page Components for Routes
import { HomeComponent } from './pages/home/home.component';
import { AppContainerComponent } from './components/app-container/app-container.component';
import { ClientListComponent } from './pages/client-list/client-list.component';
import { ReportListComponent } from './pages/report-list/report-list.component';
import { ContactListComponent } from './pages/contact-list/contact-list.component';
import { Error403Component } from './pages/error403/error403.component';
import { Error404Component } from './pages/error404/error404.component';
import { ContactComponent } from './pages/contact/contact.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'app', component: AppContainerComponent, canActivateChild: [AuthGuard], children: [
  // { path: 'app', component: AppContainerComponent, children: [
    {path: 'reports', component: ReportListComponent },
    {path: 'clients', component: ClientListComponent },
    {path: 'contacts', component: ContactListComponent }, 
    {path: 'contacts/:id', component: ContactComponent}
  ]},
  { path: 'home', redirectTo: '/', pathMatch:'full'},
  { path: 'error403', component: Error403Component },
  { path: '**', component: Error404Component }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
