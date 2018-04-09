import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
// import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
  selector: 'data-table-login',
  templateUrl: 'dataTableLogin.component.html',
  styleUrls: ['actionPolicy.component.less']
})
export class DataTableLoginComponent implements OnInit, AfterViewInit {
  apiPrefix: any = '/v1';
  title: string;
  tableName: string;
  description: string;

  currentStep = 1;
  maxStep = 1;

  deviceGroupList: any = [];

  sendData: any = {};
  deviceGroup: any = {};

  btnFlgs = {
    btnPrev: false,
    btnNext: true,
    btnFinished: false
  };


  constructor(
    public httpClient: HttpClientComponent,
    public bsModalRef: BsModalRef
  ) { }

  ngOnInit() {
    this.httpClient.setUrl(this.apiPrefix);
    this.getDeviceGroupList();
  }

  ngAfterViewInit() {
    this.setBottomBtns();
  }

  // step common function

  public next() {
    /*
      when click next icon btn ,step ++
    */
    let contuineFlg = true;
    if (this.currentStep === 1) {
      contuineFlg = this.checkTableNameValidation();
    }
    if (this.currentStep === 2) {
      contuineFlg = this.checkDeviceGroupList();
    }
    if (contuineFlg) {
      this.maxStep === this.currentStep ? this.maxStep++ : this.maxStep = this.maxStep;
      this.currentStep++;
      // this.maxStep === 4 ? this.maxStep = 4 : this.maxStep++;
      this.setBottomBtns();
    }
  }

  public previous() {
    /*
      when click prev icon btn ,step --
    */
    this.currentStep--;
    this.setBottomBtns();
  }

  public setBottomBtns() {
    /*
      set bottom (prev next finished) btn status,disabled or not ,
      call : afterviewinit and next 、previous
    */
    if (this.currentStep === 1) {
      this.btnFlgs.btnPrev = false;
    } else {
      this.btnFlgs.btnPrev = true;
    }
    if (this.currentStep === 3) {
      this.drawStepTable();
    }
    if (this.currentStep === 4) {
      this.btnFlgs.btnNext = false;
      this.btnFlgs.btnFinished = true;
    } else {
      this.btnFlgs.btnNext = true;
      this.btnFlgs.btnFinished = false;
    }

  }
  public setSteps(step: number) {
    this.currentStep = step;
  }

  // step 1

  public checkTableNameValidation() {
    /*
      check this.tableName vilidaty(repeat,exit)
      call : step 1
    */
    if (this.tableName) {
      let url = '/api_data_table_name_verify/?name=' + this.tableName + '/';
      this.get(url).subscribe((res: any) => {
        if (res && res.status && res.status.status && res.status.status.toLowerCase() === 'false') {
          let msg = res.status.message;
          alert(msg);
          return false;
        }
      });
    } else {
      alert('テーブル名を入力してください！');
      return false;
    }
    return true;
  }

  // step 2

  public getDeviceGroupList() {
    /*
      get device group list
      call: checkTableNameValidation taleName right.

    */
    let url = '/api_device_group/';
    this.get(url).subscribe((res: any) => {
      if (res && res.status && res.status.status.toLowerCase() === 'true') {
        if (res.data && res.data.length > 0) {
          this.deviceGroupList = res.data;
          this.deviceGroup.group_id = res.data[0]['group_id'];
        }
      } else {
        let msg = res.status.message;
        alert(msg);
        return false;
      }
    });
    return true;
  }

  public checkDeviceGroupList() {
    /*
      check deviceGroupList is empty or not
     */
    if (!this.deviceGroupList || this.deviceGroupList.length <= 0) {
      alert('Device group is not available!');
      return false;
    }
    return true;
  }

  // step3

  private getDeviceGroupName() {
    let _t = this;
    let selectDeviceGroup: any;
    if (this.deviceGroupList && this.deviceGroupList.length > 0) {
      selectDeviceGroup = _.find(this.deviceGroupList, function (groupData) {
        return groupData['group_id'] === _t.deviceGroup.group_id;
      });
      if (selectDeviceGroup) {
        this.deviceGroup = selectDeviceGroup;
      }
    }
  }

  public drawStepTable() {

    this.getDeviceGroupName();
    if (this.deviceGroup && this.deviceGroup['group_id'] && this.deviceGroup['name']) {
      let url = 'v1/api_data_table_step3_table/?id=' + this.deviceGroup['group_id'] + '&device_group_name=' + this.deviceGroup['name'];
      let stepTableModel: any = [
        {
          label: 'デバイスグループ', name: 'deviceGroup', align: 'center', sortable: false,
          cellattr: this.arrtSetting
        },
        {
          label: 'コレクションポリシーグループ', hidden: false, name: 'cpGroup', align: 'center', sortable: false,
          cellattr: this.arrtSetting
        },
        {
          label: 'Priority', name: 'priority', align: 'center',
          cellattr: this.arrtSetting
        },
        { label: 'コレクションポリシー', name: 'policy', align: 'center' },
        { label: '取得方法', hidden: false, name: 'method', align: 'center' },
        {
          label: 'No', hidden: false, name: 'policyNo', index: 'policyNo', align: 'center',
          formatter: this.formatterColumnsBtn
        }
      ];

      $('#stepTable').jqGrid({
        url: url,
        datatype: 'JSON',
        // datatype: 'local',
        mtype: 'get',
        colModel: stepTableModel,
        // data: testData,
        loadComplete: function () {
        },
        autowidth: false,
        beforeSelectRow: function (rowid, e) { return false; },
        width: 560,
        height: '190',
        jsonReader: {
          root: 'data.data',
          total: 'num_page',
          records: 'total_num',
          userData: 'status',
          repeatitems: false,
        },
      });

      // $('#stepTable').jqGrid('filterToolbar', { defaultSearch: 'cn' });
    }
  }

  public arrtSetting(rowId, val, rowObject, cm) {
    let attr = rowObject.attr[cm.name], result;
    if (attr.rowspan != null && attr.rowspan !== 'None') {
      result = ' rowspan=' + '"' + attr.rowspan + '"';
    } else {
      result = ' style="display:none"';
    }
    return result;
  }

  // protected formatterColumnsBtn(cellvalue, options, rowObject) {
  //   console.log('cellvalue', cellvalue);
  //   console.log('options', options);
  //   console.log('rowObject', rowObject);

  // }
  protected formatterColumnsBtn(value, grid, rows, state) {
    let _t = this;
    return '<button style="color:#f60" onclick="modify.bind(' + this + ')">Edit</button>';
  }

  public modify(id) {
    console.log('aaaaaaaaaaaaaaa');
  }

  // common function of http

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
