import { Component, OnInit, AfterViewInit, ElementRef } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';
import * as moment from 'moment';
import * as flatpickr from 'flatpickr';

@Component({
  selector: 'data-table-detail',
  templateUrl: 'dataTableDetail.component.html',
  styleUrls: ['actionPolicy.component.less']
})
export class DataTableDetailComponent implements OnInit, AfterViewInit {
  tableName: string;
  tableId: string;
  tableType: string;
  apiPrefix: String = '/v1';
  contentData: any;
  startTime: any;
  endTime: any;
  flatPickrStartTime: any;
  flatPickrEndTime: any;
  pickrOption: any = {
    enableTime: true,
    time_24hr: true
  };


  constructor(
    public httpClient: HttpClientComponent,
    public router: Router,
    private route: ActivatedRoute,
    public bsModalRef: BsModalRef,
    public elementRef: ElementRef
  ) { }

  public ngOnInit() {
    this.httpClient.setUrl(this.apiPrefix);
  }

  public ngAfterViewInit() {
    let _t = this;
    this.setPopUpSize();
    setTimeout(() => {
      _t.tableName = _t.contentData['name'];
      _t.tableId = _t.contentData['table_id'];
      _t.tableType = _t.contentData['coll_policy__policy_type'];
      _t.drawTable('init');
    }, 0);
    this.initPickr();
  }

  protected setPopUpSize() {
    $('#detail-popup').parents('div.modal-content').css('width', '711px');
  }

  protected initPickr() {
    let startEle = document.getElementById('startTimeInput');
    let endEle = document.getElementById('endTimeInput');
    this.flatPickrStartTime = new flatpickr(startEle, this.pickrOption);
    this.flatPickrEndTime = new flatpickr(endEle, this.pickrOption);

  }

  protected setMaxAndMinDate(type) {
    /**
     * Date:20180416
     * @author necy
     * @param type : starttime or endtime flg
     * brief :set the max value or min value of flatpickr plugin
     */
    if (this.startTime && type === 'start') {
      this.flatPickrEndTime.set('minDate', this.startTime);
    }
    if (this.endTime && type === 'end') {
      this.flatPickrStartTime.set('maxDate', this.endTime);
    }
  }
  protected drawTable(type: string) {
    let _t = this;
    let lableTmp = _t.tableType == '1' ? 'OID' : 'Path';
    let nameTmp = _t.tableType == '1' ? 'oid' : 'path';
    let tableModel = [
      { label: 'デバイス名', name: 'hostname', align: 'center' },
      { label: 'Time Stamp', name: 'date', align: 'center' },
      { label: lableTmp, name: nameTmp, align: 'center' },
      { label: 'Value', name: 'value', align: 'center' },
    ];
    let url = '/v1/api_data_table_step1/?id=' + this.tableId;
    let tableJson: any = {
      url: url,
      datatype: 'JSON',
      // datatype: 'local',
      mtype: 'get',
      colModel: tableModel,
      // data: _t.testData,
      loadComplete: function (val) {
        _t.setColumeLable(val.data.data);
      },
      rowNum: 10,
      rowList: [10, 20, 30],
      autowidth: false,
      width: 665,
      beforeSelectRow: function (rowid, e) { return false; },
      gridComplete: function () { },
      height: 230,
      pager: '#searchTablePager',
      jsonReader: {
        root: 'data.data',
        page: 'current_page_num',
        total: 'num_page',
        records: 'total_num',
        userData: 'status',
        repeatitems: false,
      },
    };
    $('#searchTable').jqGrid(tableJson);
    $('#searchTable').jqGrid('filterToolbar', { defaultSearch: 'cn' });
    if (type === 'search') {
      if (this.startTime && this.endTime) {
        let startTime = moment(moment(this.startTime).unix() * 1000).format('YYYY-MM-DD HH:mm:ss');
        let endTime = moment(moment(this.endTime).unix() * 1000).format('YYYY-MM-DD HH:mm:ss');
        url = '/v1/api_data_table_step1/?id=' + this.tableId + '&start_date=' + startTime + '&end_date=' + endTime;
        $('#searchTable').jqGrid().setGridParam({ datatype: 'json', url: url }).trigger('reloadGrid');
      } else if (this.startTime && !this.endTime || !this.startTime && this.endTime) {
        alert('取得開始日時と取得終了日時を選択してください！');
      }
    }
  }

  protected setColumeLable(tableData: any) {
    let checkName = 'Value';
    if (tableData.length > 0) {
      checkName = tableData[0]['checkitem'].toUpperCase();
      $('#searchTable').jqGrid('setLabel', 'value', checkName);
    }
    return checkName;
  }

  protected csvExport() {
    let url = 'v1/api_data_table_csv_export/?id=' + this.tableId + '&page=1&rows=65536';
    if (this.startTime && this.endTime) {
      let startTime = moment(moment(this.startTime).unix() * 1000).format('YYYY-MM-DD HH:mm:ss');
      let endTime = moment(moment(this.endTime).unix() * 1000).format('YYYY-MM-DD HH:mm:ss');
      url = 'v1/api_data_table_csv_export/?start_date=' + startTime + '&end_date=' + endTime + '&id=' + this.tableId + '&page=1&rows=65536';
    }
    window.location.href = url;
  }

  protected close() {
    this.bsModalRef.hide();
  }

}
