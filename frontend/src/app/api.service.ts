import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { switchMap, tap, catchError } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Client, ClientContact } from './models/client.model';
import { Contact } from './models/contact.model';
import { APIResponse } from './models/api_response.model'


@Injectable({
  providedIn: 'root'
})
export class ApiService {

  API_URL = environment.api.host + '/api';
  constructor(private http: HttpClient) { }

  get_contacts(contact_type?: 'other' | 'clientmanager' | 'consultant', searchTerm?: string): Observable<Contact[]> {

    return this.http.get<APIResponse>(`${this.API_URL}/contacts`, { observe: 'body' }).pipe(
      catchError(this.error_handler),
      switchMap(body => of<Contact[]>(body['data']))
    )
  }

  get_contact(contact_id: number): Observable<Contact> {

    return this.http.get<APIResponse>(`${this.API_URL}/contacts/${contact_id}`, { observe: 'body' }).pipe(
      catchError(this.error_handler),
      switchMap(body => of<Contact>(body['data']))
    )
  }

  add_contact(contact: Contact): Observable<Contact> {

    return this.http.get<APIResponse>(`${this.API_URL}/contacts`, { observe: 'body' }).pipe(
      catchError(this.error_handler),
      switchMap(body => of<Contact>(body['data']))
    )

  }

  get_clients(searchTerm?: string): Observable<Client[]> {

    return this.http.get<APIResponse>(`${this.API_URL}/clients`, { observe: 'body' }).pipe(
      catchError(this.error_handler),
      switchMap(body => of<Client[]>(body['data']))
    )
  }

  error_handler(error_response: HttpErrorResponse) {
    if (error_response.error instanceof ErrorEvent) {
      console.error('Client Error: ', error_response.message)
    } else {
      console.error('Server Error: ', error_response)
    }
    return throwError("An error has been encountered by the application and has been logged. Please try again later.")
  }

}
