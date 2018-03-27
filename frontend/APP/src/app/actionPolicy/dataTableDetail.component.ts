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
        // this.initDatePicker();
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
    // public initDatePicker() {
    //     console.log(12345);
    //     const selectDateInputField: HTMLInputElement = this.elementRef.nativeElement.querySelector('#selectDate');
    //     const func = flatpickr['default'];
    //     const selectDateTP = func(selectDateInputField, {
    //         'enableTime': true,
    //         'onChange': (selectedDates, dateStr, instance) => {
    //             this.startTime = moment(dateStr + ' 00:00:00', 'YYYY-MM-DD HH:mm:ss').unix();
    //             this.endTime = moment(dateStr + ' 23:59:59', 'YYYY-MM-DD HH:mm:ss').unix();
    //             const a = _.split(dateStr, '-');
    //             // this.select_date = a[0].slice(2, 4) + '-' + a[1] + '-' + a[2];
    //             // this.outputOnChangesDate.emit(this.select_date);

    //         }
    //     });
    //     selectDateTP.setDate(this.startTime * 1000);
    // }
}
