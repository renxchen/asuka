import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'data-table-login',
    templateUrl: 'dataTableLogin.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class DataTableLoginComponent implements OnInit, AfterViewInit {

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        // public bsModalRef: BsModalRef
    ) {}

    ngOnInit(){

    }

    ngAfterViewInit() {

    }
}