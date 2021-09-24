import { Component, OnInit } from '@angular/core';
import { EMPTY, Observable } from 'rxjs';
import { ApiService } from 'src/app/api.service';
import { Client } from 'src/app/models/client.model';

@Component({
  selector: 'app-client-list',
  templateUrl: './client-list.component.html',
  styleUrls: ['./client-list.component.css']
})
export class ClientListComponent implements OnInit {

  clients:Observable<Client[]> = EMPTY;

  constructor(private api: ApiService) { }

  ngOnInit(): void {
    this.clients = this.api.get_clients()
  }
}
