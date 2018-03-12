import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'action-policy-login',
    templateUrl: 'actionPolicyLogin.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class ActionPolicyLoginComponent implements OnInit, AfterViewInit {




    actionPolicyName: string;
    actionPolicyDescription: string;

    triggerType: number;
    triggerTypes: any = [{id: 0, value: '文字列比較'}, {id: 1, value: '数値比較'}, {id: 2, value: '演算比較'}, {id: 3, value: '取得失敗'}];
    conditionList: any = [{id: 4, value: '未満'}, {id: 0, value: '以下'}, {id: 1, value: '等しい'}, {id: 2, value: '以上'}, {id: 5, value: 'より大きい'}, {id: 3, value: '異なる'}];
    continuousOverList: any = [{id: 1, value: '1回'}, {id: 2, value: '2回'}, {id: 3, value: '3回'}, {id: 4, value: '4回'}, {id: 5, value: '5回'}];
    actionTypes: any = [{id: 0, value: 'SNMP Trap送信'}, {id: 1, value: 'スクリプト実行'}, {id: 2, value: '自動化シナリオ実行'}];


    isStringCompareTable: boolean;
    oneColumn: boolean;
    isTriggerType0: boolean;
    isTriggerType1: boolean;
    isTriggerType2: boolean;
    isTriggerType3: boolean;

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        // public bsModalRef: BsModalRef
    ) {}

    ngOnInit(){
        this.triggerType = 0;
        this.oneColumn = true;
        this.setTriggerType(0);
    }

    ngAfterViewInit() {

    }

    setTriggerType(type: number){
        if (type == 0){
            this.isTriggerType0 = true;
            this.isTriggerType1 = false;
            this.isTriggerType2 = false;
            this.isTriggerType3 = false;
            this.oneColumn = true;
        } else if (type == 1){
            this.isTriggerType0 = false;
            this.isTriggerType1 = true;
            this.isTriggerType2 = false;
            this.isTriggerType3 = false;
            this.oneColumn = true;
        } else if (type == 2){
            this.isTriggerType0 = false;
            this.isTriggerType1 = false;
            this.isTriggerType2 = true;
            this.isTriggerType3 = false;
            this.oneColumn = false;
        } else if (type == 3){
            this.isTriggerType0 = false;
            this.isTriggerType1 = false;
            this.isTriggerType2 = false;
            this.isTriggerType3 = true;
            this.oneColumn = true;
        }
    }

    changeTriggerType(){
        let type = this.triggerType;
        this.setTriggerType(type);
    }
}