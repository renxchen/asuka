import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
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

    apiPrefix: any = '/v1';
    title: string;

    modalRef: BsModalRef;
    modalConfig = {
        animated: true,
        keyboard: true,
        backdrop: true,
        ignoreBackdropClick: true
    };

    editingAction: string;
    actionSelectTitle: string;
    actionSelectedType: number = 0;

    snmpVersion: number = 1;


    actionPolicyName: string;
    actionPolicyDescription: string;

    triggerType: number;
    triggerTypes: any = [{id: 2, value: '文字列比較'}, {id: 1, value: '数値比較'}, {id: 0, value: '演算比較'}, {id: 3, value: '取得失敗'}];
    conditionList: any = [{id: 4, value: '未満'}, {id: 0, value: '以下'}, {id: 1, value: '等しい'}, {id: 2, value: '以上'}, {id: 5, value: 'より大きい'}, {id: 3, value: '異なる'}];
    continuousOverList: any = [{id: 1, value: '1回'}, {id: 2, value: '2回'}, {id: 3, value: '3回'}, {id: 4, value: '4回'}, {id: 5, value: '5回'}];
    actionTypes: any = [{id: 0, value: 'SNMP Trap送信'}, {id: 1, value: 'スクリプト実行'}, {id: 2, value: '自動化シナリオ実行'}];

    columnOne: string;
    columnA: string;
    columnB: string;

    criticalActionA: string;
    criticalActionB: string;
    majorActionA: string;
    majorActionB: string;
    minorActionA: string;
    minorActionB: string;

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        private modalService: BsModalService
    ) {}

    ngOnInit(){
        this.httpClient.setUrl(this.apiPrefix);
        this.triggerType = 2;
        this.columnOne = "table sample";
        this.criticalActionA = "Please select action 1";
        this.criticalActionB = "Please select action 2";
        this.majorActionA = "Please select action 1";
        this.majorActionB = "Please select action 2";
        this.minorActionA = "Please select action 1";
        this.minorActionB = "Please select action 2";
    }

    ngAfterViewInit() {

    }

    resetAll(){
        this.resetColumn();
    }

    resetColumn(){
        this.columnOne = "";
        this.columnA = "";
        this.columnB = "";
    }

    resetTable(){

    }

    selectAction(template, isWhich){
        this.editingAction = isWhich;
        if (isWhich == "critical_1"){

            this.actionSelectTitle = "Critical Action 1";
        } else if (isWhich == "critical_2"){
            this.actionSelectTitle = "Critical Action 2";

        } else if (isWhich == "major_1"){
            this.actionSelectTitle = "Major Action 1";

        } else if (isWhich == "major_2"){
            this.actionSelectTitle = "Major Action 2";

        } else if (isWhich == "minor_1"){
            this.actionSelectTitle = "Minor Action 1";

        } else if (isWhich == "minor_2"){
            this.actionSelectTitle = "Minor Action 2";

        }

        this.modalRef = this.modalService.show(template, this.modalConfig);
    }


    confirmSelectedAction(){

        let actionName;
        for (let i=0; i<this.actionTypes.length; i++){
            if (this.actionTypes[i]['id'] == this.actionSelectedType ){
                actionName = this.actionTypes[i]['value'];
            }
        }

        if (this.editingAction == "critical_1"){
            this.criticalActionA = actionName;
        } else if (this.editingAction == "critical_2"){
            this.criticalActionB = actionName;
        } else if (this.editingAction == "major_1"){
            this.majorActionA = actionName;
        } else if (this.editingAction == "major_2"){
            this.majorActionB = actionName;
        } else if (this.editingAction == "minor_1"){
            this.minorActionA = actionName;
        } else if (this.editingAction == "minor_2"){
            this.minorActionB = actionName;
        }

        this.modalRef.hide();
    }

    save(){


        let type = this.triggerType;
        let checkResult = this.isColumnMachTrigger(type);
        if (!checkResult['flag']){
            alert(checkResult['message']);
            return;
        }
        if (type == 0) {
            this.saveCalculationType();
        } else if (type == 1) {
            this.saveNumberType();
        } else if (type == 2) {
            this.saveStringType();
        } else if (type == 3) {
            this.saveFailedType();
        }
    }

    isColumnMachTrigger(type){

    }

    checkStringType(){

    }

    saveStringType(){
        let flag;

        let actionPolicyInfo: any = {};
        let url = '/api_new_data_collection/';

        actionPolicyInfo['name'] = this.actionPolicyName;
        actionPolicyInfo['desc'] = this.actionPolicyDescription;
        actionPolicyInfo['trigger_type'] = 2;
        actionPolicyInfo['column_a'] = this.columnOne;
        actionPolicyInfo['column_b'] = null;




    }

    saveNumberType(){
        let actionPolicyInfo: any = {};
        let url = '/api_new_data_collection/';

        actionPolicyInfo['name'] = this.actionPolicyName;
        actionPolicyInfo['desc'] = this.actionPolicyDescription;
        actionPolicyInfo['trigger_type'] = 1;
        actionPolicyInfo['column_a'] = this.columnOne;
        actionPolicyInfo['column_b'] = null;

    }

    saveCalculationType(){
        let actionPolicyInfo: any = {};
        let url = '/api_new_data_collection/';

        actionPolicyInfo['name'] = this.actionPolicyName;
        actionPolicyInfo['desc'] = this.actionPolicyDescription;
        actionPolicyInfo['trigger_type'] = 0;
        actionPolicyInfo['column_a'] = this.columnA;
        actionPolicyInfo['column_b'] = this.columnB;

    }

    saveFailedType(){
        let actionPolicyInfo: any = {};
        let url = '/api_new_data_collection/';

        actionPolicyInfo['name'] = this.actionPolicyName;
        actionPolicyInfo['desc'] = this.actionPolicyDescription;
        actionPolicyInfo['trigger_type'] = 3;
        actionPolicyInfo['column_a'] = this.columnOne;
        actionPolicyInfo['column_b'] = null;

    }


}