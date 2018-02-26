import { Component, OnInit, AfterViewInit, TemplateRef } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
import * as _ from 'lodash';
declare var $: any;
@Component({
    selector: 'cp-view',
    templateUrl: './cPView.component.html',
    styleUrls: ['collectionPolicy.component.less']
})
export class CPViewComponent implements OnInit, AfterViewInit {
    cPType: any;
    thirdCol: any;
    thirdName: any;
    apiPrefix: string;
    modalRef: BsModalRef;
    closeMsg: any;
    modalMsg: any;
    cPTable: any;
    modalConfig = {
        animated: true,
        keyboard: false,
        backdrop: true,
        ignoreBackdropClick: true,
        class: 'modal-lg'
    };
    constructor(
        private httpClient: HttpClientComponent,
        private router: Router,
        private modalService: BsModalService
    ) { }
    ngOnInit() {
        this.cPType = '0';
    }
    ngAfterViewInit() {
        this.drawCPTable('コマンド', 'cli_command', this.cPType);
    }
    // btn formatter
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-primary detail" id='
            + rowObject['coll_policy_id'] + '><i class="fa fa-info-circle"></i> 確認</button>&nbsp;'
            + '<button class="btn btn-xs btn-success edit" id='
            + rowObject['coll_policy_id'] + '><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;'
            + '<button class="btn btn-xs btn-warning delete" id='
            + rowObject['coll_policy_id'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    // change the type of policy
    public changeCPType(event) {
        event.stopPropagation();
        this.cPType = $(event.target).val();
        if (this.cPType === '0') {
            this.cPTable.GridUnload();
            this.drawCPTable('コマンド', 'cli_command', this.cPType);
        } else {
            this.cPTable.GridUnload();
            this.drawCPTable('OID', 'snmp_oid', this.cPType);
        }
    }
    // init table
    public drawCPTable(thirdCol?: any, thirdName?: any, cPType?: any) {
        let _t = this;
        _t.cPTable = $('#cpTable').jqGrid({
            url: '/v1/api_collection_policy/',
            datatype: 'JSON',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'coll_policy_id', index: 'coll_policy_id', search: false, key: true },
                { label: 'コレクションポリシー名', name: 'name', index: 'name', width: 50, align: 'center', search: true },
                { label: 'OS Type', name: 'ostype_name', index: 'ostype', width: 50, align: 'center', search: true },
                { label: thirdCol, name: thirdName, index: thirdName, width: 50, align: 'center', search: true },
                { label: '概要', name: 'desc', index: 'desc', width: 50, align: 'center', search: true },
                {
                    label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
                    formatter: this.formatterBtn, resizable: false
                }
            ],
            gridComplete: function () {
                _t.detailBtn();
                _t.editBtn();
                _t.deleteBtn();
            },
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
            pager: '#cpPager',
            postData: { 'policy_type': cPType },
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 340,
            viewrecords: false,
            emptyrecords: 'There is no data to display',
            jsonReader: {
                root: 'data.data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });
        $('#cpTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }

    public detailBtn() {
        let _t = this;
        $('.detail').click(function (event) {
            let id = $(event)[0].target.id;
            if (_t.cPType === '0') {
                _t.router.navigate(['/index/clicpdetail'],
                    { queryParams: { 'id': id } });
            } else {
                _t.router.navigate(['/index/snmpcpdetail'],
                    { queryParams: { 'id': id } });
            }
        });
    }
    public editBtn() {
        let _t = this;
        _t.apiPrefix = '/v1';
        // let url = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        $('.edit').click(function (event) {
            let id = $(event)[0].target.id;
            // _t.httpClient.setUrl(_t.apiPrefix);
            // _t.httpClient
            //     .toJson(_t.httpClient.get(url + '?id=' + id))
            //     .subscribe(res => {
            //         if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
            if (_t.cPType === '0') {
                _t.router.navigate(['/index/clicpedit'],
                    { queryParams: { 'id': id } });
            } else {
                _t.router.navigate(['/index/snmpcpedit'],
                    { queryParams: { 'id': id } });
            }
            // } else {
            //     if (res['status'] && res['status']['message']) {
            //                 alert(res['status']['message']);
            //             }
            // check this cp occupation, add 'occupation' feedback
            // if (res['status']['message'] && res['status']['message'] === 'occupation') {
            //     this.modalMsg = 'This collection policy is being occupied';
            //     this.closeMsg = 'close';
            //     _t.showAlertModal(this.modalMsg, this.closeMsg);
            // } else {
            //     if (res['status'] && fres['status']['message']) {
            //         alert(res['status']['message']);
            //     }
            // }
            // }
            // });
        });
    }
    public deleteBtn() {
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy/';
        $('.delete').click(function (event) {
            event.stopPropagation();
            let id = $(event)[0].target.id;
            let name = $('#cpTable').jqGrid().getRowData(id)['name'];
            let alt = confirm(name + 'を削除します。よろしいですか？');
            if (alt) {
                _t.httpClient.setUrl(_t.apiPrefix);
                _t.httpClient
                    .toJson(_t.httpClient.delete(url + '?id=' + id))
                    .subscribe(res => {
                        console.log('res', res);
                        let status = _.get(res, 'status');
                        let msg: any = _.get(status, 'message');
                        let data = _.get(res, 'data');
                        if (status && status['status'].toLowerCase() === 'true') {
                            this.modalMsg = '削除に成功しました。';
                            this.closeMsg = '閉じる';
                            _t.showAlertModal(this.modalMsg, this.closeMsg);
                            $('#modalButton').on('click', function () {
                                $('#cpTable').jqGrid().trigger('reloadGrid');
                            });
                        } else {
                            // check this cp occupation, add 'occupation' feedback
                            if (msg && msg === 'COLL_POLICY_EXIST_IN_POLICYS_GROUPS') {
                                // let msgTmp = msg.split('_IN_')[1].toLowerCase();
                                // console.log(msg, msgTmp);
                                this.modalMsg = 'Can not be deteted when collection policy exits in policy group';
                                this.closeMsg = 'close';
                                _t.showAlertModal(this.modalMsg, this.closeMsg);
                            } else {
                                if (res['status'] && res['status']['message']) {
                                    alert(res['status']['message']);
                                }
                            }
                        }
                    });
            }
        });
    }
    public cpLogin() {
        if (this.cPType === '0') {
            this.router.navigate(['/index/clicplogin'],
                { queryParams: { 'cPType': parseInt(this.cPType, 0) } });
        } else {
            this.router.navigate(['/index/snmpcplogin'],
                { queryParams: { 'cPType': parseInt(this.cPType, 0) } });
        }
    }
    public loadCompleteFun(res) {
        if (res && !res['data']) {
            if (res['new_token']) {
                let code = res['new_token']['code'];
                if (code === 1023) {
                    alert('用户过期，请重新登录');
                    this.router.navigate(['/login']);
                } else if (code === 103) {
                    alert('该用户无权访问，请重新登录');
                    this.router.navigate(['/login']);
                }
            }
        }
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
