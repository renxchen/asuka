import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
declare var $: any;
// import * as _ from 'lodash';

@Component({
    selector: 'emergency-stop',
    templateUrl: 'emergencyStop.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class EmergencyStopComponent implements OnInit, AfterViewInit {

    // total: number;
    apiPrefix: any = '/v1';

    emergencyStopModel: any = [
        {label: 'deviceNo', hidden: true, name: 'device_id'},
        {label: 'デバイス', name: 'device', width: 50, align: 'center', classes: 'device', sortable: true, search: true, cellattr: this.arrtSetting},
        {label: 'policyGroupNo', name: 'policy_group_id', hidden:true},
        {label: 'コレクションポリシーグループ',  name: 'policy_group', width: 50, align: 'center', sortable: false, search: false, cellattr: this.arrtSetting},
        {label: '優先度', name: 'priority', width: 30, align: 'center', classes: 'device', sortable:false, search: false, cellattr: this.arrtSetting},
        {label: 'policyNo', name: 'policy_id', hidden: true},
        {label: 'コレクションポリシー',  name: 'policy', width: 50, align: 'center', sortable: false, search: false},
    ];

    testData: any = [
        {device_id: 10, device: 'SSEU_A', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
        policy: 'CPU監視  60分おき', attr: {device: {rowspan: "3"}, policy_group: {rowspan: "2"}, priority: {rowspan: "2"}}},
        {device_id: 10, device: 'SSEU_A', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
        policy: 'HDD監視  60分おき', attr: {device: {rowspan: null}, policy_group: {rowspan: null}, priority: {rowspan: null}}},
        {device_id: 10, device: 'SSEU_A', policy_group_id:12, policy_group: 'Cisco_AER_重点監視', priority: '高',
        policy: 'CPU監視  15分おき', attr: {device: {rowspan: null}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
        {device_id: 20, device: 'SSEU_B', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
        policy: 'CPU監視  60分おき', attr: {device: {rowspan: 1}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
        {device_id: 30, device: 'SSEU_C', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
        policy: 'CPU監視  60分おき', attr: {device: {rowspan: 2}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
        {device_id: 30, device: 'SSEU_C', policy_group_id:12, policy_group: 'Cisco_AER_重点監視', priority: '高',
        policy: 'CPU監視  15分おき', attr: {device: {rowspan: null}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
    ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        this.httpClient.setUrl(this.apiPrefix);

        // this.total = this.testData.length;
    }

    ngAfterViewInit() {
        this.drawEmergencyStopTable();
    }

    public arrtSetting(rowId, val, rowObject, cm) {
        let attr = rowObject.attr[cm.name], result;
        if (attr.rowspan != null) {
            result = ' rowspan=' + '"' + attr.rowspan + '"';
        } else {
            result = ' style="display:none"';
        }
        return result;
    }


    public renderLink(){
        let _this = this;
        let _device = $('.device');
        for (let i=0;i<_device.length;i++){
            let _target = $(_device[i]);
            let _content = '<div style="color:blue; text-decoration: underline;">';
            _content += _target.html() + '</div>';
            _target.html(_content);
            let deviceNo = _target.prev().html();
            _target.click( function (event) {
                _this.router.navigate(['/index/policiesperdevice'],{queryParams:{'id':deviceNo}});
            })
        }

        let _policy = $($('.policy')["0"]);
        let _content2 = '<a href="#" style="color:blue; text-decoration: underline;">';
        _content2 += _policy.html() + '</a>';
        _policy.html(_content2);
    }

    // jumpToPolicy(){
    //     let policyNo = this.policyNo;
    //     for (let policy of this.policyList){
    //         if (policy["coll_policy_id"] == policyNo){
    //             if (policy["policy_type"] == 0){
    //                 this.router.navigate(['/index/clicpdetail'],{queryParams:{'id':policyNo}});
    //             } else if (policy["policy_type"] == 1){
    //                 this.router.navigate(['/index/snmpcpdetail'],{queryParams:{'id':policyNo}});
    //             }
    //         }
    //     }
    // }

    // public arrtSetting(rowId, val, rowObject, cm) {
    //     // let result;
    //     // if (rowId == 1){
    //     //     result = 'rowspan=' + '"' + this.total + '"';
    //     // } else {
    //     //     result = 'style="display:none"';
    //     // }
    //     // return result;
    //     let attr = rowObject.attr[cm.name], result;
    //     if (attr.rowspan != null) {
    //         result = ' rowspan=' + '"' + attr.rowspan + '"';
    //     } else {
    //         result = ' style="display:none"';
    //     }
    //     return result;
    // }

    public drawEmergencyStopTable() {
        let _this = this;
        let url = '/v1/api_data_collection_policy/';
        $('#emergencyStopTable').jqGrid({
            // url: url,
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: this.emergencyStopModel,
            // postData: { '': '' },
            data: this.testData,
            // viewrecords: true,
            loadComplete: function () {
                // _this.stopPolicy();
                // _this.renderLink();
            },
            // rowNum: 2,
            // rowList: [1, 2, 3],
            autowidth: true,
            beforeSelectRow: function (rowid, e) {
                return false;
            },
            height: 340,
            // autoheight: true,
            // grouping:true,
            // groupingView : {
            //     groupField : ['device']
            // },
            // pager: '#emergencyStopPager',
            // jsonReader: {
            //     root: 'data',
            //     page: 'current_page_num',
            //     total: 'num_page',
            //     records: 'total_num',
            //     userData: 'status',
            //     repeatitems: false,
            // },
        });
        $('#emergencyStopTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}