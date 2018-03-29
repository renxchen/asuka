import { Component, OnInit, AfterViewInit, TemplateRef } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Http } from '@angular/http';
import { Router } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
import { DeviceErrorTableComponent } from './deviceErrorTable.component';
import { ProgressbarComponent } from '../../components/processbar/processbar.component';
import { Observable } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'device-loign',
    templateUrl: './deviceLogin.component.html',
    styleUrls: ['./device.component.less']
})
export class DeviceLoginComponent implements OnInit {
    filename: any;
    devLoginTable$: any;
    apiPrefix: any;
    uploadFlg: string;
    errorDevices: any;
    optId: any;
    loginFlg: Boolean = true;
    actionFlg: Boolean = true;
    formData: FormData;
    modalRef: BsModalRef;
    processbar: BsModalRef;
    closeMsg: any;
    modalMsg: any;
    modalConfig = {
        animated: true,
        keyboard: false,
        backdrop: true,
        ignoreBackdropClick: true,
        class: 'modal-md'
    };
    modalConfigLg = {
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
        private http: Http
    ) { }

    ngOnInit() {
        this.uploadFlg = 'null';
    }
    public changeFile(files: FileList) {
        if (files && files.length > 0) {
            let file: File = files.item(0);
            let fileType = file.type;
            this.filename = file.name;
            this.formData = new FormData();
            this.formData.append('file', file);
            // if (fileType === 'application/vnd.ms-excel') {
            if (this.filename.indexOf('.csv') > -1) {
                this.uploadFlg = 'csv';
                this.loginFlg = false;
            } else {
                this.uploadFlg = 'other';
                this.loginFlg = true;
            }
        } else {
            if (this.filename) {
                this.loginFlg = false;
            } else {
                this.loginFlg = true;
            }
        }
    }
    public uploadFile() {
        if (this.devLoginTable$) {
            this.devLoginTable$.GridUnload();
            // $('#devLoginTable').jqGrid('clearGridData');
        }
        this.processbar = this.modalService.show(ProgressbarComponent, this.modalConfig);
        this.processbar.content.message = 'Uploading...';
        this.http.post('/v1/api_device/upload', this.formData)
            .map(res => res.json())
            .catch(error => Observable.throw(error))
            .subscribe(res => {
                // this.modalRef.hide();
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data: any = _.get(res, 'error_list');
                this.optId = _.get(res, 'operation_id');
                if (status && status['status'].toLowerCase() === 'true') {
                    // $('#devLoginTable').trigger('reloadGrid');
                    this.processbar.hide();
                    this.drawDevLoginTable();
                    this.actionFlg = false;
                    if (data && data.length > 0) {
                        this.modalRef = this.modalService.show(DeviceErrorTableComponent, this.modalConfigLg);
                        this.modalRef.content.closeMsg = '閉じる';
                        this.errorDevices = data;
                        this.modalRef.content.data = this.errorDevices;
                    }
                } else {
                    this.processbar.hide();
                    this.actionFlg = true;
                    alert(msg);
                }
            });
    }
    public drawDevLoginTable() {
        let _t = this;
        _t.devLoginTable$ = $('#devLoginTable').jqGrid({
            url: '/v1/api_device_pre/?operation_id=' + this.optId,
            datatype: 'JSON',
            mtype: 'get',
            colNames: ['DeviceId', 'Hostname', 'IP Address', 'Telnet Port', 'SNMP Port', 'SNMP Community',
                'SNMP Version', 'Login Expect', 'Device Type', 'Ostype', 'Group', 'Telnet Status', 'SNMP Status'
            ],
            colModel: [
                { hidden: true, name: 'device_id', index: 'device_id', search: false, key: true },
                { name: 'hostname', index: 'hostname', width: 40, align: 'center', search: true },
                { name: 'ip', index: 'ip', width: 50, align: 'center', search: true },
                { name: 'telnet_port', index: 'telnet_port', width: 50, align: 'center', search: true },
                { name: 'snmp_port', index: 'snmp_port', width: 50, align: 'center', search: true },
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
                { name: 'device_type', index: 'device_type', width: 50, align: 'center', search: true },
                {
                    name: 'ostype', index: 'ostype', width: 50, align: 'center', search: true,
                    formatter: function (cellvalue, options, rowObject) {
                        return cellvalue['name'];
                    }
                },
                {
                    name: 'group_name', index: 'group_name', width: 50, align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                { name: 'telnet_status', index: 'telnet_status', width: 50, align: 'center', search: true },
                { name: 'snmp_status', index: 'status_type', width: 50, align: 'center', search: true },
            ],
            // beforeSelectRow: function (rowid, e) { return false; },
            // beforeRequest: function () {
            //     let currentPage: any = $('#devLoginTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#devLoginTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#devLoginTable').jqGrid('getGridParam', 'records');
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         $('#devLoginTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
            // text-overflow: ellipsis;
            pager: '#devLoginPager',
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 330,
            viewrecords: false,
            multiselect: true,
            emptyrecords: 'There is no data to display',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                repeatitems: false,
            },
        });
        $('#devLoginTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    public noDataFormatter(cellvalue, options, rowObject) {
        if (cellvalue === null || cellvalue === '') {
            return '-';
        } else {
            return cellvalue;
        }
    }
    public deviceCheck() {
        this.apiPrefix = '/v1';
        let checkUrl = '/api_device_pre/';
        let deviceSel: any = [];
        deviceSel = $('#devLoginTable').jqGrid('getGridParam', 'selarrrow');
        let checkInfo: any = {};
        checkInfo['id_list'] = deviceSel;
        checkInfo['operation_id'] = this.optId;
        if (deviceSel.length > 0) {
            this.processbar = this.modalService.show(ProgressbarComponent, this.modalConfig);
            this.processbar.content.message = 'Check...';
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(checkUrl, checkInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    if (status && status['status'].toLowerCase() === 'true') {
                        this.devLoginTable$.GridUnload();
                        this.drawDevLoginTable();
                        // $('#devLoginTable').jqGrid('clearGridData');
                        // $('#devLoginTable').trigger('reloadGrid');
                        this.processbar.hide();
                    } else {
                        this.processbar.hide();
                        alert('Status check failed.');
                    }
                });
        } else {
            alert('Please choose one device at least.');
        }
    }
    // save to database;
    public deviceLogin() {
        this.apiPrefix = '/v1';
        let databaseUrl = '/api_device/';
        let loginInfo: any = {};
        loginInfo['operation_id'] = this.optId;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.post(databaseUrl, loginInfo))
            .subscribe(res => {
                let status = _.get(res, 'status');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    this.router.navigate(['index/deviceview/']);
                } else {
                    alert('Save failed.');
                }
            });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
