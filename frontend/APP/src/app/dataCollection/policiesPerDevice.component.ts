import { Component, OnInit, AfterViewInit,Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
// import { DevicesComponentsDirective } from './devicesComponents.directive';
declare let $: any;
import * as _ from 'lodash';

@Component({
    selector: 'policies-per-device',
    templateUrl: 'policiesPerDevice.component.html',
    styleUrls: ['dataCollection.component.less'],
    // directives: [DevicesComponentsDirective]
})

export class PoliciesPerDeviceComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';
    // dd: string = '1';
    deviceNo: any;
    stopAll = '<button class="btn btn-xs btn-primary" id="stopAll">全停止</button>';
    startAll = '<button class="btn btn-xs btn-default" id="stopAll">全解除</button>';
    ppdModel: any = [
        {label: 'No', hidden: true, name: 'policyNo', index: 'policyNo'},
        // {label: 'デバイス',  name: 'device', width: 30, align: 'center',
        // cellattr: this.arrtSetting, sortable: false,},
        {label: 'コレクションポリシーグループ名',  name: 'cpGroup', width: 100,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},

        {label: 'プライオリティー',  name: 'priority', width: 30,
            align: 'center', sortable: false, cellattr: this.arrtSetting,},

        {label: 'コレクションポリシー', name: 'policy', width: 50, align: 'center',
            classes: 'policy', sortable: false,cellattr: this.renderCpColor },

        {label: ' ', name: 'valid_status', width: 50, align: 'center', search: false,
        formatter: this.fomatterBtn, sortable: false, height: 50,},
        // {label: '', name: 'action', width: 50, align: 'center', search: false,
        // formatter: this.fomatterBtn, sortable: false, height: 50,}
    ];
    deviceList: any = [];
    testData: any = [
        {policyNo: 10, cpGroup: 'Cisco AER 基本監視', priority: '標準',
        policy: 'CPU監視  60分おき', action: 0, attr: {cpGroup: {rowspan: "2"}, priority: {rowspan: "2"}}},
        {policyNo: 20, cpGroup: 'Cisco AER 基本監視', priority: '標準',
        policy: 'HDD監視  60分おき', action: 1, attr: {cpGroup: {rowspan: null}, priority: {rowspan: null}}},
        {policyNo: 30, cpGroup: '緊急停止_SSEU A', priority: '緊急',
        policy: 'CPU監視  機能OFF', action: 1, attr: {cpGroup: {rowspan: "1"}, priority:{rowspan: "1"}}},
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
        this.httpClient.setUrl(this.apiPrefix);
        this.getDevices();
        // v1/api_data_collection_devices/
        // this.deviceList = [{deviceNo: 1, name: 'deivce1'},
        //     {deviceNo: 2, name: 'deivce2'},
        //     {deviceNo: 3, name: 'deivce3'},
        //     {deviceNo: 4, name: 'deivce4'},];

        // console.log('bbb',this.deviceNo);
        // this.route.params.subscribe(params => {
        //     this.deviceNo = params['deviceNo'];
        // });

    }

    // @Input()
    //   set ready(isReady: boolean) {
    //     if (isReady) this.setSelect();
    //   }

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
                        // console.log(this.deviceList);
                        this.deviceNo = this.route.snapshot.queryParams['id'];
                        // console.log(this.deviceNo);
                        // console.log(typeof(this.deviceNo));

                        if(typeof(this.deviceNo) == 'undefined'){
                            // console.log("ununun");
                            // console.log(this.deviceList[0]['device_id']);
                            this.deviceNo = this.deviceList[0]['device_id'];
                            // console.log('init,no=1 :',this.deviceNo);

                        }


                        setTimeout(function () {
                            _t.drawPPDTable();
                            _t.setSelect();
                        }, 0);


                        // $('#device').chosen();


                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }

    setStopAllButton(res){
        // console.log(res.data.length);
        if (res.data.length != 0){
            for (let item of res.data) {
                if (item.valid_status == true){
                    return this.stopAll;
                }
            }
            return this.startAll;
        } else {
            return ' ';
        }

    }



    public setSelect(){
        let _this = this;
        // $("#device").chosen("destroy").init();
        // jQuery Chosen.destroy();
        $('#device').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            _this.deviceNo = $('#device').val();
            // console.log('deviceNo',_this.deviceNo);
            let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
            // console.log(newUrl);
            // $("#policiesTable").trigger("reloadGrid");
            $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");

        }).val(this.deviceNo).trigger("chosen:updated");



        // $('#device').val(this.deviceNo).trigger("chosen:updated");
        // $('#device')



        // $('#device').chosen({
        //     no_results_text: "検索結果ありません：",
        //     search_contains: true,
        // }).change( function () {
        //     _this.deviceNo = $('#device').val();
        //     console.log('deviceNo',_this.deviceNo);
        //
        //
        // });

        console.log('deviceNo,init.finish:',this.deviceNo);
    }

    public fomatterBtn(cellvalue, options, rowObject) {
        // console.log(rowObject);
        if (cellvalue == true){
            return '<button class="btn btn-xs btn-primary stop"' +
                ' name="'+ rowObject["policy"] +'" id="'+ rowObject["cpGroupNo"] + "_" + rowObject["priority"] + "_" + rowObject["policyNo"] + '">停止</button>';
        } else if (cellvalue == 0){
            return '<button class="btn btn-xs btn-default stop"' +
                ' name="'+ rowObject["policy"] +'" id="'+ rowObject["cpGroupNo"] + "_" + rowObject["priority"] + "_" +  rowObject["policyNo"] + '">解除</button>';
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
        // console.log(res);

        let _this = this;
        // $('#policiesTable').jqGrid('setLabel', 'action', 'asd');
        $('#policiesTable').jqGrid('setLabel', 'valid_status', _this.setStopAllButton(res));
        let url = '/api_data_collection_devices/';
        $('#stopAll').click(function (event) {
            // console.log(event);
            if(event.target.innerHTML == '全停止'){
                let _confirm = confirm('Stop All?');
                // event.target.parentElement.innerHTML = _this.startAll;

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
                                // if (res['data']) {
                                //     // let id = res['data']['coll_policy_id'];
                                //     // this.router.navigate(['/index/cliCPEdit'],
                                //     //     { queryParams: { 'id': id } });
                                // }
                            } else {
                                alert('failed');
                                // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                                //     this.uniqueFlg = false;
                                // } else {
                                //     alert(res['status']['message']);
                                // }
                            }
                    });
                    // send the request to background, return if success; if success, reload the table
                }

            } else {
                let _confirm = confirm('Start All?');
                // event.target.parentElement.innerHTML = _this.startAll;
                if(_confirm){
                    _this.httpClient
                        .toJson(_this.httpClient.put(url,
                                    {"is_all": 1, 'device_id': _this.deviceNo, "coll_policy_id": "-1",
                                    "policy_group_id": "-1", 'status': 1}
                                ))
                        .subscribe(res => {
                            if (res['status']['status'].toString().toLowerCase() === 'true') {
                                $('#stopAll').html('全停止').removeClass('btn-default').addClass('btn-primary');
                                let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
                                $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
                                // if (res['data']) {
                                //     // let id = res['data']['coll_policy_id'];
                                //     // this.router.navigate(['/index/cliCPEdit'],
                                //     //     { queryParams: { 'id': id } });
                                // }
                            } else {
                                alert('failed');
                                // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                                //     this.uniqueFlg = false;
                                // } else {
                                //     alert(res['status']['message']);
                                // }
                            }
                    });
                    // send the request to background, return if success; if success, reload the table
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

            if ($('#'+id).html() == '停止'){
                let _confirm = confirm('Stop '+policy+'?');
                if(_confirm){
                    // $('#'+id).html('解除').removeClass('btn-primary').addClass('btn-default');
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
                                // if (res['data']) {
                                //     // let id = res['data']['coll_policy_id'];
                                //     // this.router.navigate(['/index/cliCPEdit'],
                                //     //     { queryParams: { 'id': id } });
                                // }
                            } else {
                                alert('failed');
                                // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                                //     this.uniqueFlg = false;
                                // } else {
                                //     alert(res['status']['message']);
                                // }
                            }
                    });
                    // send the request to background, return if success; if success, reload the table
                }

            } else {
                let _confirm = confirm('Start '+policy+'?');
                if(_confirm){
                    // $('#'+id).html('停止').removeClass('btn-default').addClass('btn-primary');
                    // send the request to background, return if success; if success, reload the table
                    _this.httpClient
                        .toJson(_this.httpClient.put(url,
                                    {"is_all": 0, 'device_id': _this.deviceNo, "coll_policy_id": coll_policy_id,
                                    "policy_group_id": policy_group_id, 'priority': priority, 'status': 1}
                                ))
                        .subscribe(res => {
                            if (res['status']['status'].toString().toLowerCase() === 'true') {
                                let newUrl = '/v1/api_data_collection_devices/?device_id='+_this.deviceNo;
                                $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");
                                // if (res['data']) {
                                //     // let id = res['data']['coll_policy_id'];
                                //     // this.router.navigate(['/index/cliCPEdit'],
                                //     //     { queryParams: { 'id': id } });
                                // }
                            } else {
                                alert('failed');
                                // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                                //     this.uniqueFlg = false;
                                // } else {
                                //     alert(res['status']['message']);
                                // }
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