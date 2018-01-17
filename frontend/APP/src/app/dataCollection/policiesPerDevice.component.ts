import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'policies-per-device',
    templateUrl: 'policiesPerDevice.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class PoliciesPerDeviceComponent implements OnInit, AfterViewInit {

    dd: string = '1';
    deviceNo: number;
    stopAll = '<button class="btn btn-xs btn-primary">全停止</button>';
    startAll = '<button class="btn btn-default">全解除</button>';
    dcModel: any = [
        {label: 'No', hidden: true, name: 'policyNo', index: 'policyNo'},
        {label: 'デバイス',  name: 'device', width: 30, align: 'center',
        cellattr: this.arrtSetting, sortable: false,},
        {label: 'コレクションポリシーグループ名',  name: 'cpGroup', width: 100,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},
        {label: 'プライオリティー',  name: 'priority', width: 30,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},
        {label: 'コレクションポリシー', name: 'policy', width: 50, align: 'center',
            classes: 'policy', sortable: false,},
        {label: this.stopAll, name: 'action', width: 50, align: 'center', search: false,
        formatter: this.fomatterBtn, sortable: false, height: 50,}
    ];

    testData: any = [
        {policyNo: 10, device:'SSEU A', cpGroup: 'Cisco AER 基本監視', priority: '標準',
        policy: 'CPU監視　60分おき', attr: {device: {rowspan: "3"}, cpGroup: {rowspan: "2"}, priority: {rowspan: "2"}}},
        {policyNo: 20, device:'SSEU A', cpGroup: 'Cisco AER 基本監視', priority: '標準',
        policy: 'HDD監視　60分おき', attr: {device: {rowspan: "none"}, cpGroup: {rowspan: "none"}, priority: {rowspan: "none"}}},
        {policyNo: 30, device:'SSEU A', cpGroup: '緊急停止_SSEU A', priority: '緊急',
        policy: 'CPU監視 機能OFF', attr: {device: {rowspan: "none"}, cpGroup: {rowspan: "1"}, priority:{rowspan: "1"}}},
        // {cpNo: 2, cPName: 'ishiba_test_01', ostype: 'cisco-ios', oid: '$#$3', commond: 'show interface', summary: 'test'},
        // {cpNo: 3, cPName: 'ishiba_test_02', ostype: 'cisco-ios', oid: '$#$8', commond: 'show file systems', summary: 'file'},
        // {cpNo: 4, cPName: 'ishiba_test_03', ostype: 'cisco-ios', oid: '$#$2', commond: 'show data', summary: 'data'},
        // {cpNo: 5, cPName: 'masaykan_test_01', ostype: 'cisco-ios', oid: '$#$6', commond: 'show ip route', summary: 'route'},
        // {cpNo: 6, cPName: 'masaykan_test', ostype: 'cisco-ios', oid: '$#$7', commond: 'show file', summary: 'open_file'},
    ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        // this.route.params.subscribe(params => {
        //     this.deviceNo = params['deviceNo'];
        // });
        this.deviceNo = this.route.snapshot.queryParams['id'];
        console.log(this.deviceNo);

    }

    ngAfterViewInit() {
        this.setSelect();
        this.drawPPDTable();


    }

    public setSelect(){
        let _this = this;
        $('#device').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            _this.dd = $('#device').val();

        });
    }

    public fomatterBtn(cellvalue, options, rowObject) {
        // console.log(rowObject);
        return '<button class="btn btn-xs btn-primary stop"' +
            ' name='+ rowObject["policy"] +' id='+ rowObject["policyNo"] + '>停止</button>'
    }

    public arrtSetting(rowId, val, rawObject, cm) {
        let attr = rawObject.attr[cm.name], result;
        if (attr.rowspan != "none") {
            result = ' rowspan=' + '"' + attr.rowspan + '"';
        } else {
            result = ' style="display:none"';
        }
        return result;
    }

    public stopPolicy(){
        $('.stop').click(function (event) {
            let id = $(event)[0].target.id;
            let policy = $(event)[0].target.name;



            if ($('#'+id).html() == '停止'){
                let _confirm = confirm('Stop '+policy+'?');
                if(_confirm){
                    $('#'+id).html('解除').removeClass('btn-primary').addClass('btn-default');
                }

            } else {
                let _confirm = confirm('Start '+policy+'?');
                if(_confirm){
                    $('#'+id).html('停止').removeClass('btn-default').addClass('btn-primary');
                }

            }


            // let id = target.id;
            // target.html("<a>ffffff</a>");
        });
    }

    public renderTitleHeight(){
        $('.ui-jqgrid-htable th div').height(22);
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
                _this.stopPolicy();
                _this.renderTitleHeight();
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
        // $('#policiesTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }

}