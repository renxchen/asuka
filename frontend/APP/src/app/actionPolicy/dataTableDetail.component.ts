import { Component, OnInit, AfterViewInit, ElementRef } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';
import * as moment from 'moment';
import * as flatpickr from 'flatpickr';

@Component({
    selector: 'data-table-detail',
    templateUrl: 'dataTableDetail.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class DataTableDetailComponent implements OnInit, AfterViewInit {
    apiPrefix: any = '/v1';
    title: string;
    id: number;
    startTime: any;
    endTime: any;

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        public bsModalRef: BsModalRef,
        public elementRef: ElementRef
    ) { }

    ngOnInit() {
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
        }, 0);
    }
}
