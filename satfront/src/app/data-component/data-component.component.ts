import { Component, OnInit } from '@angular/core';
import { Apollo, gql } from 'apollo-angular';

const GET_DATA_QUERY = gql`
    query {
        allSatellites {
            name
            satId
            tleDate
            line1
            line2
        }
    }
`;

interface QueryResponse {
  allSatellites: Satellite[];
}

interface Satellite {
  name: string;
  satId: number;
  tleDate: string;
  line1: string;
  line2: string;
}

@Component({
  selector: 'app-data-component',
  templateUrl: './data-component.component.html',
  styleUrl: './data-component.component.css'
})
export class DataComponentComponent implements OnInit {
  items: Satellite[] = [];
  loading = true;
  error: any;

  constructor(private apollo: Apollo) {}

  ngOnInit(): void {
    this.apollo.watchQuery<QueryResponse>({
      query: GET_DATA_QUERY
    }).valueChanges.subscribe({
      next: (result) => {
        if (result.data && result.data.allSatellites) {
          console.log(result.data.allSatellites);
		  this.items = result.data.allSatellites;
        }
        this.loading = result.loading;
      },
      error: (error) => {
        this.error = error;
        this.loading = false;
      }
    });
  }
}
