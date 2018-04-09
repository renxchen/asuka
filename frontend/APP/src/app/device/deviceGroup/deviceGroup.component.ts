
/**
 * @author: Zizhuang Jiang
 * @contact: zizjiang@cisco.com
 * @file: deviceGroup.component.ts
 * @time: 2018/03/08
 * @desc: device group summary
 */import { Component, OnInit, AfterViewInit, TemplateRef } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
import { GroupLoginComponent } from './groupLogin.component';
import { GroupEditComponent } from './groupEdit.component';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'device-group',
    templateUrl: './deviceGroup.component.html',
    styleUrls: ['.././device.component.less']
})
export class DeviceGroupComponent implements OnInit, AfterViewInit {
    groupId: any;
    name: any;
    desc: any;
    osType: any;
    osTypeId: any;
    deviceTable$: any;
    apiPrefix: any;
    groups: any = [];
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    modalConfig = {
        animated: true,
        keyboard: false,
        backdrop: true,
        ignoreBackdropClick: true,
        class: 'modal-lg'
    };
    constructor(
        public httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private router: Router,
        private activedRoute: ActivatedRoute, ) {
    }
    ngOnInit() {
        this.getGroups();
    }
    ngAfterViewInit() {
        let groupIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (groupIdeTmp && typeof (groupIdeTmp) !== 'undefined') {
            this.groupId = groupIdeTmp;
            this.drawDeviceTable(this.groupId);
            this.getPanelData(this.groupId);
        } else {
            this.groupId = '-1';
            this.drawDeviceTable('-1');
            this.getPanelData('-1');
        }
    }
    public drawDeviceTable(id: any) {
        let _t = this;
        _t.deviceTable$ = $('#deviceTable').jqGrid({
            // api
            url: '/v1/api_device/?group_id=' + id,
            datatype: 'JSON',
            mtype: 'get',
            colNames: ['DeviceId', 'Hostname', 'IP Address', 'Telnet Port', 'SNMP Port', 'SNMP Community',
                'SNMP Version', 'Login Expect', 'Device Type', 'Telnet Status', 'SNMP Status'
            ],
            colModel: [
                { hidden: true, name: 'device_id', index: 'device_id', search: false, key: true },
                { name: 'hostname', index: 'hostname', width: 50, align: 'center', search: true },
                { name: 'ip', index: 'ip', width: 50, align: 'center', search: true },
                { name: 'telnet_port', index: 'telnet_port', width: 40, align: 'center', search: true },
                { name: 'snmp_port', index: 'snmp_port', width: 40, align: 'center', search: true },
                {
                    name: 'snmp_community', index: 'snmp_community', width: 50, align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                {
                    name: 'snmp_version', index: 'snmp_version', width: 50, align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                {
                    name: 'login_expect', index: 'login_expect', width: 50, align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                { name: 'device_type', index: 'device_type', width: 40, align: 'center', search: true },
                { name: 'telnet_status', index: 'telnet_status', width: 50, align: 'center', search: true },
                { name: 'snmp_status', index: 'status_type', width: 50, align: 'center', search: true },
            ],
            beforeSelectRow: function (rowid, e) { return false; },
            // beforeRequest: function () {
            //     let currentPage: any = $('#deviceTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#deviceTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#deviceTable').jqGrid('getGridParam', 'records');
            //     console.log(currentPage, rowNum, records);
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         $('#deviceTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
            gridComplete: function () {
                $('.ui-jqgrid tr.jqgrow td').css({ 'white-space': 'nowrap', 'text-overflow': 'ellipsis' });
            },
            loadComplete: function (res) {
                let status = _.get(_.get(res, 'status'), 'status');
                $('.ui-jqgrid tr.jqgrow td').css({ 'white-space': 'nowrap', 'text-overflow': 'ellipsis' });
                let code: any = _.get(_.get(res, 'status'), 'code');
                let msg: any = _.get(_.get(res, 'status'), 'message');
                if (status === 'False') {
                    if (code === 102 || code === 103) {
                        localStorage.setItem('sessionTimeOut', msg);
                        _t.router.navigate(['/login/']);
                    }
                }
            },
            pager: '#devicePager',
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 350,
            viewrecords: true,
            emptyrecords: 'マーチしたデータがない',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                repeatitems: false,
            },
        });
        $('#deviceTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    // no data formatter
    public noDataFormatter(cellvalue, options, rowObject) {
        if (cellvalue === null || cellvalue === '') {
            return '-';
        } else {
            return cellvalue;
        }
    }
    public loginExpFormmater(cellvalue, options, rowObject) {
        let cell: any;
        for (let i = 0; i < cellvalue.length; i++) {
            cell = cellvalue['i'] + '/n';
        }
        return cell;
    }
    public getGroups() {
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_device_groups/'))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data = _.get(res, 'data');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (data) {
                        this.groups = data;
                    }
                } else {
                    if (msg) {
                        this.modalMsg = msg;
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }
    public getPanelData(id: any) {
        /**
        * @brief get the current device group info and display them
        * param id: device group id
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        if (id === '-1') {
            this.name = '無所属';
            this.osType = '無所属';
            this.desc = '無所属';
            return;
        }
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_device_groups/?group_id=' + id))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data: any = _.get(res, 'data');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (data && data.length > 0) {
                        this.name = _.get(data[0], 'name');
                        this.osType = _.get(_.get(data[0], 'ostype'), 'name');
                        this.desc = _.get(data[0], 'desc');
                    }
                } else {
                    if (msg) {
                        this.modalMsg = msg;
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }

    public getGroupInfo(id: any) {
        /**
        * @brief get devices in the current group
        * param id: device group id
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        if (id) {
            this.groupId = id;
            this.getPanelData(id);
            $('#deviceTable').jqGrid('clearGridData');
            $('#deviceTable')
            .jqGrid('setGridParam', { url : '/v1/api_device/?group_id=' + id })
            .trigger('reloadGrid');
        }
    }
    public editGroup(id: any) {
        /**
        * @brief get the device group id and show edit popup
        * @post refresh table if edit successfully
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.modalRef = this.modalService.show(GroupEditComponent, this.modalConfig);
        this.modalRef.content.id = id;
        let group$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                this.getGroups();
                if (id = this.groupId) {
                    this.getGroupInfo(id);
                }
            }
            this.unsubscribe(group$);
        });
    }
    public deleteGroup(id: any) {
        let name: any;
        for (let i = 0; i < this.groups.length; i++) {
            if (this.groups[i]['group_id'] === id) {
                name = this.groups[i]['name'];
            }
        }
        let alt = confirm(name + 'を削除します。よろしいですか？');
        if (alt) {
            this.apiPrefix = '/v1';
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.delete('/api_device_groups/?group_id=' + id))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        this.modalMsg = '削除しました。';
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                        this.getGroups();
                        if (id = this.groupId) {
                            $('#deviceTable').jqGrid('clearGridData');
                            this.drawDeviceTable('-1');
                            this.getPanelData('-1');
                        }
                    } else {
                        if (msg) {
                            this.modalMsg = msg;
                            this.closeMsg = '閉じる';
                            this.showAlertModal(this.modalMsg, this.closeMsg);
                        }
                    }
                });
        }
    }
    public groupLogin(id: any) {
        /**
        * @brief show create popup
        * @post refresh table if create successfully
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.modalRef = this.modalService.show(GroupLoginComponent, this.modalConfig);
        let group$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                this.getGroups();
            }
            this.unsubscribe(group$);
        });
    }
    public unsubscribe(res: any) {
        res.unsubscribe();
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        /**
        * @brief show modal dialog
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
