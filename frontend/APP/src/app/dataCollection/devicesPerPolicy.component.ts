import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
declare var $: any;
// import * as _ from 'lodash';

@Component({
    selector: 'devices-per-policy',
    templateUrl: 'devicesPerPolicy.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DevicesPerPolicyComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';
    policyNo: any;
    policyList: any = [];

    dppModel: any = [
        {label: 'No', hidden: true, name: 'deviceNo', index: 'deviceNo'},
        {label: 'デバイス', name: 'device', width: 50, align: 'center',
            classes: 'device', sortable:false},
        {label: 'ステータス',  name: 'status', width: 30,
            align: 'center', sortable: false, search: false},
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
    }

    ngAfterViewInit() {
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
                        this.policyNo = this.route.snapshot.queryParams['id'];

                        if(typeof(this.policyNo) == 'undefined'){
                            this.policyNo = this.policyList[0]['coll_policy_id'];
                        }
                        this.drawDPPTable();
                        setTimeout(function () {
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

    public setSelect(){
        let _this = this;
        $('#policy').chosen({
            no_results_text: "検索結果ありません：",
            search_contains: true,
        }).change( function () {
            _this.policyNo = $('#policy').val();
            let newUrl = '/v1/api_data_collection_policy/?coll_policy_id='+_this.policyNo;
            $("#devicesTable").jqGrid().setGridParam({url : newUrl}).trigger("reloadGrid");

        }).val(this.policyNo).trigger("chosen:updated");
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

    jumpToPolicy(){
        let policyNo = this.policyNo;
        for (let policy of this.policyList){
            if (policy["coll_policy_id"] == policyNo){
                if (policy["policy_type"] == 0){
                    this.router.navigate(['/index/clicpdetail'],{queryParams:{'id':policyNo}});
                } else if (policy["policy_type"] == 1){
                    this.router.navigate(['/index/snmpcpdetail'],{queryParams:{'id':policyNo}});
                }
            }
        }
    }

    public drawDPPTable() {
        let _this = this;
        let policyId = this.policyNo;
        console.log(policyId);
        if(typeof(policyId) == 'undefined'){
           return;
        }
        let url = '/v1/api_data_collection_policy/?coll_policy_id='+policyId;
        $('#devicesTable').jqGrid({
            url: url,
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: this.dppModel,
            // postData: { '': '' },
            // data: this.testData,
            // viewrecords: true,
            loadComplete: function () {
                // _this.stopPolicy();
                _this.renderLink();
            },
            // rowNum: 2,
            rowList: [10, 20, 30],
            autowidth: true,
            beforeSelectRow: function (rowid, e) {
                return false;
            },
            height: 400,
            pager: '#devicesPager',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });
        $('#devicesTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}