import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';

@Component({
    selector: 'snmp-edit',
    templateUrl: 'snmpCPEdit.component.html',
    styleUrls: ['collectionPolicy.component.less']
})

export class SNMPCPEditComponent implements OnInit, AfterViewInit {
    constructor() {
    }
    ngOnInit() {
        console.log('snmp');
    }
    ngAfterViewInit() {
    }
}
