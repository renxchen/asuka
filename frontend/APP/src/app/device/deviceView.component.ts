/**
 * @author: Zizhuang Jiang
 * @contact: zizjiang@cisco.com
 * @file: deviceView.component.ts
 * @time: 2018/03/08
 * @desc: devices summary
 */
import { Component, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
import { ProgressbarComponent } from '../../components/processbar/processbar.component';
import { Observable } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'device-view',
    templateUrl: './deviceView.component.html',
    styleUrls: ['./device.component.less']
})
export class DeviceViewComponent implements OnInit, AfterViewInit {
    apiPrefix: any;
    devViewTable$: any;
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
    constructor(
        public httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private router: Router) { }

    ngOnInit() { }
    ngAfterViewInit() {
        this.drawdevViewTable();
    }
    public drawdevViewTable() {
        /**
        * @brief get data and display it in the grid
        * @pre called after the Dom has been ready
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        let _t = this;
        _t.devViewTable$ = $('#devViewTable').jqGrid({
            url: '/v1/api_device/',
            datatype: 'JSON',
            mtype: 'get',
            colNames: ['DeviceId', 'Hostname', 'IP Address', 'Telnet Port', 'SNMP Port', 'SNMP Community',
                'SNMP Version', 'Login Expect', 'Device Type', 'Ostype', 'Group', 'Telnet Status', 'SNMP Status'
            ],
            colModel: [
                { hidden: true, name: 'devices_id', index: 'devices_id', search: false, key: true },
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
                    name: 'ostype_name', index: 'ostype_name', width: 50, align: 'center', search: true
                },
                // { name: 'group', index: 'group', width: 50, align: 'center', search: true },
                {
                    name: 'group_list', index: 'group_list', width: 50, align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                { name: 'telnet_status', index: 'telnet_status', width: 50, align: 'center', search: true },
                { name: 'snmp_status', index: 'status_type', width: 50, align: 'center', search: true },
            ],
            // beforeRequest: function () {
            //     let currentPage: any = $('#devViewTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#devViewTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#devViewTable').jqGrid('getGridParam', 'records');
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         $('#devViewTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
            gridComplete: function () {
                $('.ui-jqgrid tr.jqgrow td').css({ 'white-space': 'nowrap', 'text-overflow': 'ellipsis' });
            },
            loadComplete: function (res) {
                let status = _.get(_.get(res, 'status'), 'status');
                let code: any = _.get(_.get(res, 'status'), 'code');
                let msg: any = _.get(_.get(res, 'status'), 'message');
                if (status === 'False') {
                    if (code === 102 || code === 103) {
                        localStorage.setItem('sessionTimeOut', msg);
                        _t.router.navigate(['/login/']);
                    }
                }
            },
            pager: '#devViewPager',
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 350,
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
        $('#devViewTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    public noDataFormatter(cellvalue, options, rowObject) {
        /**
        * @brief format the data
        * @param cellvalue: value of the cell;
                  options:includes attributes such as RowId,colModel;
                  rowObject:json data of the row
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        if (cellvalue === null || cellvalue === '') {
            return '-';
        } else {
            return cellvalue;
        }
    }
    public deviceCheck() {
        /**
        * @brief status check
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.apiPrefix = '/v1';
        let checkUrl = '/api_device/';
        let deviceSel: any = [];
        deviceSel = $('#devViewTable').jqGrid('getGridParam', 'selarrrow');
        let checkInfo: any = {};
        checkInfo['id_list'] = deviceSel;
        if (deviceSel.length > 0) {
            this.processbar = this.modalService.show(ProgressbarComponent, this.modalConfig);
            this.processbar.content.message = 'Checking...';
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(checkUrl, checkInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        $('.modal').hide();
                        this.devViewTable$.GridUnload();
                        this.drawdevViewTable();
                    } else {
                        $('.modal').hide();
                        if (msg) {
                            this.modalMsg = msg;
                            this.closeMsg = '閉じる';
                            this.showAlertModal(this.modalMsg, this.closeMsg);
                        }
                    }
                });
        } else {
            this.modalMsg = 'Please choose one device at least.';
            this.closeMsg = '閉じる';
            this.showAlertModal(this.modalMsg, this.closeMsg);
        }
    }
    public CSVExport() {
        window.location.href = '/v1/api_device/export';
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
