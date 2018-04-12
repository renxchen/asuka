/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: cPGDetail.component.ts
* @time: 2018/03/13
* @desc: display collection policy group in detail
*/
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
    templateUrl: './cPGDetail.component.html',
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
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    constructor(
        private httpClient: HttpClientComponent,
        private activatedRoute: ActivatedRoute,
        private router: Router,
        private modalService: BsModalService
    ) {
        let cPIdTmp = this.activatedRoute.snapshot.queryParams['id'];
        if (cPIdTmp) {
            this.cPGId = cPIdTmp;
            this.getCPGInfo(this.cPGId);
        } else {
            this.router.navigate(['/index/cpgview']);
        }
    }

    ngOnInit() {
        this.getOsType();
        this.getCPNames();
    }

    public getCPGInfo(id: any) {
        /**
        * @brief get the specified collection policy group data and assignment variable
        * @param id:collection policy id
        * @author Dan Lv
        * @date 2018/03/13
        */
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
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (groupData && groupData.length > 0) {
                        this.name = _.get(groupData[0], 'name');
                        this.desc = _.get(groupData[0], 'desc');
                        this.selectedOsType = _.get(groupData[0], 'ostypeid');
                    }
                    if (groupsData) {
                        this.cpList = groupsData;
                        this.moreInfoTable(this.cpList);
                    }
                }else {
                    if (res['status'] && res['status']['message']) {
                        this.modalMsg = res['status']['message'];
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }
    public getOsType() {
        /**
        * @brief get all of the ostype data
        * @author Dan Lv
        * @date 2018/03/13
        */
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_ostype/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        this.osType = res['data'];
                        let osTypeTmp = _.clone(res['data']);
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        this.modalMsg = res['status']['message'];
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }
    public getCPNames() {
        /**
        * @brief get all of the collection policy data
        * @author Dan Lv
        * @date 2018/03/13
        */
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_get_collection_policy_name/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        this.cpNames = res['data'];
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        this.modalMsg = res['status']['message'];
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }
    public moreInfoTable(data: any) {
        /**
        * @brief display data in the grid
        * @param data:the data displayed in the grid
        * @pre called after calling the function of getCPGInfo
        * @author Dan Lv
        * @date 2018/03/13
        */
        let _t = this;
        _t.cpgActionGrid$ = $('#moreInfoTable').jqGrid({
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
                            return '<a class="cp-span" id=' + 'cli_' + policyId +
                                ' style="text-decoration:underline;color:#066ac5">' + cellvalue + '</a>';
                        } else if (cpType.toString() === '1') {
                            return '<a class="cp-span" id=' + 'snmp_' + policyId +
                                ' style="text-decoration:underline;color:#066ac5">' + cellvalue + '</a>';
                        } else {
                            return;
                        }
                    }
                },
                { name: 'exec_interval', index: 'exec_interval', width: 30, align: 'center', formatter: _t.execIntervalFormatter },
            ],
            gridComplete: function () {
                _t.toCPDetail();
            },
            beforeSelectRow: function (rowid, e) { return false; },
            // beforeRequest: function () {
            //     let currentPage: any = $('#cpTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#cpTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#cpTable').jqGrid('getGridParam', 'records');
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         $('#cpTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
            pager: '#cPGPager',
            rowNum: 5,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 150,
            viewrecords: true,
            emptyrecords: 'No data to display',
        });
        $('#cpglogintable').jqGrid({ searchOnEnter: true, defaultSearch: 'cn' });
    }
    public execIntervalFormatter(id: any) {
        /**
        * @brief format the data
        * @author Dan Lv
        * @date 2018/03/14
        */
        if (id.toString() === '60') {
            return '1分';
        } else if (id.toString() === '300') {
            return '5分';
        } else if (id.toString() === '900') {
            return '15分';
        } else if (id.toString() === '3600') {
            return '1時間';
        } else if (id.toString() === '86400') {
            return '1日';
        } else {
            return 'null';
        }
    }
    public toCPDetail() {
        /**
        * @brief get the collection policy id and jump to colleciton policy detail page
        * @author Dan Lv
        * @date 2018/03/13
        */
        let _t = this;
        $('.cp-span').click(function (event) {
            let idTmp = $(event)[0].target.id.split('_');
            let type: any = _.indexOf(idTmp, 0);
            if (_.indexOf(idTmp, 'cli', 0) !== -1) {
                _t.router.navigate(['/index/clicpdetail'],
                    { queryParams: { 'id': idTmp[1] } });
            } else if (_.indexOf(idTmp, 'snmp', 0) !== -1) {
                _t.router.navigate(['/index/snmpcpdetail'],
                    { queryParams: { 'id': idTmp[1] } });
            }else {
                event.stopPropagation();
                return;
            }
            event.stopPropagation();
        });
    }
    public cPGEdit() {
        /**
        * @brief jump to collection policy group edit page
        * @author Dan Lv
        * @date 2018/03/13
        */
        this.router.navigate(['/index/cpgedit'],
            { queryParams: { 'id': this.cPGId } });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        /**
        * @brief show modal dialog
        * @author Dan Lv
        * @date 2018/03/13
        */
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
