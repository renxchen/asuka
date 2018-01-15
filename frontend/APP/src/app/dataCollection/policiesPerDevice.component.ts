import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'policies-per-device',
    templateUrl: 'policiesPerDevice.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class PoliciesPerDeviceComponent implements OnInit, AfterViewInit {

    dd: string = '1';
    dcModel: any = [
        {label: 'No', hidden: true, name: 'dcNo', index: 'dcNo'},
        {label: '優先度',  name: 'priority', width: 30, align: 'center'},
        {label: 'OS Type', name: 'ostype', width: 50, align: 'center'},
        {label: 'デバイスグループ',  name: 'deviceGroup', width: 80, align: 'center'},
        {label: 'コレクションポリシーグループ名',  name: 'cpGroup', width: 100, align: 'center'},
        {label: '有効期間',  name: 'validPeriod', width: 60, align: 'center'},
        {label: '取得方法', name: 'scheduleType', width: 50, align: 'center'},
        {label: 'ステータス', name: 'status', width: 50, align: 'center', classes: 'status'},
        {label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
        formatter: this.fomatterBtn
        }
    ];

    testData: any = [
        {dcNo: 10, priority: '標準', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '期間なし', scheduleType: '常に取得',  status: '無効'},
        {dcNo: 20, priority: '高', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '2017/12/12 23:59\n– 2018/1/12 23:59', scheduleType: '取得停止',  status: '有効'},
        // {cpNo: 2, cPName: 'ishiba_test_01', ostype: 'cisco-ios', oid: '$#$3', commond: 'show interface', summary: 'test'},
        // {cpNo: 3, cPName: 'ishiba_test_02', ostype: 'cisco-ios', oid: '$#$8', commond: 'show file systems', summary: 'file'},
        // {cpNo: 4, cPName: 'ishiba_test_03', ostype: 'cisco-ios', oid: '$#$2', commond: 'show data', summary: 'data'},
        // {cpNo: 5, cPName: 'masaykan_test_01', ostype: 'cisco-ios', oid: '$#$6', commond: 'show ip route', summary: 'route'},
        // {cpNo: 6, cPName: 'masaykan_test', ostype: 'cisco-ios', oid: '$#$7', commond: 'show file', summary: 'open_file'},
    ];


    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
    ) {}

    ngOnInit() {

    }

    ngAfterViewInit() {
        this.setSelect();
        this.drawPPDTable();

    }

    public setSelect(){
        let _this = this;
        $('#devices').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            _this.dd = $('#devices').val();
        });
    }

    public fomatterBtn(cellvalue, options, rowObject) {
        // console.log(rowObject);
        return '<button class="btn btn-xs btn-success edit" id='+ rowObject["dcNo"] + '><i class="fa fa-pencil-square"></i> 編集</button>'
    }

    public drawPPDTable() {
        let _this = this;
        $('#policiesTable').jqGrid({
            // url: '/v1/api_data_collection/',
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: this.dcModel,
            // postData: { '': '' },
            data: this.testData,
            // viewrecords: true,
            loadComplete: function () {
                // _this.editDC();
                // _this.renderColor();
            },
            rowNum: 10,
            rowList: [10, 20, 30],
            autowidth: true,
            beforeSelectRow: function (rowid, e) {
                return false;
            },
            height: 230,
            pager: '#policiesPager',
            // jsonReader: {
            //     root: 'data',
            //     page: 'current_page_num',
            //     total: 'num_page',
            //     records: 'total_num',
            //     userData: 'status',
            //     repeatitems: false,
            // },
        });
        $('#dcTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }

}