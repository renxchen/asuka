import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'action-policy-view',
    templateUrl: 'actionPolicyView.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class ActionPolicyViewComponent implements OnInit, AfterViewInit {

    constructor(
        private modalService: BsModalService,
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