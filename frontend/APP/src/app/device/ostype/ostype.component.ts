/**
 * @author: Zizhuang Jiang
 * @contact: zizjiang@cisco.com
 * @file: ostype.component.ts
 * @time: 2018/03/08
 * @desc: ostype summary
 */
import { Component, OnInit, AfterViewInit, OnDestroy, ComponentFactory } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Router } from '@angular/router';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
import { OstypeLoginComponent } from './ostypeLogin.component';
import { OstypeEditComponent } from './ostypeEdit.component';
import { Subscription } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'ostype',
    templateUrl: './ostype.component.html',
    styleUrls: ['.././device.component.less']
})
export class OstypeComponent implements OnInit, AfterViewInit, OnDestroy {
    ostypeTable$: any;
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
        this.drawOstypeTable();
    }
    public drawOstypeTable() {
        /**
        * @brief get data and display it in the grid
        * @pre called after the Dom has been ready
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        let _t = this;
        _t.ostypeTable$ = $('#ostypeTable').jqGrid({
            url: '/v1/api_device_ostype/',
            datatype: 'json',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'ostypeid', index: 'ostypeid', search: false, key: true },
                { label: 'OS Type名', name: 'name', index: 'name', align: 'center', search: true },
                {
                    label: '概要', name: 'desc', index: 'desc', align: 'center', search: true,
                    formatter: _t.noDataFormatter
                },
                {
                    label: 'CLI情報取得前<br/>デフォルト実行コマンド', name: 'start_default_commands',
                    index: 'start_default_commands', align: 'left', search: true, formatter: _t.brFormatter
                },
                {
                    label: 'CLI情報取得完了後<br/>デフォルト実行コマンド', name: 'end_default_commands',
                    index: 'end_default_commands', align: 'left', search: true,
                    formatter: _t.brFormatter
                },
                {
                    label: 'CLIエラー文字列', name: 'log_fail_judges', index: 'log_fail_judges',
                    align: 'left', search: true, formatter: _t.brFormatter
                },
                {
                    label: 'CLIデフォルト<br/>プロンプト文字列', name: 'telnet_prompt', index: 'telnet_prompt',
                    align: 'center', search: true
                },
                { label: 'CLIタイム<br/>アウト値', name: 'telnet_timeout', index: 'telnet_timeout', align: 'center', search: true },
                { label: 'SNMPタイム<br/>アウト値', name: 'snmp_timeout', index: 'snmp_timeout', align: 'center', search: true },
                {
                    label: 'アクション', name: 'action', width: 180, align: 'center', search: false, sortable: false,
                    formatter: _t.formatterBtn
                }
            ],
            gridComplete: function () {
                _t.editBtn();
                _t.deleteBtn();
                $('.ui-jqgrid .ui-jqgrid-htable th div').css({ 'height': '30px' });
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
            beforeSelectRow: function (rowid, e) { return false; },
            // beforeRequest: function () {
            //     let currentPage: any = $('#ostypeTable').jqGrid('getGridParam', 'page');
            //     let rowNum: any = $('#ostypeTable').jqGrid('getGridParam', 'rowNum');
            //     let records: any = $('#ostypeTable').jqGrid('getGridParam', 'records');
            //     let totalPages = records % rowNum;
            //     if (records > 0 && currentPage > totalPages) {
            //         console.log(records, currentPage, totalPages);
            //         $('#ostypeTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
            //     }
            // },
            pager: '#ostypePager',
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 350,
            viewrecords: true,
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
        $('#ostypeTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    // btn formatter
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-success edit" id='
            + rowObject['ostypeid'] + '><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;'
            + '<button class="btn btn-xs btn-warning delete" id='
            + rowObject['ostypeid'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    // </br> formatter
    public brFormatter(cellvalue, options, rowObject) {
        /**
        * @brief format the data
        * @param cellvalue: value of the cell;
                  options:includes attributes such as RowId,colModel;
                  rowObject:json data of the row
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        if (cellvalue !== null && cellvalue !== '') {
            return '<i class="fa fa-genderless"></i> ' + cellvalue.replace(/，/g, '<br /><i class="fa fa-genderless"></i> ');
            // return '<i class="fa fa-genderless"></i> ' + cellvalue.replace(/，/g, '\n<i class="fa fa-genderless"></i> ');
        } else {
            return '-';
        }
    }
    // no data formatter
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
    public editBtn() {
        /**
        * @brief get the ostype id and show edit popup
        * @post refresh table if edit successfully
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        $('.edit').click(function (event) {
            let editId = $(event)[0].target.id;
            if (editId) {
                _t.modalRef = _t.modalService.show(OstypeEditComponent, _t.modalConfig);
                _t.modalRef.content.id = editId;
                _t.modalRef.content.actionType = 'edit';
                let ostypeEdit$ = _t.modalService.onHidden.subscribe(o => {
                    if (o) {
                        $('#ostypeTable').jqGrid('clearGridData');
                        $('#ostypeTable').trigger('reloadGrid');
                    }
                    _t.unsubscribe(ostypeEdit$);
                });
            }
        });
    }
    public deleteBtn() {
         /**
        * @brief get the ostype id and delete this ostype
        * @post reload cpgTable if delete sucessfully
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_device_ostype/?id=';
        $('.delete').click(function (event) {
            event.stopPropagation();
            let delId = $(event)[0].target.id;
            let delName = $('#ostypeTable').jqGrid().getRowData(delId)['name'];
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
                            _t.modalMsg = '削除しました。';
                            _t.closeMsg = '閉じる';
                            _t.showAlertModal(_t.modalMsg, _t.closeMsg);
                            $('#modalButton').on('click', function () {
                                $('#ostypeTable').jqGrid('clearGridData');
                                $('#ostypeTable').trigger('reloadGrid');
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
        });
    }
    public ostypeLogin() {
        /**
        * @brief show create popup
        * @post refresh table if create successfully
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.modalRef = this.modalService.show(OstypeLoginComponent, this.modalConfig);
        let ostypeLogin$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                $('#ostypeTable').jqGrid('clearGridData');
                $('#ostypeTable').trigger('reloadGrid');
            }
            this.unsubscribe(ostypeLogin$);
        });
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
    public unsubscribe(res: any) {
        res.unsubscribe();
    }
    ngOnDestroy() {
        if (this.modalRef) {
            this.modalRef.hide();
        }
    }
}
