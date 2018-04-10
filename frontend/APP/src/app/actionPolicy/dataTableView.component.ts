import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { DataTableLoginComponent } from './dataTableLogin.component';
import { DataTableDetailComponent } from './dataTableDetail.component';
declare var $: any;
import * as _ from 'lodash';

@Component({
  selector: 'data-table-view',
  templateUrl: 'dataTableView.component.html',
  styleUrls: ['actionPolicy.component.less']
})
export class DataTableViewComponent implements OnInit, AfterViewInit {

  tableModel: any = [
    { label: 'No', hidden: true, name: 'table_id', index: 'table_id' },
    { label: 'テーブル名', name: 'name', width: 30, align: 'center' },
    { label: '概要', name: 'description', width: 45, align: 'center' },
    {
      label: 'アクション', name: 'action', width: 30, align: 'center', search: false,
      formatter: this.formatterButtons
    },
  ];

  testData: any = [
    { table_id: 10, name: 'data table 1', description: 'description of data table 1' },
    { table_id: 11, name: 'data table 2', description: 'description of data table 2' },
    { table_id: 12, name: 'data table 3', description: 'description of data table 3' },
  ];

  modalRef: BsModalRef;
  modalConfig = {
    animated: true,
    keyboard: true,
    backdrop: true,
    ignoreBackdropClick: true
  };

  constructor(
    private modalService: BsModalService,
    public httpClient: HttpClientComponent,
    public router: Router,
    private route: ActivatedRoute,
    // public bsModalRef: BsModalRef
  ) { }

  ngOnInit() {

  }

  ngAfterViewInit() {
    this.drawDataTableTable();

  }

  formatterButtons(cellvalue, options, rowObject) {
    // let buttons = '';
    let buttons = '<button class="btn btn-xs btn-default showInfo" id="show_' + rowObject["table_id"] + '"><i class="fa fa-info-circle"></i> 表示</button>&nbsp;';
    buttons += '<button class="btn btn-xs btn-warning delete" id="delete_' + rowObject["table_id"] + '"><i class="fa fa-minus-square"></i> 削除</button>&nbsp;';
    buttons += '<button class="btn btn-xs btn-primary addAction" id="add_' + rowObject["table_id"] + '"><i class="fa fa-plus-square"></i> アクションポリシー追加</button>';
    return buttons
  }

  public drawDataTableTable() {
    let _this = this;
    $('#tableTable').jqGrid({
      // url: '/v1/api_data_collection/',
      // datatype: 'JSON',
      datatype: 'local',
      // mtype: 'get',
      colModel: _this.tableModel,
      // postData: { '': '' },
      data: _this.testData,
      // viewrecords: true,
      loadComplete: function () {
        _this.showDataTable();
        // _this.renderColor();
      },
      rowNum: 10,
      rowList: [10, 20, 30],
      autowidth: true,
      beforeSelectRow: function (rowid, e) { return false; },
      height: 230,
      pager: '#tablePager',
      // jsonReader: {
      //     root: 'data',
      //     page: 'current_page_num',
      //     total: 'num_page',
      //     records: 'total_num',
      //     userData: 'status',
      //     repeatitems: false,
      // },
    });
    $('#tableTable').jqGrid('filterToolbar', { defaultSearch: 'cn' });
  }

  newTable() {

    this.modalRef = this.modalService.show(DataTableLoginComponent, this.modalConfig);
    // init the title of modal
    this.modalRef.content.title = 'テーブル登録';

  }

  public showDataTable() {
    let _this = this;
    $('.showInfo').click(function (event) {
      let id = $(event)[0].target.id;
      let tableId = id.split('_')[1];
      // open modal and init the title and id of modal
      _this.modalRef = _this.modalService.show(DataTableDetailComponent, _this.modalConfig);
      _this.modalRef.content.title = 'データ取得編集';
      _this.modalRef.content.id = tableId;
    });
  }
}

