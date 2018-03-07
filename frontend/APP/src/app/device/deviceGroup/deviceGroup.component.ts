import { Component, OnInit, AfterViewInit, TemplateRef } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Router } from '@angular/router';
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
export class DeviceGroupComponent implements OnInit {
    groupId: any;
    name: any;
    desc: any;
    osType: any;
    osTypeId: any;
    deviceTable$: any;
    apiPrefix: any;
    groups: any = [];
    modalRef: any;
    groupData = [{ 'group_id': 1, 'name': 'group1' },
    { 'group_id': 2, 'name': 'group2' },
    { 'group_id': 3, 'name': 'group3' },
    { 'group_id': 4, 'name': 'group4' }];
    modalConfig = {
        animated: true,
        keyboard: false,
        backdrop: true,
        ignoreBackdropClick: true,
        class: 'modal-md'
    };
    constructor(
        public httpClient: HttpClientComponent,
        private modalService: BsModalService) { }
    ngOnInit() {
        // this.groups = this.groupData;
        this.getGroups();
        this.drawDeviceTable('-1');
        this.getPanelData('-1');

    }
    public drawDeviceTable(id: any) {
        let _t = this;
        _t.deviceTable$ = $('#deviceTable').jqGrid({
            // api
            url: '/v1/api_device/?group_id=' + id,
            datatype: 'JSON',
            mtype: 'get',
            colNames: ['GroupId', 'Hostname', 'IP Address', 'Telnet Port', 'SNMP Port', 'SNMP Community',
                'SNMP Version', 'Login Expect', 'Device Type', 'Telnet Status', 'SNMP Status'
            ],
            colModel: [
                { hidden: true, name: 'group_id', index: 'group_id', search: false, key: true },
                { name: 'hostname', index: 'hostname', width: 50, align: 'center', search: true },
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
                { name: 'telnet_status', index: 'telnet_status', width: 50, align: 'center', search: true },
                { name: 'snmp_status', index: 'status_type', width: 50, align: 'center', search: true },
            ],
            beforeSelectRow: function (rowid, e) { return false; },
            onPaging: function () {
                let currentPage: any = $('#deviceTable').jqGrid('getGridParam', 'page');
                let rowNum: any = $('#deviceTable').jqGrid('getGridParam', 'rowNum');
                let records: any = $('#deviceTable').jqGrid('getGridParam', 'records');
                let totalPages = records % rowNum;
                if (records > 0 && currentPage > totalPages) {
                    $('#deviceTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
                }
            },
            // text-overflow: ellipsis;
            pager: '#devicePager',
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 340,
            viewrecords: false,
            emptyrecords: 'There is no data to display',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                // userData: 'status',
                repeatitems: false,
            },
        });
        $('#deviceTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
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
                if (status && status['status'].toLowerCase() === 'true') {
                    if (data) {
                        this.groups = data;
                    }
                } else {
                    if (msg) {
                        alert(msg);
                    }
                }
            });
    }
    public getPanelData(id: any) {
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
                if (status && status['status'].toLowerCase() === 'true') {
                    if (data && data.length > 0) {
                        this.name = _.get(data[0], 'name');
                        this.osType = _.get(_.get(data[0], 'ostype'), 'name');
                        this.desc = _.get(data[0], 'desc');
                    }
                } else {
                    if (msg) {
                        alert(msg);
                    }
                }
            });
    }

    // click事件
    public getGroupInfo(id: any) {
        // event.preventDefault();
        // let id = event.target.id;
        console.log(id);
        this.deviceTable$.GridUnload();
        if (id) {
            this.getPanelData(id);
            this.drawDeviceTable(id);
        }
    }
    public editGroup(id: any) {
        // event.preventDefault();
        // let id = event.target.id;
        console.log(id);
        this.modalRef = this.modalService.show(GroupEditComponent, this.modalConfig);
        this.modalRef.content.id = id;
        let group$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                this.getGroups();
            }
            this.unsubscribe(group$);
        });
    }
    public deleteGroup(id: any) {
        // event.preventDefault();
        // let id = event.target.id;
        console.log(id);
        let name: any;
        console.log(this.groups);
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
                    if (status && status['status'].toLowerCase() === 'true') {
                        alert('Delete successfully');
                        this.getGroups();
                    } else {
                        if (msg) {
                            alert(msg);
                        }
                    }
                });
        }
    }
    public groupLogin(id: any) {
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
}
