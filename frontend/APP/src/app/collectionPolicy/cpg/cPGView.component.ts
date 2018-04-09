/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: cPGView.component.ts
* @time: 2018/03/13
* @desc: collection policy group summary
*/

import { Component, OnInit, AfterViewInit, ComponentFactory } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Router } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
import { CPGDetailComponent } from './cPGDetail.component';
import { CPGEditComponent } from './cPGEdit.component';
import { CPGLoginComponent } from './cPGLogin.component';
import { Subscription } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'cpg-view',
    templateUrl: './cPGView.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})
export class CPGViewComponent implements OnInit, AfterViewInit {
    cpgTable$: any;
    apiPrefix: string;
    closeMsg: any;
    modalMsg: any;
    modalRef: BsModalRef;
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
        /**
        * @brief get data and display it in the grid
        * @pre called after the Dom has been ready
        * @author Dan Lv
        * @date 2018/03/13
        */
        let _t = this;
        this.cpgTable$ = $('#cpgTable').jqGrid({
            url: '/v1/api_collection_policy_group/',
            datatype: 'json',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'policy_group_id', index: 'policy_group_id', search: false, key: true },
                { label: 'コレクションポリシーグループ名', name: 'name', index: 'name', width: 50, align: 'center', search: true },
                { label: 'OS Type', name: 'ostypeid__name', index: 'ostypeid__name', width: 50, align: 'center', search: true },
                { label: '概要', name: 'desc', index: 'desc', width: 50, align: 'center', search: true, formatter: _t.noDataFormatter },
                {
                    label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
                    formatter: _t.formatterBtn, resizable: false, sortable: false
                }
            ],
            gridComplete: function () {
                $('.ui-jqgrid tr.jqgrow td').css({ 'white-space': 'nowrap', 'text-overflow': 'ellipsis' });
                _t.detailBtn();
                _t.editBtn();
                _t.deleteBtn();
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
            beforeSelectRow: function (rowid, e) { return false; },
            // beforeRequest: function () {
            //     let currentPage: any = $('#cpgTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#cpgTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#cpgTable').jqGrid('getGridParam', 'records');
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         $('#cpgTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
            pager: '#cpgPager',
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 350,
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
        $('#cpgTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    // btn formatter
    public formatterBtn(cellvalue, options, rowObject) {
        /**
         * @brief format the action buttons
         * @param cellvalue: value of the cell;
                  options:includes attributes such as RowId,colModel;
                  rowObject:json data of the row
         * @pre called during calling the function of drawCPTable
         * @return renturn action buttons with rowId
         * @author Dan Lv
         * @date 2018/03/13
         */
        return '<button class="btn btn-xs btn-primary detail" id='
            + rowObject['policy_group_id'] + '><i class="fa fa-info-circle"></i> 確認</button>&nbsp;'
            + '<button class="btn btn-xs btn-success edit" id='
            + rowObject['policy_group_id'] + '><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;'
            + '<button class="btn btn-xs btn-warning delete" id='
            + rowObject['policy_group_id'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    // no data formatter
    public noDataFormatter(cellvalue, options, rowObject) {
        if (cellvalue === null || cellvalue === '') {
            return '-';
        } else {
            return cellvalue;
        }
    }
    public detailBtn() {
        /**
        * @brief get the collection policy group id and jump to detail page
        * @author Dan Lv
        * @date 2018/03/13
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        $('.detail').click(function (event) {
            let detaiId = $(event)[0].target.id;
            if (detaiId) {
                _t.router.navigate(['/index/cpgdetail'],
                    { queryParams: { 'id': detaiId } });
            }
            event.stopPropagation();
        });
    }
    public editBtn() {
        /**
        * @brief get the collection policy group id and jump to edit page
        * @author Dan Lv
        * @date 2018/03/13
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        $('.edit').click(function (event) {
            let editId = $(event)[0].target.id;
            if (editId) {
                _t.router.navigate(['/index/cpgedit'],
                    { queryParams: { 'id': editId } });
            }
            event.stopPropagation();
        });
    }
    public deleteBtn() {
        /**
        * @brief get the collection policy group id and delete this collection policy group
        * @post reload cpgTable if delete sucessfully
        * @author Dan Lv
        * @date 2018/03/13
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy_group/?id=';
        $('.delete').click(function (event) {
            let delId = $(event)[0].target.id;
            if (delId) {
                let delName = $('#cpgTable').jqGrid().getRowData(delId)['name'];
                let alt = confirm(delName + 'を削除します。よろしいですか？');
                if (alt) {
                    _t.httpClient.setUrl(_t.apiPrefix);
                    _t.httpClient
                        .toJson(_t.httpClient.delete(url + delId))
                        .subscribe(res => {
                            let status = _.get(res, 'status');
                            let msg = _.get(status, 'message');
                            let data = _.get(res, 'data');
                            if (status && status['status'].toString().toLowerCase() === 'true') {
                                _t.modalMsg = '削除に成功しました。';
                                _t.closeMsg = '閉じる';
                                _t.showAlertModal(_t.modalMsg, _t.closeMsg);
                                $('#modalButton').on('click', function () {
                                    $('#cpgTable').jqGrid('clearGridData');
                                    $('#cpgTable').trigger('reloadGrid');
                                    // $('#cpgTable').jqGrid().trigger('reloadGrid');
                                });
                            } else {
                                if (msg) {
                                    _t.modalMsg = msg;
                                    _t.closeMsg = '閉じる';
                                    _t.showAlertModal(_t.modalMsg, _t.closeMsg);
                                }
                            }
                        });
                }
            }
            event.stopPropagation();
        });
    }
    public cpgLogin() {
        /**
        * @brief show cpgLogin Popup
        * @post reload cpgTable after receiving the returned data
        * @author Dan Lv
        * @date 2018/03/13
        */
        this.modalRef = this.modalService.show(CPGLoginComponent, this.modalConfig);
        let cpgLogin$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                // this.cpgTable$.GridUnload();
                // this.drawCPGTable();
                $('#cpgTable').jqGrid('clearGridData');
                $('#cpgTable').trigger('reloadGrid');
            }
            this.unsubscribe(cpgLogin$);
        });
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
    public unsubscribe(res: any) {
        res.unsubscribe();
    }
}
