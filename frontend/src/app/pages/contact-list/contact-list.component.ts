import { Component, OnInit } from '@angular/core';
import { Contact } from 'src/app/models/contact.model';
import { EMPTY, Observable } from 'rxjs';
import { ApiService } from 'src/app/api.service';

@Component({
  selector: 'app-contact-list',
  templateUrl: './contact-list.component.html',
  styleUrls: ['./contact-list.component.css']
})
export class ContactListComponent implements OnInit {

  contacts:Observable<Contact[]> = EMPTY;

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.contacts = this.api.get_contacts()
  }


}
