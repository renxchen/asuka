import { Component, OnInit, AfterViewInit } from '@angular/core';
import { NgClass } from '@angular/common';
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
    apiPrefix: any = '/v1';
    title: string;



    buttonDisable1: string = "";
    buttonDisable2: string = "disabled";
    buttonDisable3: string = "disabled";
    buttonDisable4: string = "disabled";

    buttonClass1: any;
    buttonClass2: any;
    buttonClass3: any;
    buttonClass4: any;

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
        this.setButtons();
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

    setButtons(){
        this.buttonClass1 = true;
        this.buttonClass2 = false;
        this.buttonClass3 = false;
        this.buttonClass4 = false;
    }

    click(){
        this.buttonClass2 = true;
        this.buttonClass3 = true;
        this.buttonClass4 = true;
        // console.log(this.buttonClass1);
    }
}