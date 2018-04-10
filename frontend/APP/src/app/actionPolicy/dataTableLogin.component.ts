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
  highLightId: string;
  currentStep = 1;
  maxStep = 1;

  deviceGroupList: any = [];

  sendData: any = {};
  deviceGroup: any = {};
  selectedRowObj: any;
  selectedDeviceGroupId: any;


  btnFlgs = {
    btnPrev: false,
    btnNext: true,
    btnFinished: false
  };

  changeFlgs = {
    deviceGroupChaneged: false,
    columeSelectedChangeed: false
  };

  constructor(
    public httpClient: HttpClientComponent,
    public bsModalRef: BsModalRef
  ) { }

  ngOnInit() {
    this.deviceGroup['id'] = '';
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
    if (this.currentStep === 3) {
      contuineFlg = this.checkColumeSelected();
      if (contuineFlg) {
        this.getTreeData();
      }
    }
    if (this.currentStep === 4) {
      this.getTreeData();
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

  public setChangeFlgs(type) {
    if (type === 'deviceGroup') {
      this.changeFlgs.deviceGroupChaneged = true;
    }
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
      if (res && res.status && res.status.status && res.status.status.toLowerCase() === 'true') {
        if (res.data && res.data.length > 0) {
          this.deviceGroupList = res.data;
          this.selectedDeviceGroupId = res.data[0]['group_id'];
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
        return groupData['group_id'] == _t.selectedDeviceGroupId;
      });
      if (selectDeviceGroup) {
        this.deviceGroup = selectDeviceGroup;
      }
    }
  }

  public drawStepTable() {
    let _t = this;
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
        },
        { label: 'device_group_id', name: 'groupNo', hidden: true },
        { label: 'coll_id', name: 'policyNo', hidden: true },
        { label: 'schedule_id', name: 'schedule_id', hidden: true },
        { label: 'policy_group_id', name: 'cpGroup_id', hidden: true },
        { label: 'oid', name: 'oid', hidden: true },

      ];
      $('#stepTable').jqGrid({
        url: url,
        datatype: 'JSON',
        // datatype: 'local',
        mtype: 'get',
        colModel: stepTableModel,
        // data: testData,
        loadComplete: function () { },
        gridComplete: function () {
          _t.selectData();
        },
        autowidth: false,
        beforeSelectRow: function (rowid, e) { return false; },
        width: 560,
        height: '175',
        jsonReader: {
          root: 'data.data',
          total: 'num_page',
          records: 'total_num',
          userData: 'status',
          repeatitems: false,
        },
      });
      if (this.changeFlgs.deviceGroupChaneged) {
        $("#stepTable").jqGrid().setGridParam({ datatype: 'json', url: url }).trigger('reloadGrid');
        this.changeFlgs.deviceGroupChaneged = false;
      }

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


  protected formatterColumnsBtn(value, grid, rows, state) {

    let rowId = grid['rowId'];
    return '<button  class="btn btn-xs btn-primary" name="selectBtn" id="row_id_' + rowId + '">カラム選択</button>';
  }

  public selectData() {
    let _t = this;
    let allEles = $("button[name='selectBtn']");
    allEles.click(function (event) {
      let selectedBtnId = $(event)[0].target.id;
      let selectedRowId = $(event)[0].target.id.split('_')[2];
      let rowData = $("#stepTable").jqGrid('getRowData', selectedRowId);
      _t.setBtnHighLight(selectedBtnId, allEles);
      _t.selectedRowObj = rowData;

    });
  }

  public setBtnHighLight(selectedEleId, allEles) {
    if (allEles && allEles.length > 0) {
      allEles.each(function () {
        let eleId = $(this)[0].id;
        if (selectedEleId === eleId) {
          $(this).addClass('highlight');
        } else {
          $(this).removeClass('highlight');
        }
      });
    }
  }

  private checkColumeSelected() {
    let flg = this.selectedRowObj ? true : false;
    if (!flg) {
      alert('カラムを選択してください!');
    }
    return flg;
  }

  protected getTreeData() {
    /*
      call :step3 next
      cli : get tree data
      snmp: make tree data
    */
    let treeData: any = {};
    let treeType = '';
    if (this.selectedRowObj) {
      console.log('this.selectedRowObj', this.selectedRowObj);
      treeType = this.selectedRowObj['method'].toLowerCase();
      if (treeType === 'snmp') {
        console.log('snmp');
        treeData = {
          'text': 'OID',
          'state': {
            'opened': true
          },
          'data': {
            'rule_type': 'value',
            'is_root': true,
            'rule_id': 0
          }
        };
        this.drawTree(treeData);
      } else {
        console.log('cli');
        let collection_policy_id = this.selectedRowObj['policyNo'];
        let url = '/api_data_table_step4_tree/?id=' + collection_policy_id;
        this.get(url).subscribe((res: any) => {
          if (res && res.status && res.status.status && res.status.status.toLowerCase() === 'true') {
            treeData = res.data.data;
            console.log('treeData', treeData);
            this.drawTree(treeData);
          } else {
            alert('No Data !');
          }
        });
      }
    }
  }

  protected drawTree(treeData) {

    let treeJson: any = {
      'core': {
        'data': treeData,
        'themes': {
          'theme': 'classic',
          'dots': true,
          'responsive': false,
          'icons': true
        },
        'multiple': false,
        'check_callback': false,
      },
      'plugins': [
        'types',
        'themes'
      ],
      'types': {
        '#': { 'max_depth': 4 }
      },
    };
    $('#tree').jstree(treeJson).bind('activate_node.jstree', function (obj, e) {
    });
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
