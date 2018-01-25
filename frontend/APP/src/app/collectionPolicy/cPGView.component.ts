import { Component, OnInit, AfterViewInit, ComponentFactory } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
import { CPGDetailComponent } from './cPGDetail.component';
import { CPGActionComponent } from './cPGAction.component';
import { CPGEditComponent } from './cPGEdit.component';
import { CPGLoginComponent } from './cPGLogin.component';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'cpg-view',
    templateUrl: 'cPGView.component.html',
    styleUrls: ['collectionPolicy.component.less']
})
export class CPGViewComponent implements OnInit, AfterViewInit {
    cpgTable$: any;
    apiPrefix: string;
    closeMsg: any;
    modalMsg: any;
    modalRef: BsModalRef;
    cpgInfo: any;
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
        private modalService: BsModalService) {
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
        this.drawCPGTable();
    }
    public drawCPGTable() {
        let _t = this;
        $('#cpgTable').jqGrid({
            url: '/v1/api_collection_policy_group/',
            datatype: 'json',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'policy_group_id', index: 'policy_group_id', search: false, key: true },
                { label: 'コレクションポリシー名', name: 'name', index: 'name', width: 50, align: 'center', search: true },
                { label: '概要', name: 'desc', index: 'desc', width: 50, align: 'center', search: true },
                { label: 'OS Type', name: 'ostypeid', index: 'ostypeid', width: 50, align: 'center', search: true },
                {
                    label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
                    formatter: this.formatterBtn, resizable: false
                }
            ],
            loadComplete(res) {
                console.log(res);
            },
            gridComplete: function () {
                _t.detailBtn();
                _t.editBtn();
                _t.deleteBtn();
            },
            beforeSelectRow: function (rowid, e) { return false; },
            beforeRequest: function () {
                let currentPage: any = $('#cpgTable').jqGrid('getGridParam', 'page');
                let rowNum: any = $('#cpgTable').jqGrid('getGridParam', 'rowNum');
                let records: any = $('#cpgTable').jqGrid('getGridParam', 'records');
                let totalPages = records % rowNum;
                if (records > 0 && currentPage > totalPages) {
                    $('#cpgTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
                }
            },
            pager: '#cpgPager',
            // postData: { 'policy_type': cPType },
            rowNum: 5,
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
                userData: 'status',
                repeatitems: false,
            },
        });
        $('#cpgTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    // btn formatter
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-primary detail" id='
            + rowObject['policy_group_id'] + '><i class="fa fa-info-circle"></i> 確認</button>&nbsp;'
            + '<button class="btn btn-xs btn-success edit" id='
            + rowObject['policy_group_id'] + '><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;'
            + '<button class="btn btn-xs btn-warning delete" id='
            + rowObject['policy_group_id'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    public checkCPGRun(id: any): any {
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url + id)).subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data = _.get(res, 'data');
                if (status && status['status'].toLowerCase() === 'true') {
                    if (data) {
                        return data;
                    }
                } else {
                    if (msg && msg === 'occupation') {
                        this.modalMsg = 'This collection policy is being occupied';
                        this.closeMsg = 'close';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                        return '';
                    }
                }
                return '';
            });
    }
    public detailBtn() {
        let _t = this;
        $('.detail').click(function (event) {
            let id = $(event)[0].target.id;
            if (id && _t.checkCPGRun(id) !== '') {
                _t.modalRef = _t.modalService.show(CPGActionComponent, _t.modalConfig);
                _t.modalRef.content.cpgInfo = _t.checkCPGRun(id);
                this.modalRef.content.actionType = 'edit';
                this.modalRef.content.id = id;
            }
        });
    }
    public editBtn() {
        let _t = this;
        $('.edit').click(function (event) {
            let id = $(event)[0].target.id;
            if (id && _t.checkCPGRun(id) !== '') {
                _t.modalRef = _t.modalService.show(CPGActionComponent, _t.modalConfig);
                _t.modalRef.content.cpgInfo = _t.checkCPGRun(id);
                this.modalRef.content.actionType = 'edit';
                let cpgEdit$ = _t.modalService.onHidden.subscribe(res => {
                    if (res) {
                        _t.cpgTable$.GridUnload();
                        _t.drawCPGTable();
                    }
                    // this used as modal;
                    this.unsubscribe(cpgEdit$);
                });
            }
        });
    }
    public deleteBtn() {
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        $('.delete').click(function (event) {
            event.stopPropagation();
            let id = $(event)[0].target.id;
            let name = $('#cpgTable').jqGrid().getRowData(id)['name'];
            let alt = confirm(name + 'を削除します。よろしいですか？');
            if (alt) {
                _t.httpClient.setUrl(_t.apiPrefix);
                _t.httpClient
                    .toJson(_t.httpClient.delete(url + id))
                    .subscribe(res => {
                        console.log(res);
                        let status = _.get(res, 'status');
                        let msg = _.get(status, 'message');
                        let data = _.get(res, 'data');
                        if (status && status['status'].toLowerCase() === 'true') {
                            this.modalMsg = '削除に成功しました。';
                            this.closeMsg = '閉じる';
                            _t.showAlertModal(this.modalMsg, this.closeMsg);
                            $('#modalButton').on('click', function () {
                                $('#cpgTable').jqGrid().trigger('reloadGrid');
                            });
                        } else {
                            // check this cp occupation, add 'occupation' feedback
                            if (msg && msg === 'POLICY_GROUP_EXIST_IN_SCHEDULE') {
                                this.modalMsg = 'This collection policy is being occupied';
                                this.closeMsg = 'close';
                                _t.showAlertModal(this.modalMsg, this.closeMsg);
                            } else {
                                alert(msg);
                            }
                        }
                    });
            }
        });
    }
    public cpLogin() {
        this.modalRef = this.modalService.show(CPGActionComponent, this.modalConfig);
        this.modalRef.content.actionType = 'login';
        let cpgLogin$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                this.cpgTable$.GridUnload();
                this.drawCPGTable();
            }
            // this.unsubscribe(cpgLogin$);
        });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
