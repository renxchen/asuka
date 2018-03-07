import { Component, OnInit, AfterViewInit, ComponentFactory } from '@angular/core';
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
export class OstypeComponent implements OnInit, AfterViewInit {
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
        let _t = this;
        _t.ostypeTable$ = $('#ostypeTable').jqGrid({
            url: '/v1/api_device_ostype/',
            datatype: 'json',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'ostypeid', index: 'ostypeid', search: false, key: true },
                { label: 'OS Type名', name: 'name', index: 'name', width: 200, align: 'center', search: true },
                { label: '概要', name: 'desc', index: 'desc', width: 200, align: 'center', search: true },
                {
                    label: 'CLI情報取得前デフォルト実行コマンド', name: 'start_default_commands',
                    index: 'start_default_commands', width: 250, align: 'center', search: true
                },
                {
                    label: 'CLI情報取得完了後デフォルト実行コマンド', name: 'end_default_commands',
                    index: 'end_default_commands', width: 250, align: 'center', search: true
                },
                { label: 'CLIエラー文字列', name: 'log_fail_judges', index: 'log_fail_judges', width: 150, align: 'center', search: true },
                { label: 'CLIデフォルトプロンプト文字列', name: 'telnet_prompt', index: 'telnet_prompt', width: 220, align: 'center', search: true },
                { label: 'CLI タイムアウト値', name: 'telnet_timeout', index: 'telnet_timeout', width: 180, align: 'center', search: true },
                { label: 'SNMP タイムアウト値', name: 'snmp_timeout', index: 'snmp_timeout', width: 170, align: 'center', search: true },
                {
                    label: 'アクション', name: 'action', width: 120, align: 'center', search: false,
                    formatter: this.formatterBtn, resizable: false
                }
            ],
            gridComplete: function () {
                _t.editBtn();
                _t.deleteBtn();
            },
            beforeSelectRow: function (rowid, e) { return false; },
            onPaging: function () {
                let currentPage: any = $('#ostypeTable').jqGrid('getGridParam', 'page');
                let rowNum: any = $('#ostypeTable').jqGrid('getGridParam', 'rowNum');
                let records: any = $('#ostypeTable').jqGrid('getGridParam', 'records');
                let totalPages = records % rowNum;
                if (records > 0 && currentPage > totalPages) {
                    console.log(records, currentPage, totalPages);
                    $('#ostypeTable').jqGrid('setGridParam', { page: 1 }).trigger('reloadGrid');
                }
            },
            pager: '#ostypePager',
            rowNum: 5,
            rowList: [5, 10, 15],
            autowidth: false,
            // set overFlow-x
            width: 1216,
            shrinkToFit: false,
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
        $('#ostypeTable').jqGrid('filterToolbar', { searchOnEnter: true, defaultSearch: 'cn' });
    }
    // btn formatter
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-success edit" id='
            + rowObject['ostypeid'] + '><i class="fa fa-pencil-square"></i> 編集</button>&nbsp;'
            + '<button class="btn btn-xs btn-warning delete" id='
            + rowObject['ostypeid'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    public editBtn() {
        let _t = this;
        _t.apiPrefix = '/v1';
        // let url = '/api_device_ostype/?id=';
        $('.edit').click(function (event) {
            let id = $(event)[0].target.id;
            if (id) {
                console.log('id', id);
                // _t.router.navigate(['/index/ostypedit'],
                //     { queryParams: { 'id': id } });
                _t.modalRef = _t.modalService.show(OstypeEditComponent, _t.modalConfig);
                _t.modalRef.content.id = id;
                _t.modalRef.content.actionType = 'edit';
                let ostypeEdit$ = _t.modalService.onHidden.subscribe(o => {
                    if (o) {
                        _t.ostypeTable$.GridUnload();
                        _t.drawOstypeTable();
                    }
                    _t.unsubscribe(ostypeEdit$);
                });
            }
        });
    }
    public deleteBtn() {
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_device_ostype/?id=';
        $('.delete').click(function (event) {
            event.stopPropagation();
            let id = $(event)[0].target.id;
            let name = $('#ostypeTable').jqGrid().getRowData(id)['name'];
            let alt = confirm(name + 'を削除します。よろしいですか？');
            if (alt) {
                _t.httpClient.setUrl(_t.apiPrefix);
                _t.httpClient
                    .toJson(_t.httpClient.delete(url + id))
                    .subscribe(res => {
                        let status = _.get(res, 'status');
                        let msg = _.get(status, 'message');
                        let data = _.get(res, 'data');
                        if (status && status['status'].toLowerCase() === 'true') {
                            _t.modalMsg = '削除に成功しました。';
                            _t.closeMsg = '閉じる';
                            _t.showAlertModal(_t.modalMsg, _t.closeMsg);
                            $('#modalButton').on('click', function () {
                                $('#ostypeTable').jqGrid().trigger('reloadGrid');
                            });
                        } else {
                            // check this ostype occupation, check with backend
                            if (msg === 'EXIST_IN_DEVICES') {
                                this.modalMsg = 'Can not been delete when ostype exits in devices';
                                this.closeMsg = 'close';
                                _t.showAlertModal(this.modalMsg, this.closeMsg);
                            } else if (msg === 'OSTYPE_EXIST_IN_SCHEDULE') {
                                this.modalMsg = 'Can not been delete when ostype exits in schedule';
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
    public ostypeLogin() {
        this.modalRef = this.modalService.show(OstypeLoginComponent, this.modalConfig);
        this.modalRef.content.actionType = 'create';
        let ostypeLogin$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                this.ostypeTable$.GridUnload();
                this.drawOstypeTable();
            }
            this.unsubscribe(ostypeLogin$);
        });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
    public unsubscribe(res: any) {
        res.unsubscribe();
    }
}
