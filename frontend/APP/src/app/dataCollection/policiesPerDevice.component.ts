import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';

@Component({
    selector: 'policies-per-device',
    templateUrl: 'policiesPerDevice.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class PoliciesPerDeviceComponent implements OnInit, AfterViewInit {

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
    ) {}

    ngOnInit() {
    }

    ngAfterViewInit() {
    }

}