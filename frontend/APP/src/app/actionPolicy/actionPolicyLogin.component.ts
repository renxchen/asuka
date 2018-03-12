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

    thresholdType: number;
    thresholdTypes: any = [{id: 0, value: '文字列比較'}, {id: 1, value: '数値比較'}, {id: 2, value: '演算比較'}, {id: 3, value: '取得失敗'}];

    actionTypes: any = [{id: 0, value: 'SNMP Trap送信'}, {id: 1, value: 'スクリプト実行'}, {id: 2, value: '自動化シナリオ実行'}];


    isStringCompareTable: boolean;

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        // public bsModalRef: BsModalRef
    ) {}

    ngOnInit(){
        this.thresholdType = 0;
        this.isStringCompareTable = true;
    }

    ngAfterViewInit() {

    }
}