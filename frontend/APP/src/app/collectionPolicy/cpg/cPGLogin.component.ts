/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: cPGLogin.component.ts
* @time: 2018/03/13
* @desc: create collection policy group
*/
import { Component, OnInit, AfterViewInit, OnDestroy, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Validator } from '../../../components/validation/validation';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalDirective } from 'ngx-bootstrap/modal';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'cpg-login',
    templateUrl: './cPGLogin.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})
export class CPGLoginComponent implements OnInit, AfterViewInit {
    cPGId: any;
    apiPrefix: any;
    cpgActionGrid$: any;
    name: any;
    osType: any;
    selectedOsType: any;
    desc: any;
    // moreFlg: Boolean = true;
    addFlg: Boolean = true;
    nameFlg: Boolean = true;
    nameNotNull: Boolean = true;
    cliFlg: Boolean = true;
    selCPName: any;
    cpNames: any;
    cpNamesTmp: any;
    snmpNames: any;
    selExecInterval: any;
    // selExpiDurantion: any = '1';
    cpsTem: any = {};
    cpList: any = [];
    // bsModalRef: any;
    constructor(
        private httpClient: HttpClientComponent,
        private activatedRoute: ActivatedRoute,
        private router: Router,
        private bsModalRef: BsModalRef,
        private modalService: BsModalService
    ) { }

