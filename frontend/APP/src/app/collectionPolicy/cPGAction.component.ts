import { Component, OnInit, AfterViewInit, OnDestroy, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalDirective } from 'ngx-bootstrap/modal';
declare var $: any;
import * as _ from 'lodash';
@Component({
    selector: 'cpg-action',
    templateUrl: './cPGAction.component.html',
    styleUrls: ['./collectionPolicy.component.less']
})
export class CPGActionComponent implements OnInit, AfterViewInit {
    cpgInfo: any;
    actionType: any;
    id: any;
    apiPrefix: any;
    tableData: any;
    name: any;
    osType: any;
    selectedOsType: any;
    desc: any;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef) {
    }
    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
        this.drawcpglogintable(this.tableData);
    }
    private changemoreType() {
        // this.moreType = !this.moreType;
    }
    public getOsType() {
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_ostype/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        this.osType = res['data'];
                        let osTypeTmp = _.clone(res['data']);
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public doCheck() {
    }
    public formatterBtn(cellvalue, options, rowObject) {
        return '<button class="btn btn-xs btn-warning delete"  id='
            + rowObject['title_id'] + '><i class="fa fa-minus-square"></i> 削除</button>';
    }
    // table
    public drawcpglogintable(data: any) {
        let _t = this;
        $('#cpglogintable').jqGrid({
            // url: '/v1/api_collection_policy_group/',
            datatype: 'local',
            data: data,
            // mtype: 'get',
            colModel: [
                { label: 'No', hidden: true, name: 'title_id', index: 'title_id', search: false },
                { label: '機能ON/OFF', name: 'check', index: 'check', width: 50, align: 'center', formatter: "checkbox", formatoptions: { disabled: false } },
                { label: 'コレクションポリシー名', name: 'dataone', index: 'dataone', width: 60, align: 'center', },
                { label: '取得間隔', name: 'getTime', index: 'getTime', width: 40, align: 'center', },
                { label: '保存間隔', name: 'saveTime', index: 'saveTime', width: 40, align: 'center', },
                {
                    label: '', name: '', width: 30, align: 'center', formatter: this.formatterBtn, sortable: false,
                }
            ],
            gridComplete: function () {
                _t.deleteBtn();
            },

            beforeSelectRow: function (rowid, e) { return false; },
            pager: '#cpgloginPager',
            rowNum: 5,
            rowList: [5, 10, 15],
            width: 736,
            height: 100,
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
        $('#cpglogintable').jqGrid({ searchOnEnter: true, defaultSearch: 'cn' });
    }

    public deleteBtn() {


    }
    public cPGLogin() {
    }
}
