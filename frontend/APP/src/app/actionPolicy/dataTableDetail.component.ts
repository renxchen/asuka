import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'data-table-detail',
    templateUrl: 'dataTableDetail.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class DataTableDetailComponent implements OnInit, AfterViewInit {
    apiPrefix: any = '/v1';
    title: string;
    id: number;

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        public bsModalRef: BsModalRef
    ) {}

    ngOnInit(){
        this.httpClient.setUrl(this.apiPrefix);


    }

    ngAfterViewInit() {
        // this.initButtons();
        setTimeout(() => {

            // $('#validPeriod').hide();
            // $('#dataSchedule').hide();
            // if(this.id == -1){
            //     this.getOsTypes();
            //     this.setInitSelect();
            //     $('button.btn-danger').hide();
            // } else {
            //     this.getDetailById(this.id);
            // }
        },0);
    }



}