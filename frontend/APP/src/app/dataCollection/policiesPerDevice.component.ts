import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
declare let $: any;
import * as _ from 'lodash';

@Component({
    selector: 'policies-per-device',
    templateUrl: 'policiesPerDevice.component.html',
    styleUrls: ['dataCollection.component.less'],
})

export class PoliciesPerDeviceComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';
    deviceNo: any;
    stopAll = '<button class="btn btn-xs btn-primary" id="stopAll">監視全停止</button>';
    startAll = '<button class="btn btn-xs btn-default" id="stopAll">全解除</button>';
    ppdModel: any = [
        {label: 'No', hidden: true, name: 'policyNo', index: 'policyNo'},
        {label: 'デバイスグループ名',  name: 'deviceGroup', width: 100,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},
        {label: 'コレクションポリシーグループ名',  name: 'cpGroup', width: 100,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},
        {label: 'プライオリティー',  name: 'priority', width: 30,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},
        {label: 'コレクションポリシー', name: 'policy', width: 50, align: 'center',
            classes: 'policy', sortable: false,cellattr: this.renderCpColor },
        {label: ' ', name: 'btn_status', width: 50, align: 'center', search: false,
        formatter: this.fomatterBtn, sortable: false, height: 50,},

    ];
    deviceList: any = [];
    // testData: any = [
    //     {policyNo: 10, cpGroup: 'Cisco AER 基本監視', priority: '標準',
    //     policy: 'CPU監視  60分おき', action: 0, attr: {cpGroup: {rowspan: "2"}, priority: {rowspan: "2"}}},
    //     {policyNo: 20, cpGroup: 'Cisco AER 基本監視', priority: '標準',
    //     policy: 'HDD監視  60分おき', action: 1, attr: {cpGroup: {rowspan: null}, priority: {rowspan: null}}},
    //     {policyNo: 30, cpGroup: '緊急停止_SSEU A', priority: '緊急',
    //     policy: 'CPU監視  機能OFF', action: 1, attr: {cpGroup: {rowspan: "1"}, priority:{rowspan: "1"}}},
    // ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        this.httpClient.setUrl(this.apiPrefix);
        this.getDevices();
    }

    ngAfterViewInit() {
    }

    getDevices() {
        let _t = this;
        this.httpClient
            .toJson(this.httpClient.get('/api_data_collection_devices/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['devices']) {
                        this.deviceList = res['devices'];
                        this.deviceNo = this.route.snapshot.queryParams['id'];
                        if(typeof(this.deviceNo) == 'undefined'){
                            this.deviceNo = this.deviceList[0]['device_id'];
                        }
                        setTimeout(function () {
                            _t.drawPPDTable();
                            _t.setSelect();
                        }, 0);
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }

    setStopAllButton(res){
        if (res.data.length != 0){
            let flag = false;
            for (let item of res.data) {
                if (item.btn_status == 1){
                    return this.stopAll;
                } else if (item.btn_status == 0){
                    flag = true;
                }
            }
            if (flag) {
                return this.startAll;
            } else {
                return '';
            }
        } else {
            return ' ';
        }
    }

    public setSelect(){
        let _this = this;
        $('#device').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            _this.deviceNo = $('#device').val();
            let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
            $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
        }).val(this.deviceNo).trigger("chosen:updated");
        console.log('deviceNo,init.finish:',this.deviceNo);
    }

    public fomatterBtn(cellvalue, options, rowObject) {
        if (cellvalue == 1){
            return '<button class="btn btn-xs btn-primary stop"' +
                ' name="'+ rowObject["policy"] +'" id="'+ rowObject["cpGroupNo"] + "_" + rowObject["priority"] + "_" + rowObject["policyNo"] + '">監視停止</button>';
        } else if (cellvalue == 0){
            return '<button class="btn btn-xs btn-default stop"' +
                ' name="'+ rowObject["policy"] +'" id="'+ rowObject["cpGroupNo"] + "_" + rowObject["priority"] + "_" +  rowObject["policyNo"] + '">解除</button>';
        } else if (cellvalue == -1){
            return ''
        } else {
            return cellvalue;
        }
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

    renderCpColor(rowId, val, rowObject){
        let status = rowObject['valid_status'];
        if (status == 1){
            return 'style="color:blue"';
        }
    }

    allAction(res){
        let _this = this;
        $('#policiesTable').jqGrid('setLabel', 'btn_status', _this.setStopAllButton(res));
        let url = '/api_data_collection_devices/';
        $('#stopAll').click(function (event) {
            if(event.target.innerHTML == '監視全停止'){
                let _confirm = confirm('全部の監視を停止します。よろしいですか？');
                if(_confirm){
                    _this.httpClient
                        .toJson(_this.httpClient.put(url,
                                    {"is_all": 1, 'device_id': _this.deviceNo, "coll_policy_id": "-1",
                                    "policy_group_id": "-1", 'status': 0}
                                ))
                        .subscribe(res => {
                            if (res['status']['status'].toString().toLowerCase() === 'true') {
                                $('#stopAll').html('全解除').removeClass('btn-primary').addClass('btn-default');
                                let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
                                $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
                            } else {
                                // alert('失敗しました。');
                                alert(res['status']['message']);
                            }
                    });
                }

            } else {
                let _confirm = confirm('全部の監視停止を解除します。よろしいですか？');
                if(_confirm){
                    _this.httpClient
                        .toJson(_this.httpClient.put(url,
                                    {"is_all": 1, 'device_id': _this.deviceNo, "coll_policy_id": "-1",
                                    "policy_group_id": "-1", 'status': 1}
                                ))
                        .subscribe(res => {
                            if (res['status']['status'].toString().toLowerCase() === 'true') {
                                $('#stopAll').html('監視全停止').removeClass('btn-default').addClass('btn-primary');
                                let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
                                $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");

                            } else {
                                // alert('失敗しました。');
                                alert(res['status']['message']);
                            }
                    });
                }
            }
        });
    }

    public stopPolicy(){
        let _this = this;
        $('.stop').click(function (event) {
            let id = $(event)[0].target.id;
            let policy = $(event)[0].target.name;
            let coll_policy_id = id.split('_')[2];
            let priority = id.split('_')[1];
            let policy_group_id = id.split('_')[0];
            let url = '/api_data_collection_devices/';

            if ($('#'+id).html() == '監視停止'){
                let _confirm = confirm(policy+'の監視を停止します。よろしいですか？');
                if(_confirm){
                    _this.httpClient
                        .toJson(_this.httpClient.put(url,
                                    {"is_all": 0, 'device_id': _this.deviceNo, "coll_policy_id": coll_policy_id,
                                    "policy_group_id": policy_group_id, 'priority': priority, 'status': 0}
                                ))
                        .subscribe(res => {
                            if (res['status']['status'].toString().toLowerCase() === 'true') {
                                console.log('device no'+_this.deviceNo);
                                let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
                                $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
                            } else {
                                // alert('失敗しました。');
                                alert(res['status']['message']);

                            }
                    });

                }

            } else {
                let _confirm = confirm(policy+'の監視停止を解除します。よろしいですか？');
                if(_confirm){
                    _this.httpClient
                        .toJson(_this.httpClient.put(url,
                                    {"is_all": 0, 'device_id': _this.deviceNo, "coll_policy_id": coll_policy_id,
                                    "policy_group_id": policy_group_id, 'priority': priority, 'status': 1}
                                ))
                        .subscribe(res => {
                            if (res['status']['status'].toString().toLowerCase() === 'true') {
                                let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
                                $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
                            } else {
                                // alert('失敗しました。');
                                alert(res['status']['message']);
                            }
                    });
                }
            }
        });
    }

    public renderTitleHeight(){
        $('.ui-jqgrid-htable th div').height(22);
    }

    public drawPPDTable() {
        let _this = this;
        let deviceId = this.deviceNo;
        if(typeof(deviceId) == 'undefined'){
           return;
        }
        let url = '/v1/api_data_collection_devices/?device_id='+deviceId;
        $('#policiesTable').jqGrid({
            url: url,
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: this.ppdModel,
            // postData: { '': '' },
            // data: this.testData,
            // viewrecords: true,
            loadComplete: function (res) {
                _this.stopPolicy();
                _this.renderTitleHeight();
                _this.allAction(res);
            },
            // rowNum: 10,
            // rowList: [10, 20, 30],
            autowidth: true,
            beforeSelectRow: function (rowid, e) {
                return false;
            },
            height: 400,
            // pager: '#policiesPager',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });
        // $('#policiesTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }

}