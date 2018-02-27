import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'devices-per-policy',
    templateUrl: 'devicesPerPolicy.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DevicesPerPolicyComponent implements OnInit, AfterViewInit {

    // total: number;
    apiPrefix: any = '/v1';
    policyNo: any;
    policyList: any = [];


    dppModel: any = [
        {label: 'No', hidden: true, name: 'deviceNo', index: 'deviceNo'},
        // {label: 'コレクションポリシー',  name: 'policy', width: 30, align: 'center',
        // cellattr: this.arrtSetting.bind(this), sortable: false, classes: 'policy', search: false,},
        {label: 'デバイス', name: 'device', width: 50, align: 'center',
            classes: 'device',},
        {label: 'ステータス',  name: 'status', width: 30,
            align: 'center', sortable: false, search: false, },

    ];

    testData: any = [
        {deviceNo: 1, device: 'device1', status: '取得中'},
        {deviceNo: 2, device: 'device2', status: '停止'},
        {deviceNo: 3, device: 'device3', status: '取得中'}
    ];

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit() {
        this.httpClient.setUrl(this.apiPrefix);
        this.getPolicy();
        // this.total = this.testData.length;
    }

    ngAfterViewInit() {
        // this.setSelect();
        this.drawDPPTable();
    }

    getPolicy(){
        let _t = this;
        this.httpClient
            .toJson(this.httpClient.get('/api_data_collection_policy/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['policies']) {

                        this.policyList = res['policies'];
                        // console.log(this.deviceList);
                        this.policyNo = this.route.snapshot.queryParams['id'];
                        // console.log(this.deviceNo);
                        // console.log(typeof(this.deviceNo));

                        if(typeof(this.policyNo) == 'undefined'){
                            // console.log("ununun");
                            // console.log(this.deviceList[0]['device_id']);
                            this.policyNo = this.policyList[0]['policy_id'];
                            // console.log('init,no=1 :',this.deviceNo);

                        }
                        this.drawDPPTable();

                        setTimeout(function () {
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

    public setSelect(){
        let _this = this;
        $('#policy').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            _this.policyNo = $('#device').val();
            // console.log('deviceNo',_this.deviceNo);
            let newUrl = '/v1/api_data_collection_policys/?policy_id='+_this.policyNo;
            // console.log(newUrl);
            // $("#policiesTable").trigger("reloadGrid");
            $("#policiesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");

        }).val(this.policyNo).trigger("chosen:updated");
    }

    public renderLink(){
        let _this = this;
        let _device = $('.device');
        for (let i=0;i<_device.length;i++){
            let _target = $(_device[i]);
            let _content = '<div style="color:blue;">';
            _content += _target.html() + '</div>';
            _target.html(_content);
            let deviceNo = _target.prev().html();
            _target.click( function (event) {
                _this.router.navigate(['/index/policiesperdevice'],{queryParams:{'id':deviceNo}});
            })
        }

        let _policy = $($('.policy')["0"]);
        let _content2 = '<a href="#" style="color:blue;">';
        _content2 += _policy.html() + '</a>';
        _policy.html(_content2);
    }

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

    public drawDPPTable() {
        let _this = this;
        // let policyId = this.policyNo;
        // if(typeof(policyId) == 'undefined'){
        //    return;
        // }
        // let url = '/v1/api_data_collection_policy/?policy_id='+policyId;
        $('#devicesTable').jqGrid({
            // url: url,
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: this.dppModel,
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
        $('#devicesTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}