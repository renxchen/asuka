import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
// import * as _ from 'lodash';

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
        {label: 'deviceGroupId', hidden: true, name:'device_group_id'},
        {label: 'デバイスグループ',  name: 'device_group', width: 30, align: 'center', formatter: this.formatterDeviceGroup},
        {label: 'policyGroupId', hidden: true, name: 'coll_policy_group_id'},
        {label: 'コレクションポリシーグループ',  name: 'coll_policy_group', width: 30, align: 'center', formatter: this.formatterColumns},
        {label: '閾値タイプ',  name: 'trigger_type', width: 30, align: 'center'},
        {label: 'カラム名',  name: 'column', width: 30, align: 'center', formatter: this.formatterColumns},
        {label: 'Critical',  name: 'critical_priority', width: 30, align: 'center', formatter: this.formatterColumns},
        {label: 'Major',  name: 'major_priority', width: 30, align: 'center', formatter: this.formatterColumns},
        {label: 'Minor',  name: 'minor_priority', width: 30, align: 'center', formatter: this.formatterColumns},
        {label: '概要', name: 'desc', width: 30, align: 'center'},
        {label: 'アクション', name: 'action', width: 60, align: 'center', search: false,
        formatter: this.formatterbtns, sortable:false},
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
        this.httpClient.setUrl(this.apiPrefix);
    }

    ngAfterViewInit() {
        this.drawActionPolicyTable();
    }

    formatterAction(cellvalue, options, rowObject) {
        if (cellvalue){

        }
    }

    formatterbtns(cellvalue, options, rowObject) {
        // let buttons = '';
        let buttons = '<button class="btn btn-xs btn-primary detail" id="detail，'+ rowObject["name"] + '"><i class="fa fa-info-circle"></i> 確認</button>&nbsp;';
        buttons += '<button class="btn btn-xs btn-success edit" id="edit，'+ rowObject["name"] + '"><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;';
        buttons += '<button class="btn btn-xs btn-warning delete" id="delete，'+ rowObject["name"] + '"><i class="fa fa-minus-square"></i> 削除</button>';

        return buttons
    }

    formatterColumns(cellvalue, options, rowObject) {
        if (cellvalue != ''){
            return '<i class="fa fa-genderless"></i> ' + cellvalue.replace(/,/g, '<br /><i class="fa fa-genderless"></i> ');
        } else {
            return '————'
        }

    }

    formatterDeviceGroup(cellvalue, options, rowObject){
        return '<span style="color: blue; text-decoration: underline;">' + cellvalue + '</span>';

    }

    newActionPolicy(){
        this.router.navigate(['/index/actionpolicylogin'],{queryParams:{'name':''}});
    }

    detailActionPolicy(){
        let _this = this;
        $('.detail').click(function (event) {
            let name = $(event)[0].target.id.split('，')[1];
            // open modal and init the title and id of modal
            _this.router.navigate(['/index/actionpolicylogin'],{queryParams:{'name': name, 'mode': 'detail'}});
        });
    }

    editActionPolicy(){
        let _this = this;
        $('.edit').click(function (event) {
            let name = $(event)[0].target.id.split('，')[1];
            // open modal and init the title and id of modal
            _this.router.navigate(['/index/actionpolicylogin'],{queryParams:{'name': name, 'mode': 'edit'}});
        });
    }

    deleteActionPolicy(){
        let _this = this;
        $('.delete').click(function (event) {
            let name = $(event)[0].target.id.split('，')[1];
            let flag = confirm('Delete '+name+'?');
            if (flag){
                let url = '/api_action_policy/?name=' + name;
                _this.httpClient
                    .toJson(_this.httpClient.delete(url))
                    .subscribe(res => {
                        alert(res['status']['status'].toString());
                    });
            }
            // open modal and init the title and id of modal
            // _this.router.navigate(['/index/actionpolicylogin'],{queryParams:{'name': name}});
        });
    }

    drawActionPolicyTable(){
        let _this = this;
        $('#actionPolicyTable').jqGrid({
            url: '/v1/api_action_policy/',
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: _this.actionPolicyModel,
            // postData: { '': '' },
            // data: _this.testData,
            // viewrecords: true,
            loadComplete: function() {
                _this.detailActionPolicy();
                _this.editActionPolicy();
                _this.deleteActionPolicy();
            },
            rowNum: 10,
            rowList: [ 10, 20, 30],
            autowidth: true,
            beforeSelectRow: function(rowid, e) { return false; },
            height: 230,
            pager: '#actionPolicyPager',
            jsonReader: {
                root: 'data.data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });
        $('#actionPolicyTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}