import { Injectable } from '@angular/core';
import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable} from 'rxjs'
import { Contact } from '../models/contact.model';
import { ApiService } from '../api.service'

@Injectable({
  providedIn: 'root'
})
export class ContactListResolverService implements Resolve<Contact[]>{

  constructor(private api:ApiService) { }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Contact[]> {
    return this.api.get_contacts()
  }

}
