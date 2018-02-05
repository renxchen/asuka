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
    selector: 'cpg-action',
    templateUrl: 'cPGAction.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})
export class CPGActionComponent implements OnInit, AfterViewInit {
    actionType: any;
    id: any;
    apiPrefix: any;
    tableData: any;
    cpgActionGrid$: any;
    name: any;
    osType: any;
    selectedOsType: any;
    desc: any;
    moreFlg: Boolean = true;
    addFlg: Boolean = true;
    nameFlg: Boolean = true;
    nameNotNull: Boolean = true;
    usingFlg: Boolean = false;
    cliFlg: Boolean = true;
    selCPName: any;
    cpNames: any;
    cpNamesTmp: any;
    snmpNames: any;
    selExecInterval: any;
    selExpiDurantion: any = '1';
    cpsTem: any = {};
    cpList: any = [];
    isInclude: Boolean = true;
    testData: any = [{ 'policys_groups_id': '2', 'status': '0', 'policy_name': 'really', 'exec_interval': '5时' },
    { 'policys_groups_id': '1', 'status': '0', 'policy_name': 'check', 'exec_interval': '5分' },
    { 'policys_groups_id': '2', 'status': '1', 'policy_name': 'box', 'exec_interval': '15分' }];
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef,
        private modalService: BsModalService) {
    }
    ngOnInit() {
        this.selCPName = 'null';
        this.selExecInterval = 'null';
        // this.selExpiDurantion = '1';
        this.getOsType();
        this.getCPNames();
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (this.actionType !== 'create') {
                if (this.actionType === 'detail') {
                    this.moreFlg = false;
                } else {
                    this.moreFlg = true;
                }
                if (typeof (this.id) !== 'undefined') {
                    this.getCPGInfo(this.id);
                }
            } else {
                this.addFlg = false;
                this.moreInfoTable(this.cpList);
            }
        }, 0);
    }
    private addBtn() {
        this.addFlg = !this.addFlg;
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
    public getCPGInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url + id)).subscribe(res => {
                // console.log('edit', res);
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let groupData: any[] = _.get(res, 'policy_group_data');
                let groupsData = _.get(res, 'policys_groups_data');
                // let daa: any = {};
                if (status && status['status'].toLowerCase() === 'true') {
                    if (msg === 'POLICY_GROUP_EXIST_IN_SCHEDULE') {
                        this.usingFlg = true;
                    } else {
                        this.usingFlg = false;
                    }
                    if (groupData && groupData.length > 0) {
                        this.name = _.get(groupData[0], 'name');
                        this.desc = _.get(groupData[0], 'desc');
                        this.selectedOsType = _.get(groupData[0], 'ostypeid');
                    }
                    if (groupsData) {
                        this.cpList = groupsData;
                        this.moreInfoTable(this.cpList);
                        // this.moreInfoTable(this.testData);
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
                        // let cpNamesTmp = _.clone(res['data']);
                        // this.selCPName = cpNamesTmp[0]['coll_policy_id'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
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
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-warning delete"  id='
            + rowObject['policy_name'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    public formatterCheckbox(cellvalue, options, rowObject) {
        return '<input type="checkbox" value=' + rowObject['policy_name'] + '>';
    }

    // table
    public moreInfoTable(data: any) {
        let _t = this;
        this.cpgActionGrid$ = $('#moreInfoTable').jqGrid({
            datatype: 'local',
            data: data,
            colNames: ['No', 'PolicyID', '機能ON/OFF', 'コレクションポリシー名', '監視間隔', 'Action'],
            colModel: [
                { hidden: true, name: 'policys_groups_id', index: 'policys_groups_id', search: false },
                { hidden: true, name: 'collection_policy_id', index: 'collection_policy_id', search: false, key: true },
                {
                    name: 'status', index: 'status', width: 50, align: 'center',
                    editable: true, edittype: 'checkbox',
                    editoptions: { value: '1:0' },
                    formatter: 'checkbox',
                    formatoptions: { disabled: false },
                    // formatter: _t.formatterCheckbox
                },
                { name: 'policy_name', index: 'policy_name', width: 60, align: 'center' },
                { name: 'exec_interval', index: 'exec_interval', width: 40, align: 'center', formatter: _t.execIntervalFomatter },
                // { label: '保存間隔', name: 'expired_duration', index: 'expired_duration', width: 40, align: 'center', },
                {
                    name: '', width: 30, align: 'center', formatter: _t.formatterBtn, sortable: false, editable: true, edittype: 'select',
                }
            ],
            gridComplete: function () {
                _t.deleteBtn();
            },
            loadComplete: function () {
                let iCol = _t.getColumnIndexByName($(this), 'status');
                for (let i = 0; i < this.rows.length; i++) {
                    $(this.rows[i].cells[iCol]).click(function (e) {
                        let id = $(e.target).closest('tr')[0].id, isChecked = $(e.target).is(':checked') ? 1 : 0;
                        alert(id);
                        let cpList: any = _t.cpList;
                        for (let j = 0; j < cpList.length; j++) {
                            if (cpList[j].collection_policy_id.toString() === id) {
                                cpList[j].status = isChecked;
                                alert(isChecked);
                            }
                        }
                        _t.cpList = cpList;
                        return;
                    });
                }
            },

            // beforeSelectRow: function (rowid, e) { return false; },
            pager: '#cpgloginPager',
            rowNum: 5,
            rowList: [5, 10, 15],
            width: 736,
            height: 100,
            viewrecords: true,
            emptyrecords: 'Nothing to display',
        });
        $('#cpglogintable').jqGrid({ searchOnEnter: true, defaultSearch: 'cn' });
    }
    public deleteBtn() {
        let _t = this;
        $('.delete').click(function (event) {
            let cpList: any = _t.cpList;
            let id = $(event)[0].target.id;
            for (let i = 0; i < cpList.length; i++) {
                if (cpList[i].policy_name.toString() === id) {
                    cpList.splice(i, 1);
                    _t.cpgActionGrid$.GridUnload();
                    _t.moreInfoTable(cpList);
                }
            }
            _t.cpList = cpList;
        });
    }
    public cPGEdit() {
        this.actionType = 'edit';
        this.moreFlg = true;
    }
    public addMoreInfo() {
        let cpInfo: any = {};
        let cpList = this.cpList;
        for (let i = 0; i < cpList.length; i++) {
            if (cpList[i].collection_policy_id.toString() === this.selCPName) {
                alert('Can not add the same cp');
                return;
            }
        }
        if (this.selCPName !== 'null' && this.selExecInterval !== 'null') {
            cpInfo['policy_name'] = this.cpNameFomatter(this.selCPName);
            cpInfo['exec_interval'] = this.selExecInterval;
            cpInfo['expired_durantion'] = this.selExpiDurantion;
            cpInfo['collection_policy_id'] = this.selCPName;
            cpInfo['status'] = '0';
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
    // backend need to confirm the field collection_policy_id(edit) and policy(nes);
    public cPGLogin() {
        this.apiPrefix = '/v1';
        let groups: any = {};
        if (this.doCheck()) {
            groups['cps'] = this.cpList;
            // console.log(this.cpList, groups);
            let url = '/api_collection_policy_group/?name='
                + this.name + '&ostype=' + this.selectedOsType + '&desc=' + this.desc;
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
    public cpNamecChange(selCPName: any) {
        let _t = this;
        _t.cliFlg = true;
        _.each(this.cpNames, function (cpName) {
            if (cpName.coll_policy_id.toString() === selCPName
                && cpName.policy_type === 0) {
                _t.selExecInterval = 'null';
                _t.cliFlg = false;
            }
        });
    }
    public execIntervalChange(selExecInterval: any) {
        if (selExecInterval === '1') {
            // this.selCPName = 'null';
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
    public cpNameFomatter(id: any) {
        let cpNames = this.cpNames;
        for (let i = 0; i < cpNames.length; i++) {
            if (cpNames[i].coll_policy_id.toString() === id) {
                return cpNames[i].name;
            }
        }
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
    public getColumnIndexByName(grid, columnName) {
        let cm = $('#moreInfoTable').jqGrid('getGridParam', 'colModel');
        for (let i = 0; i < cm.length; i++) {
            if (cm[i].name === columnName) {
                return i;
            }
        }
        return -1;
    }
}
