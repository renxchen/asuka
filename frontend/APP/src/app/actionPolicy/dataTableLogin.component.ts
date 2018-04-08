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
    apiPrefix: any = '/v1';
    title: string;

    step = 1;
    stepStatus = 1;

    buttonDisable1: string = "";
    buttonDisable2: string = "disabled";
    buttonDisable3: string = "disabled";
    buttonDisable4: string = "disabled";

    buttonNextDisable: string = "";
    buttonBackDisable: string = "disabled";

    buttonFinishDisabled: string = "disabled";

    step1display: boolean = true;
    step2display: boolean = false;
    step3display: boolean = false;
    step4display: boolean = false;
    stepDisplay: any = [true, false, false, false];

    finishButton: boolean = false;

    buttonClass1: boolean = true;
    buttonClass2: boolean = false;
    buttonClass3: boolean = false;
    buttonClass4: boolean = false;
    buttonBackClass: boolean = false;
    buttonNextClass: boolean = true;


    tableName: string;
    description: any;
    selectedDeviceGroup;


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

    setButtons(){
        this.buttonClass1 = true;
        this.buttonClass2 = false;
        this.buttonClass3 = false;
        this.buttonClass4 = false;

        this.buttonBackClass = false;
        this.buttonNextClass = true;
    }

    setStep(stepNum,forward){
        if (forward){
            if (stepNum < 4 ){
                this.step = stepNum+1;
                this.stepDisplay[stepNum-1] = false;
                this.stepDisplay[stepNum] = true;
            }

        } else {
            this.stepDisplay[stepNum-1] = true;
            this.stepDisplay[stepNum] = false;
        }


    }

    next(){
        console.log('step', this.step);
        console.log('status', this.stepStatus);
        // this.setButtons();
        // this.setStep();
        if (this.stepStatus == 1){
            if (this.step < 2){
                this.step = 2;
            }
            this.stepStatus = 2;
            this.buttonDisable2 = "";
            this.buttonClass2 = true;
            this.step1display = false;
            this.step2display = true;
            this.buttonBackDisable = "";


        } else if (this.stepStatus == 2){
            if (this.step < 3){
                this.step = 3;
            }
            this.stepStatus = 3;
            this.buttonDisable3 = "";
            this.buttonClass3 = true;
            this.step2display = false;
            this.step3display = true;

        } else if (this.stepStatus == 3){
            if (this.step < 4){
                this.step = 4;
            }
            this.stepStatus = 4;
            this.buttonDisable4 = "";
            this.buttonClass4 = true;
            this.step3display = false;
            this.step4display = true;
            this.buttonNextDisable = "disabled";
            this.finishButton = true;

        } else if (this.step == 4){

        }

    }

    previous(){
        console.log('step', this.step);
        console.log('status', this.stepStatus);
        if (this.stepStatus == 2){
            this.stepStatus = 1;
            this.buttonBackDisable = "disabled";
            this.step1display = true;
            this.step2display = false;
        } else if (this.stepStatus == 1){

        } else if (this.stepStatus == 3){
            this.stepStatus = 2;
            this.step2display = true;
            this.step3display = false;
        } else if (this.stepStatus == 4){
            this.stepStatus = 3;
            this.step3display = true;
            this.step4display = false;
            this.buttonNextDisable = "";
        }

    }

    click(){
        this.buttonClass2 = true;
        this.buttonClass3 = true;
        this.buttonClass4 = true;
        // console.log(this.buttonClass1);
    }
}