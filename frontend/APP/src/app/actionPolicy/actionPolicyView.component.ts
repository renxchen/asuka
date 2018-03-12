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

    apiPrefix: any = '/v1';

    actionPolicyModel: any = [
        {label: 'No', hidden: true, name: 'action_policy_id', index: 'action_policy_id'},
        {label: 'アクションポリシー名',  name: 'name', width: 30, align: 'center'},
        {label: 'デバイスグループ',  name: 'device_group', width: 30, align: 'center'},
        {label: 'コレクションポリシーグループ',  name: 'policy_group', width: 30, align: 'center'},
        {label: '閾値タイプ',  name: 'threshold_type', width: 30, align: 'center'},
        {label: 'カラム名',  name: 'column_name', width: 30, align: 'center'},
        {label: 'Critical',  name: 'critical', width: 30, align: 'center'},
        {label: 'Major',  name: 'major', width: 30, align: 'center'},
        {label: 'Minor',  name: 'minor', width: 30, align: 'center'},
        {label: '概要', name: 'description', width: 40, align: 'center'},
        {label: 'アクション', name: 'action', width: 40, align: 'center', search: false,
        formatter: this.formatterbtns},
    ];

    testData: any = [
        {action_policy_id: 10, name: 'action policy 1', description: 'description 1'},
        {action_policy_id: 11, name: 'action policy 2', description: 'description 2'},
        {action_policy_id: 12, name: 'action policy 3', description: 'description 3'},
    ];

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
        this.drawActionPolicyTable();
    }

    formatterbtns(cellvalue, options, rowObject) {
        // let buttons = '';
        let buttons = '<button class="btn btn-xs btn-primary detail" id="detail_'+ rowObject["action_policy_id"] + '"><i class="fa fa-info-circle"></i> 確認</button>&nbsp;';
        buttons += '<button class="btn btn-xs btn-success edit" id="edit_'+ rowObject["action_policy_id"] + '"><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;';
        buttons += '<button class="btn btn-xs btn-warning delete" id="delete_'+ rowObject["action_policy_id"] + '"><i class="fa fa-minus-square"></i> 削除</button>';

        return buttons
    }

    newActionPolicy(){
        this.router.navigate(['/index/actionpolicylogin'],{queryParams:{'name':''}});
    }

    drawActionPolicyTable(){
        let _this = this;
        $('#actionPolicyTable').jqGrid({
            // url: '/v1/api_data_collection/',
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: _this.actionPolicyModel,
            // postData: { '': '' },
            data: _this.testData,
            // viewrecords: true,
            loadComplete: function() {
                // _this.showDataTable();
                // _this.renderColor();
            },
            rowNum: 10,
            rowList: [ 10, 20, 30],
            autowidth: true,
            beforeSelectRow: function(rowid, e) { return false; },
            height: 230,
            pager: '#actionPolicyPager',
            // jsonReader: {
            //     root: 'data',
            //     page: 'current_page_num',
            //     total: 'num_page',
            //     records: 'total_num',
            //     userData: 'status',
            //     repeatitems: false,
            // },
        });
        $('#actionPolicyTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}