    ngOnInit() {
        this.selCPName = 'null';
        this.selExecInterval = 'null';
        // this.selExpiDurantion = '1';
        this.getOsType();
        this.getCPNames();
    }
    ngAfterViewInit() {
        setTimeout(() => {
            this.moreInfoTable(this.cpList);
        }, 0);
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
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                        // let osTypeTmp = _.clone(res['data']);
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
                        this.cpNamesTmp = res['data'];
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-warning delete"  id='
            + rowObject['policy'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    public deleteBtn() {
        let _t = this;
        $('.delete').click(function (event) {
            let cpList: any = _t.cpList;
            let id = $(event)[0].target.id;
            for (let i = 0; i < cpList.length; i++) {
                if (cpList[i].policy.toString() === id) {
                    cpList.splice(i, 1);
                    _t.cpgActionGrid$.GridUnload();
                    _t.moreInfoTable(cpList);
                }
            }
            _t.cpList = cpList;
            event.stopPropagation();
        });
    }
    public execIntervalChange(selExecInterval: any) {
        if (selExecInterval === '60') {
            let snmpNameTmp: any = [];
            _.each(this.cpNames, function (cpName) {
                if (cpName.policy_type.toString() === '1') {
                    snmpNameTmp.push(cpName);
                }
            });
            this.cpNames = snmpNameTmp;
        } else {
            this.cpNames = this.cpNamesTmp;
        }
    }
    public cpNamecChange(selCPName: any) {
        let _t = this;
        _t.cliFlg = true;
        _.each(this.cpNames, function (cpName) {
            if (cpName.coll_policy_id.toString() === selCPName
                && cpName.policy_type === 0) {
                // _t.selExecInterval = 'null';
                _t.cliFlg = false;
            }
        });
    }
    private addBtn() {
        this.addFlg = !this.addFlg;
    }
    public cpNameFomatter(id: any) {
        let cpNames = this.cpNames;
        let cpName: any = {};
        for (let i = 0; i < cpNames.length; i++) {
            if (cpNames[i].coll_policy_id.toString() === id) {
                cpName['name'] = cpNames[i].name;
                cpName['type'] = cpNames[i].policy_type;
                return cpName;
            }
        }
    }
    public toCPDetail() {
        let _t = this;
        $('.cp-span').click(function (event) {
            let idTmp = $(event)[0].target.id.split('_');
            let type: any = _.indexOf(idTmp, 0);
            if (_.indexOf(idTmp, 'cli', 0) !== -1) {
                _t.bsModalRef.hide();
                _t.router.navigate(['/index/clicpdetail'],
                    { queryParams: { 'id': idTmp[1] } });
            } else if (_.indexOf(idTmp, 'snmp', 0) !== -1) {
                _t.bsModalRef.hide();
                _t.router.navigate(['/index/snmpcpdetail'],
                    { queryParams: { 'id': idTmp[1] } });
            }
            event.stopPropagation();
        });
    }
    public addMoreInfo() {
        let cpInfo: any = {};
        let cpList = this.cpList;
        for (let i = 0; i < cpList.length; i++) {
            if (cpList[i].policy.toString() === this.selCPName) {
                alert('Can not add the same cp');
                return;
            }
        }
        if (this.selCPName !== 'null' && this.selExecInterval !== 'null') {
            let cpName = this.cpNameFomatter(this.selCPName);
            cpInfo['policy_name'] = cpName.name;
            cpInfo['exec_interval'] = this.selExecInterval;
            // cpInfo['expired_durantion'] = this.selExpiDurantion;
            cpInfo['policy'] = this.selCPName;
            cpInfo['status'] = '1';
            cpInfo['policy_group'] = this.cPGId;
            cpInfo['policy_policy_type'] = cpName.type;
            // console.log('cpInfo', cpInfo);
            this.cpList.push(cpInfo);
            this.cpgActionGrid$.GridUnload();
            this.moreInfoTable(this.cpList);
        } else {
            if (this.selCPName === 'null') {
                alert('cpName can not be null');
            }
            if (this.selExecInterval === 'null') {
                alert('Monitor time can not be null');
            }
        }
    }
    public getColumnIndexByName(grid, columnName) {
        let cm = $('#moreInfoTable').jqGrid('getGridParam', 'colModel');
        for (let i = 0; i < cm.length; i++) {
            if (cm[i].name === columnName) {
                return i;
            }
        }
        return -1;
    }
    public moreInfoTable(data: any) {
        let _t = this;
        _t.cpgActionGrid$ = $('#moreInfoTable').jqGrid({
            datatype: 'local',
            data: data,
            colNames: ['CPGID', 'CPID', 'PolicyType', '機能ON/OFF', 'コレクションポリシー名', '監視間隔', 'Action'],
            colModel: [
                { hidden: true, name: 'policys_groups_id', index: 'policys_groups_id', search: false },
                { hidden: true, name: 'policy', index: 'policy', search: false, key: true },
                { hidden: true, name: 'policy_policy_type', index: 'policy_policy_type', search: false },
                {
                    name: 'status', index: 'status', width: 30, align: 'center',
                    editable: false, edittype: 'checkbox',
                    editoptions: { value: '1:0' },
                    formatter: 'checkbox',
                    formatoptions: { disabled: false },
                },
                {
                    name: 'policy_name', index: 'policy_name', width: 60, align: 'center',
                    formatter: function (cellvalue, options, rowObject) {
                        let policyId = rowObject.policy;
                        let cpType: any = rowObject.policy_policy_type;
                        // if (cpType.toString() === '0') {
                        //     return '<a href="/index/clicpdetail?id=' + policyId
                        //         + '"style="text-decoration:underline;color:#066ac5">' + cellvalue + '</a>';
                        // } else if (cpType.toString() === '1') {
                        //     return '<a href="/index/snmpcpdetail?id=' + policyId
                        //         + '"style="text-decoration:underline;color:#066ac5">' + cellvalue + '</a>';
                        // } else {
                        //     return;
                        // }
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
                { name: 'exec_interval', index: 'exec_interval', width: 40, align: 'center', formatter: _t.execIntervalFomatter },
                // { label: '保存間隔', name: 'expired_duration', index: 'expired_duration', width: 40, align: 'center', },
                {
                    name: '', width: 30, align: 'center', formatter: _t.formatterBtn, sortable: false, editable: true, edittype: 'select',
                }
            ],
            gridComplete: function () {
                _t.deleteBtn();
                _t.toCPDetail();
            },
            loadComplete: function () {
                let iCol = _t.getColumnIndexByName($(this), 'status');
                for (let i = 0; i < this.rows.length; i++) {
                    $(this.rows[i].cells[iCol]).click(function (e) {
                        let id = $(e.target).closest('tr')[0].id, isChecked = $(e.target).is(':checked') ? 1 : 0;
                        let cpList: any = _t.cpList;
                        for (let j = 0; j < cpList.length; j++) {
                            if (cpList[j].policy.toString() === id) {
                                cpList[j].status = isChecked;
                            }
                        }
                        _t.cpList = cpList;
                        return;
                    });
                }
            },

            // beforeSelectRow: function (rowid, e) { return false; },
            pager: '#cPGPager',
            rowNum: 5,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 150,
            // viewrecords: true,
            // emptyrecords: 'Nothing to display',
        });
        $('#moreInfoTable').jqGrid({ searchOnEnter: true, defaultSearch: 'cn' });
    }
    public execIntervalFomatter(id: any) {
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
    public doCheck(): boolean {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        if (this.nameNotNull && this.nameFlg) {
            return true;
        } else {
            return false;
        }
    }
    public cPGLogin() {
        this.apiPrefix = '/v1';
        let groups: any = {};
        if (this.doCheck()) {
            groups['cps'] = this.cpList;
            groups['name'] = this.name;
            groups['ostype_name'] = this.selectedOsType;
            groups['desc'] = this.desc;
            // console.log(this.cpList, groups);
            let url = '/api_collection_policy_group/';
            // console.log(url + '---' + groups);
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(url, groups))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'msg');
                    if (status && status['status'].toLowerCase() === 'true') {
                        alert('保存しました。');
                        this.bsModalRef.hide();
                        this.modalService.setDismissReason('true');
                    } else {
                        if (msg) {
                            alert(msg);
                        }
                    }
                });
        }
    }
}
