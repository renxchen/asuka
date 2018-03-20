/**
 * @author: Dan Lv
 * @contact: danlv@cisco.com
 * @file: cPView.component.ts
 * @time: 2018/01/23
 * @desc: collection policy summary
 */
import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router, ActivatedRoute } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
import * as _ from 'lodash';
declare var $: any;
@Component({
    selector: 'cp-view',
    templateUrl: './cPView.component.html',
    styleUrls: ['./collectionPolicy.component.less']
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
        private activedRoute: ActivatedRoute,
        private modalService: BsModalService
    ) { }
    ngOnInit() {
    }
    ngAfterViewInit() {
        let cPTypeTmp: any = this.activedRoute.snapshot.queryParams['cptype'];
        if (cPTypeTmp && typeof (cPTypeTmp) !== 'undefined') {
            this.cPType = cPTypeTmp;
            this.drawCPTable('OID', 'snmp_oid', this.cPType);
        } else {
            this.cPType = '0';
            this.drawCPTable('show コマンド', 'cli_command', this.cPType);
        }
    }
    public formatterBtn(cellvalue, options, rowObject) {
        /**
         * @brief format the action buttons
         * @param cellvalue: value of the cell;
                  options:includes attributes such as RowId,colModel;
                  rowObject:json data of the row
         * @pre called during calling the function of drawCPTable
         * @return renturn action buttons with rowId
         * @author Dan Lv
         * @date 2018/01/23
         */
        return '<button class="btn btn-xs btn-primary detail" id='
            + rowObject['coll_policy_id'] + '><i class="fa fa-info-circle"></i> 確認</button>&nbsp;'
            + '<button class="btn btn-xs btn-success edit" id='
            + rowObject['coll_policy_id'] + '><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;'
            + '<button class="btn btn-xs btn-warning delete" id='
            + rowObject['coll_policy_id'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    // no data formatter
    public noDataFormatter(cellvalue, options, rowObject) {
        if (cellvalue === null || cellvalue === '') {
            return '-';
        } else {
            return cellvalue;
        }
    }
    public changeCPType(event) {
        /**
         * @brief used to switch button
         * @param event:data of the click event
         * @author Dan Lv
         * @date 2018/01/23
         */
        event.stopPropagation();
        this.cPType = $(event.target).val();
        if (this.cPType === '0') {
            this.cPTable.GridUnload();
            this.drawCPTable('show コマンド', 'cli_command', this.cPType);
        } else {
            this.cPTable.GridUnload();
            this.drawCPTable('OID', 'snmp_oid', this.cPType);
        }
    }
    public drawCPTable(thirdCol?: any, thirdName?: any, cPType?: any) {
        /**
        * @brief get data and display it in the grid
        * @param thirdCol:the label of the grid;
                 thirdName:the third name of the grid;
                 cpType：the type of collection policy
        * @pre called after the Dom has been ready
        * @author Dan Lv
        * @date 2018/01/23
        */
        let _t = this;
        _t.cPTable = $('#cpTable').jqGrid({
            url: '/v1/api_collection_policy/',
            datatype: 'JSON',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'coll_policy_id', index: 'coll_policy_id', search: false, key: true },
                { label: 'コレクションポリシー名', name: 'name', index: 'name', width: 50, align: 'center', search: true },
                { label: 'OS Type', name: 'ostype__name', index: 'ostype__name', width: 50, align: 'center', search: true },
                { label: thirdCol, name: thirdName, index: thirdName, width: 50, align: 'center', search: true },
                {
                    abel: '概要', name: 'desc', index: 'desc', width: 50, align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                {
                    label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
                    formatter: _t.formatterBtn, resizable: false
                }
            ],
            gridComplete: function () {
                _t.detailBtn();
                _t.editBtn();
                _t.deleteBtn();
            },
            loadComplete: function (res) {
                let code = _.get(_.get(res, 'new_token'), 'code');
                if (code === 102) {
                    alert('Signature has expired,please login again.');
                    _t.router.navigate(['/login/']);
                }
                if (code === 103) {
                    alert('This user is not authorized to access, please login again.');
                    _t.router.navigate(['/login/']);
                }
            },
            beforeSelectRow: function (rowid, e) { return false; },
            // beforeRequest: function () {
            //     let currentPage: any = $('#cpTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#cpTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#cpTable').jqGrid('getGridParam', 'records');
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         $('#cpTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
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
        /**
        * @brief get the collection policy id and jump to detail page
        * @author Dan Lv
        * @date 2018/01/23
        */
        let _t = this;
        $('.detail').click(function (event) {
            let detailId = $(event)[0].target.id;
            if (detailId) {
                if (_t.cPType === '0') {
                    _t.router.navigate(['/index/clicpdetail'],
                        { queryParams: { 'id': detailId } });
                } else {
                    _t.router.navigate(['/index/snmpcpdetail'],
                        { queryParams: { 'id': detailId } });
                }
            }
            event.stopPropagation();
        });
    }
    public editBtn() {
        /**
        * @brief get the collection policy id and jump to edit page
        * @author Dan Lv
        * @date 2018/01/23
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        $('.edit').click(function (event) {
            let editId = $(event)[0].target.id;
            if (editId) {
                if (_t.cPType === '0') {
                    _t.router.navigate(['/index/clicpedit'],
                        { queryParams: { 'id': editId } });
                } else {
                    _t.router.navigate(['/index/snmpcpedit'],
                        { queryParams: { 'id': editId } });
                }
            }
            event.stopPropagation();
        });
    }
    public deleteBtn() {
        /**
        * @brief get the collection policy id and delete this collection policy
        * @post must call the function of drawCPTable to refresh gird if delete sucessfully
        * @author Dan Lv
        * @date 2018/01/23
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy/';
        $('.delete').click(function (event) {
            let delId = $(event)[0].target.id;
            if (delId) {
                let delIdname = $('#cpTable').jqGrid().getRowData(delId)['name'];
                let alt = confirm(delIdname + 'を削除します。よろしいですか？');
                if (alt) {
                    _t.httpClient.setUrl(_t.apiPrefix);
                    _t.httpClient
                        .toJson(_t.httpClient.delete(url + '?id=' + delId))
                        .subscribe(res => {
                            let status = _.get(res, 'status');
                            let msg: any = _.get(status, 'message');
                            let data = _.get(res, 'data');
                            if (status && status['status'].toLowerCase() === 'true') {
                                this.modalMsg = '削除しました。';
                                this.closeMsg = '閉じる';
                                _t.showAlertModal(this.modalMsg, this.closeMsg);
                                $('#modalButton').on('click', function () {
                                    $('#cpTable').jqGrid().trigger('reloadGrid');
                                });
                            } else {
                                if (msg && msg === 'COLL_POLICY_EXIST_IN_POLICYS_GROUPS') {
                                    this.modalMsg = 'Can not be deteted when collection policy exits in policy group';
                                    this.closeMsg = 'close';
                                    _t.showAlertModal(this.modalMsg, this.closeMsg);
                                } else {
                                    if (msg) {
                                        alert(msg);
                                    }
                                }
                            }
                        });
                }
            }
            event.stopPropagation();
        });
    }
    public cpLogin() {
        /**
        * @brief get the type of collection policy and jump to login page
        * @author Dan Lv
        * @date 2018/01/23
        */
        if (this.cPType === '0') {
            this.router.navigate(['/index/clicplogin'],
                { queryParams: { 'cPType': parseInt(this.cPType, 0) } });
        } else {
            this.router.navigate(['/index/snmpcplogin'],
                { queryParams: { 'cPType': parseInt(this.cPType, 0) } });
        }
    }
    public showAlertModal(modalMsg?: any, closeMsg?: any, data?: any) {
        /**
        * @brief show modal dialog
        * @author Dan Lv
        * @date 2018/01/23
        */
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
        this.modalRef.content.data = data;
    }
}
