import {
    Component,
    OnInit,
    AfterViewInit,
} from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';
import * as _ from 'lodash';
declare var $: any;
@Component({
    selector: 'cp-view',
    templateUrl: 'cPView.component.html',
    styleUrls: ['collectionPolicy.component.less']
})
export class CPViewComponent implements OnInit, AfterViewInit {
    cPType: any;
    thirdCol: any;
    thirdName: any;
    apiPrefix: string;
    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
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
        let $cpTable = $('#cpTable');
        this.cPType = $(event.target).val();
        if (this.cPType === '0') {
            $cpTable.GridUnload();
            this.drawCPTable('コマンド', 'cli_command', this.cPType);
        } else {
            $cpTable.GridUnload();
            this.drawCPTable('OID', 'snmp_oid', this.cPType);
        }
    }
    // init table
    public drawCPTable(thirdCol?: any, thirdName?: any, cPType?: any) {
        let _t = this;
        $('#cpTable').jqGrid({
            url: '/v1/api_collection_policy/',
            datatype: 'JSON',
            mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'coll_policy_id', index: 'coll_policy_id', search: false },
                { label: 'コレクションポリシー名', name: 'name', index: 'name', width: 50, align: 'center', search: true },
                { label: 'OS Type', name: 'ostype_name', index: 'ostype', width: 50, align: 'center', search: true },
                { label: thirdCol, name: thirdName, index: thirdName, width: 50, align: 'center', search: true },
                { label: '概要', name: 'desc', index: 'desc', width: 50, align: 'center', search: true },
                {
                    label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
                    formatter: this.formatterBtn, resizable: false
                }
            ],
            loadComplete: this.loadCompleteFun,
            gridComplete: function() {
                _t.detailBtn();
                _t.editBtn();
                _t.deleteBtn();
            },
            beforeSelectRow: function(rowid, e) { return false; },
            pager: '#cpPager',
            postData: { 'policy_type': cPType },
            rowNum: 10,
            rowList: [5, 10, 15],
            autowidth: true,
            height: 340,
            viewrecords: true,
            emptyrecords: 'Nothing to display',
            jsonReader: {
                root: 'data',
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
            if (this.cPType === '0') {
            //     _t.router.navigate(['/index/cliCPViewDetail'],
            //     { queryParams: {'id' : id }});
            } else {
            //     _t.router.navigate(['/index/snmpCPViewDetail'],
            //     { queryParams: {'id' : id }});
            }
        });
    }
    public editBtn() {
        let _t = this;
        $('.edit').click(function (event) {
            let id = $(event)[0].target.id;
            console.log('id', id);
            if (_t.cPType === '0') {
                _t.router.navigate(['/index/cliCPEdit'],
                { queryParams: {'id' : id }});
            } else {
                _t.router.navigate(['/index/snmpCPEdit'],
                { queryParams: {'id' : id }});
            }
        });
    }
    public deleteBtn() {
        let _t = this;
        _t.apiPrefix = '/v1';
        let url = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        $('.delete').click(function (event) {
            let id = $(event)[0].target.id;
            // _t.httpClient.setUrl(_t.apiPrefix);
            // _t.httpClient
            // .toJson(_t.httpClient.delete(url + '?id=' + id))
            // .subscribe(res => {
            //     if ( res['status']['status'].toLowerCase() === 'true') {
            //         _t.drawCPTable();
            //     } else {
                        // if (['status']['message']) {
                            // alert(res['status']['message']);
                        // }
            //     }
            // });
        });
    }
    public cpLogin() {
        if (this.cPType === '0') {
            this.router.navigate(['/index/cliCPLogin'],
            { queryParams: {'cPType' :  parseInt(this.cPType, 0)}});
        } else {
            this.router.navigate(['/index/snmpCPLogin'],
            { queryParams: {'cPType' : parseInt(this.cPType, 0) }});
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
}
