import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'devices-per-policy',
    templateUrl: 'devicesPerPolicy.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DevicesPerPolicyComponent implements OnInit, AfterViewInit {

    total: number;

    dcModel: any = [
        {label: 'No', hidden: true, name: 'deviceNo', index: 'deviceNo'},
        {label: 'コレクションポリシー',  name: 'policy', width: 30, align: 'center',
        cellattr: this.arrtSetting.bind(this), sortable: false, classes: 'policy'},
        {label: 'デバイス', name: 'device', width: 50, align: 'center',
            classes: 'device', sortable: false,},
        {label: 'ステータス',  name: 'status', width: 30,
            align: 'center', sortable: false },

    ];

    testData: any = [
        {deviceNo: 10, device:'SSEU A', status: '取得中', policy: 'CPU監視'},
        {deviceNo: 20, device:'SSEU B', status: '停止', policy: 'CPU監視'},
        {deviceNo: 30, device:'SSEU C', status: '取得中', policy: 'CPU監視'}
    ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
    ) {}

    ngOnInit() {
        this.total = this.testData.length;
    }

    ngAfterViewInit() {
        this.setSelect();
        this.drawDPPTable();
    }

    public setSelect(){
        let _this = this;
        $('#policy').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            // _this.dd = $('#devices').val();
        });
    }

    public renderLink(){
        let _device = $('.device');
        for (let i=0;i<_device.length;i++){
            let _target = $(_device[i]);
            let _content = '<a href="#" style="color:blue;">';
            _content += _target.html() + '</a>';
            _target.html(_content);
        }

        let _policy = $($('.policy')["0"]);
        let _content2 = '<a href="#" style="color:blue;">';
        _content2 += _policy.html() + '</a>';
        _policy.html(_content2);
    }

    public arrtSetting(rowId, val, rawObject, cm) {
        let result;
        if (rowId == 1){
            result = 'rowspan=' + '"' + this.total + '"';
        } else {
            result = 'style="display:none"';
        }
        return result;
    }

    public drawDPPTable() {
        let _this = this;
        $('#devicesTable').jqGrid({
            // url: '/v1/api_data_collection/',
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: this.dcModel,
            // postData: { '': '' },
            data: this.testData,
            // viewrecords: true,
            loadComplete: function () {
                // _this.stopPolicy();
                _this.renderLink();
            },
            rowNum: 10,
            // rowList: [10, 20, 30],
            autowidth: true,
            beforeSelectRow: function (rowid, e) {
                return false;
            },
            // autoheight: true,
            // grouping:true,
            // groupingView : {
            //     groupField : ['device']
            // },
            // pager: '#policiesPager',
            // jsonReader: {
            //     root: 'data',
            //     page: 'current_page_num',
            //     total: 'num_page',
            //     records: 'total_num',
            //     userData: 'status',
            //     repeatitems: false,
            // },
        });
    }
}