import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { ModalComponent } from '../../../components/modal/modal.component';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'cpg-detail',
    templateUrl: 'cPGDetail.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})
export class CPGDetailComponent implements OnInit {
    cPGId: any;
    apiPrefix: any;
    cpgActionGrid$: any;
    name: any;
    osType: any;
    selectedOsType: any;
    desc: any;
    cpNames: any;
    cpList: any = [];
    constructor(
        private httpClient: HttpClientComponent,
        private activatedRoute: ActivatedRoute,
        private router: Router,
    ) {
        let cPIdTmp = this.activatedRoute.snapshot.queryParams['id'];
        if (cPIdTmp) {
            this.cPGId = cPIdTmp;
            this.getCPGInfo( this.cPGId);
        } else {
            this.router.navigate(['/index/cpgview/']);
        }
    }

    ngOnInit() {
        this.getOsType();
        this.getCPNames();
    }

    public getCPGInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url + id)).subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data = _.get(res, 'data');
                let groupData: any[] = _.get(data, 'policy_group_data');
                let groupsData = _.get(data, 'policys_groups_data');
                if (status && status['status'].toLowerCase() === 'true') {
                    if (groupData && groupData.length > 0) {
                        this.name = _.get(groupData[0], 'name');
                        this.desc = _.get(groupData[0], 'desc');
                        this.selectedOsType = _.get(groupData[0], 'ostypeid');
                    }
                    if (groupsData) {
                        this.cpList = groupsData;
                        this.moreInfoTable(this.cpList);
                    }
                }
            });
    }
    public getOsType() {
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_ostype/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        this.osType = res['data'];
                        let osTypeTmp = _.clone(res['data']);
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public getCPNames() {
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_get_collection_policy_name/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        this.cpNames = res['data'];
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public moreInfoTable(data: any) {
        let _t = this;
        this.cpgActionGrid$ = $('#moreInfoTable').jqGrid({
            datatype: 'local',
            data: data,
            colNames: ['No', 'PolicyID', 'PolicyType', '機能ON/OFF', 'コレクションポリシー名', '監視間隔'],
            colModel: [
                { hidden: true, name: 'policys_groups_id', index: 'policys_groups_id', search: false },
                { hidden: true, name: 'policy', index: 'policy', search: false, key: true },
                { hidden: true, name: 'policy_policy_type', index: 'policy_policy_type', search: false },
                {
                    name: 'status', index: 'status', width: 30, align: 'center',
                    editable: false, edittype: 'checkbox',
                    editoptions: { value: '1:0' },
                    formatter: 'checkbox',
                    formatoptions: { disabled: true },
                },
                {
                    name: 'policy_name', index: 'policy_name', width: 60, align: 'center',
                    formatter: function (cellvalue, options, rowObject) {
                        let policyId = rowObject.policy;
                        let cpType: any = rowObject.policy_policy_type;

                        if (cpType.toString() === '0') {
                            return '<a href="/index/cliCPDetail?id=' + policyId
                                + '"style="text-decoration:underline;color:#066ac5">' + cellvalue + '</a>';
                        } else if (cpType.toString() === '1') {
                            return '<a href="/index/snmpCPDetail?id=' + policyId
                                + '"style="text-decoration:underline;color:#066ac5">' + cellvalue + '</a>';
                        } else {
                            return;
                        }
                    }
                },
                { name: 'exec_interval', index: 'exec_interval', width: 30, align: 'center', formatter: _t.execIntervalFomatter },
            ],

            beforeSelectRow: function (rowid, e) { return false; },
            beforeRequest: function () {
                let currentPage: any = $('#cpTable').jqGrid('getGridParam', 'page');
                let rowNum: any = $('#cpTable').jqGrid('getGridParam', 'rowNum');
                let records: any = $('#cpTable').jqGrid('getGridParam', 'records');
                let totalPages = records % rowNum;
                if (records > 0 && currentPage > totalPages) {
                    $('#cpTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
                }
            },
            pager: '#cPGPager',
            rowNum: 5,
            rowList: [5, 10, 15],
            width: 700,
            height: 150,
            viewrecords: true,
            emptyrecords: 'Nothing to display',
        });
        $('#cpglogintable').jqGrid({ searchOnEnter: true, defaultSearch: 'cn' });
    }
    public execIntervalFomatter(id: any) {
        if (id.toString() === '1') {
            return '1分';
        } else if (id.toString() === '2') {
            return '5分';
        } else if (id.toString() === '3') {
            return '15分';
        } else if (id.toString() === '4') {
            return '1時間';
        } else if (id.toString() === '5') {
            return '1日';
        } else {
            return 'null';
        }
    }
    public navCPDetail(cellvalue, options, rowObject) {
        let policyId = rowObject.policy;
        let cpType: any;
        let cpNames: any = this.cpNames;
        if (cpNames !== '') {
            for (let i = 0; i < cpNames.length; i++) {
                if (cpNames[i].coll_policy_id.toString() === policyId) {
                    cpType = cpNames[i].type;
                    break;
                }
            }
        }
        if (cpType === '0') {
            return '<a href="/index/cliDetail/?id="' + options.collection_policy_id + '>' + cellvalue + '</a>';
        } else if (cpType === '1') {
            return '<a href="/index/snmpDetail/?id="' + options.collection_policy_id + '>' + cellvalue + '</a>';
        } else {
            return;
        }
    }
    public cPGEdit() {
        this.router.navigate(['/index/cpgedit'],
            { queryParams: { 'id': this.cPGId } });
    }
}