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

  selectRowObj: any;

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

  ngOnInit() { }

  ngAfterViewInit() {
    this.drawDataTableTable();
  }

  // main page

  formatterButtons(cellvalue, options, rowObject, state) {
    let rowId = options['rowId'];
    let buttons = '<button class="btn btn-xs btn-default" name ="tableActionBtn" id="show_'
      + rowId + '"><i class="fa fa-info-circle"></i> 表示</button>&nbsp;';
    buttons += '<button class="btn btn-xs btn-warning " name ="tableActionBtn" id="del_'
      + rowId + '"><i class="fa fa-minus-square"></i> 削除</button>&nbsp;';
    buttons += '<button class="btn btn-xs btn-primary " name ="tableActionBtn" id="act_'
      + rowId + '"><i class="fa fa-plus-square"></i> アクションポリシー追加</button>';
    return buttons;
  }

  public drawDataTableTable() {
    /**
     *brief: show the table of main page
    *@author:necy
    *date:20180413
    */
    let _t = this;
    let tableJson: any = {
      // url: '/v1/api_data_collection/',
      // datatype: 'JSON',
      datatype: 'local',
      // mtype: 'get',
      colModel: _t.tableModel,
      data: _t.testData,
      loadComplete: function () { },
      rowNum: 10,
      rowList: [10, 20, 30],
      autowidth: true,
      beforeSelectRow: function (rowid, e) { return false; },
      gridComplete: function () {
        _t.getSelectedRowData();
      },
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
    };
    $('#tableTable').jqGrid(tableJson);
    $('#tableTable').jqGrid('filterToolbar', { defaultSearch: 'cn' });
  }

  protected getSelectedRowData() {
    /**
     *brief: set the data of slected row to global param 'this.selectRowObj'
    *@author:necy
    *date:20180413
    */
    let _t = this;
    let allEles = $("button[name='tableActionBtn']");
    allEles.click(function (event) {
      let selectedBtnId = $(event)[0].target.id;
      let tarEle = $(event.target);
      if (tarEle.is('i')) {
        selectedBtnId = tarEle.parents('button')[0].id;
       }
      let selectedRowId = selectedBtnId.split('_')[1];
      let rowData = $('#tableTable').jqGrid('getRowData', selectedRowId);
      _t.selectRowObj = rowData;
      _t.judgeActionType(selectedBtnId);
    });
  }

  protected deleteTableRow() {
    /**
     *brief: delet selected row
    *@author:necy
    *date:20180413
    */
    if (this.selectRowObj && this.selectRowObj['table_id']) {
      let table_id = this.selectRowObj['table_id'];
      let url = '/api_data_table_step1/?id=' + table_id;

      this.delete(url).subscribe((res: any) => {
        this.showMsg(res);
      });
    }
  }

  protected judgeActionType(btn_id) {
    /**
     *brief: judge the type of click event (show:detail;del:delete;act:edit)
     *@author:necy
     *@param:btn_id : the id of the button clicked
     *date:20180413
    */
    let type = btn_id.split('_')[0];
    console.log('this.selectedRow', this.selectRowObj);
    if (type === 'show') {
      this.showDataTableDetail();
    } else if (type === 'del') {
      this.deleteTableRow();
    } else if (type === 'act') { }
  }


  // call creat popup
  protected newTable() {

    this.modalRef = this.modalService.show(DataTableLoginComponent, this.modalConfig);
    this.modalRef.content.title = 'テーブル登録';

  }

  // call detail popup

  public showDataTableDetail() {
    /**
     *brief: show detail popup
     *@author:necy
     *date:20180413
    */
    this.modalRef = this.modalService.show(DataTableDetailComponent, this.modalConfig);
    this.modalRef.content.title = 'データ取得編集';
    this.modalRef.content.contentData = this.selectRowObj;
  }

  // commum function

  private showMsg(res) {
    if (res && res.status && res.status.status) {
      if (res.status.status.toLowerCase() === 'true') {
        alert('削除しました！');
      } else {
        let msg = res.status.message;
        alert(msg);
      }
    }
  }

  private get(url: string) {
    return this.httpClient.toJson(this.httpClient.get(url));
  }

  private post(url: string, bodyData: any) {
    return this.httpClient.toJson(this.httpClient.post(url, bodyData));
  }

  private put(url: string, bodyData: any) {
    return this.httpClient.toJson(this.httpClient.put(url, bodyData));
  }

  private delete(url: string) {
    return this.httpClient.toJson(this.httpClient.delete(url));
  }

}

