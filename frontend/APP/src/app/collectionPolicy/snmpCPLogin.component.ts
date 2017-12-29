import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';

@Component({
    selector: 'snmp-login',
    templateUrl: 'snmpCPLogin.component.html',
    styleUrls: ['collectionPolicy.component.less']
})

export class SNMPCPLoginComponent implements OnInit, AfterViewInit {
    ngOnInit() {
    }
    ngAfterViewInit() {
    }
    public cPLogin() {}
}
