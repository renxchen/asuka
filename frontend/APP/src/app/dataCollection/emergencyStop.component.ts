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

    emergencyStopModel: any = [
        {label: 'deviceNo', hidden: true, name: 'deviceNo'},
        {label: 'デバイス', name: 'device', width: 50, align: 'center', classes: 'device', sortable: false, search: true, cellattr: this.arrtSetting},
        {label: 'デバイスグループ',  name: 'deviceGroup', width: 50, align: 'center', sortable: false, search: false, cellattr: this.arrtSetting},
        {label: 'policyGroupNo', name: 'cpGroupNo', hidden:true},
        {label: 'コレクションポリシーグループ',  name: 'cpGroup', width: 50, align: 'center', sortable: false, search: false, cellattr: this.arrtSetting},
        {label: '優先度', name: 'priority', width: 30, align: 'center', sortable:false, search: false, cellattr: this.arrtSetting},
        {label: 'policyNo', name: 'policyNo', hidden: true},
        {label: 'コレクションポリシー',  name: 'policy', width: 50, align: 'center', sortable: false, search: false},
    ];

    // testData: any = [
    //     {device_id: 10, device: 'SSEU_A', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
    //     policy: 'CPU監視  60分おき', attr: {device: {rowspan: "3"}, policy_group: {rowspan: "2"}, priority: {rowspan: "2"}}},
    //     {device_id: 10, device: 'SSEU_A', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
    //     policy: 'HDD監視  60分おき', attr: {device: {rowspan: null}, policy_group: {rowspan: null}, priority: {rowspan: null}}},
    //     {device_id: 10, device: 'SSEU_A', policy_group_id:12, policy_group: 'Cisco_AER_重点監視', priority: '高',
    //     policy: 'CPU監視  15分おき', attr: {device: {rowspan: null}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
    //     {device_id: 20, device: 'SSEU_B', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
    //     policy: 'CPU監視  60おき', attr: {device: {rowspan: 1}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
    //     {device_id: 30, device: 'SSEU_C', policy_group_id:11, policy_group: 'Cisco_AER_基本監視', priority: '標準',
    //     policy: 'CPU監視  60分おき', attr: {device: {rowspan: 2}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
    //     {device_id: 30, device: 'SSEU_C', policy_group_id:12, policy_group: 'Cisco_AER_重点監視', priority: '高',
    //     policy: 'CPU監視  15分おき', attr: {device: {rowspan: null}, policy_group: {rowspan: "1"}, priority:{rowspan: "1"}}},
    // ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {

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
            let _content = '<div style="color:blue; text-decoration: underline;cursor: pointer">';
            _content += _target.html() + '</div>';
            _target.html(_content);
            let deviceNo = _target.prev().html();
            _target.click( function (event) {
                _this.router.navigate(['/index/policiesperdevice'],{queryParams:{'id':deviceNo}});
            })
        }
    }

    public drawEmergencyStopTable() {
        let _this = this;
        let url = '/v1/api_emergency_stop_list/';
        $('#emergencyStopTable').jqGrid({
            url: url,
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: this.emergencyStopModel,
            // postData: { '': '' },
            // data: this.testData,
            // viewrecords: true,
            loadComplete: function () {
                _this.renderLink();
            },
            // rowNum: 2,
            // rowList: [1, 2, 3],
            autowidth: true,
            beforeSelectRow: function (rowid, e) {
                return false;
            },
            height: 400,
            // pager: '#emergencyStopPager',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });
        $('#emergencyStopTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}