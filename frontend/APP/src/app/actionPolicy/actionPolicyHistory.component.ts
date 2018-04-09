import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'action-policy-history',
    templateUrl: 'actionPolicyHistory.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class ActionPolicyHistoryComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';

    actionHistoryModel: any = [
        {label: 'No', hidden: true, name: 'action_history_id', index: 'action_history_id'},
        {label: 'アクション実行日時',  name: 'action_time', width: 30, align: 'center'},
        {label: 'アクションポリシー名',  name: 'action_policy_name', width: 30, align: 'center'},
        {label: 'デバイス',  name: 'device', width: 30, align: 'center'},
        {label: 'コレクションポリシー名',  name: 'policy', width: 30, align: 'center'},
        {label: '重要度',  name: 'priority', width: 30, align: 'center'},
        {label: '実行アクション',  name: 'action', width: 30, align: 'center'},
        {label: '実行アクション詳細', name: 'action_detail', width: 45, align: 'center'},

    ];

    testData: any = [
        {action_policy_id: 10, action_policy_name: 'action policy 1', description: 'description 1'},
        {action_policy_id: 11, action_policy_name: 'action policy 2', description: 'description 2'},
        {action_policy_id: 12, action_policy_name: 'action policy 3', description: 'description 3'},
    ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        // public bsModalRef: BsModalRef
    ) {}

    ngOnInit(){

    }

    ngAfterViewInit() {
        this.drawActionHistoryTable();
    }

    drawActionHistoryTable(){
        let _this = this;
        $('#actionHistoryTable').jqGrid({
            // url: '/v1/api_data_collection/',
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: _this.actionHistoryModel,
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
            pager: '#actionHistoryPager',
            // jsonReader: {
            //     root: 'data',
            //     page: 'current_page_num',
            //     total: 'num_page',
            //     records: 'total_num',
            //     userData: 'status',
            //     repeatitems: false,
            // },
        });
        $('#actionHistoryTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}