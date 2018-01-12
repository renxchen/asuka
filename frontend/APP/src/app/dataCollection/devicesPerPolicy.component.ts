import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';

@Component({
    selector: 'devices-per-policy',
    templateUrl: 'devicesPerPolicy.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DevicesPerPolicyComponent implements OnInit, AfterViewInit {

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
    ) {}

    ngOnInit() {
    }

    ngAfterViewInit() {
    }

}