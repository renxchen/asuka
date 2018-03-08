import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
import { Observable } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'device-view',
    templateUrl: './deviceView.component.html',
    styleUrls: ['./device.component.less']
})
export class DeviceViewComponent implements OnInit {
    /*
    @brief 函数简要说明
    @param 参数名 参数的意思和用户
    @pre 代码使用前条件
    @post 代码使用后条件
    @note 备注
    @return 返回值
    @author Zizhuang Jiang
    @date 03/08/2018
     */
    apiPrefix: any;
    devViewTable$: any;
    constructor(
        public httpClient: HttpClientComponent,
        private modalService: BsModalService) { }

    ngOnInit() {
        this.drawdevViewTable();
    }

    public drawdevViewTable() {
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
                { name: 'snmp_community', index: 'snmp_community', width: 50, align: 'center', search: true },
                { name: 'snmp_version', index: 'snmp_version', width: 50, align: 'center', search: true },
                {
                    name: 'login_expect', index: 'login_expect', width: 50, align: 'center', search: true,
                    // formatter: _t.loginExpFormmater
                },
                { name: 'device_type', index: 'device_type', width: 50, align: 'center', search: true },
                { name: 'ostype_name', index: 'ostype_name', width: 50, align: 'center', search: true
                },
                // { name: 'group', index: 'group', width: 50, align: 'center', search: true },
                { name: 'group_list', index: 'group_list', width: 50, align: 'center', search: true },
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
            pager: '#devViewPager',
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
                // userData:'erroList',
                repeatitems: false,
            },
        });
        $('#devViewTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    public deviceCheck() {
        this.apiPrefix = '/v1';
        let checkUrl = '/api_device/';
        let deviceSel: any = [];
        deviceSel = $('#devViewTable').jqGrid('getGridParam', 'selarrrow');
        alert(deviceSel);
        let checkInfo: any = {};
        checkInfo['id_list'] = deviceSel;
        if (deviceSel.length > 0) {
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(checkUrl, checkInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    console.log(res);
                    if (status && status['status'].toLowerCase() === 'true') {
                        this.devViewTable$.GridUnload();
                        this.drawdevViewTable();
                    } else {
                        alert('msg');
                    }
                });
        } else {
            alert('no device selected');
        }
    }
    public CSVExport() {

    }
}
