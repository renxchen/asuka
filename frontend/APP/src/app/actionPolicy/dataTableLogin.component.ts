import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
// import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { CommentStmt } from '@angular/compiler';

declare var $: any;
import * as _ from 'lodash';
import * as moment from 'moment';

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
  tree_id: String = '';

  deviceGroupList: any = [];
  item_id_str: any = '';

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
    this.setModalSize();
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
      if (contuineFlg) {
        this.drawStepTable();
      }
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
    }
    this.setBottomBtns();

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
      // this.drawStepTable();
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
    this.setBottomBtns();
  }

  public setChangeFlgs(type) {
    if (type === 'deviceGroup') {
      this.changeFlgs.deviceGroupChaneged = true;
      this.selectedRowObj = undefined;
    }
  }

  protected setModalSize() {
    $('#login-modal').parents('div.modal-content').css('width', '660px');
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
          label: '優先度', name: 'priority', align: 'center',
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
        width: 620,
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
      let rowData = $('#stepTable').jqGrid('getRowData', selectedRowId);
      _t.setBtnHighLight(selectedBtnId, allEles);
      _t.setColumeChangedFlg(rowData);
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

  public setColumeChangedFlg(newRowData) {
    let isEqual: boolean = _.isEqual(this.selectedRowObj, newRowData);
    this.changeFlgs.columeSelectedChangeed = isEqual ? false : true;
  }

  // step 4

  protected getTreeData() {
    /**
   * @brief get treedata for cli type and make data for snmp
   * @author Necy
   * @date 2018/04/10
   */

    let treeData: any = {};
    let treeType = '';
    if (this.selectedRowObj) {
      treeType = this.selectedRowObj['method'].toLowerCase();
      if (treeType === 'snmp') {
        treeData = {
          'text': 'OID',
          'state': {
            'opened': true
          },
          'data': {
            'rule_type': 'value',
            'is_root': true,
            'rule_id': 0,
            'tree_id': 'snmp_oid'
          }
        };
        if (this.changeFlgs.columeSelectedChangeed) {
          this.destroyTree();
          this.destroyTreeTable();
        }
        this.drawTree(treeData, treeType);
      } else {
        let collection_policy_id = this.selectedRowObj['policyNo'];
        let url = '/api_data_table_step4_tree/?id=' + collection_policy_id;
        this.get(url).subscribe((res: any) => {
          if (res && res.status && res.status.status && res.status.status.toLowerCase() === 'true') {
            treeData = res.data.data;
            // treeData = data;
            this.setTreeDisabled(treeData);
            if (this.changeFlgs.columeSelectedChangeed) {
              this.destroyTree();
              this.destroyTreeTable();
            }
            this.drawTree(treeData, treeType);
          } else {
            alert('No Data !');
          }
        });
      }
    }
  }

  private setTreeDisabled(sourceTreeData) {
    /**
      * @brief set disabled for no-leaf nodes
      * @param sourceTreeData: tree data
      * @author Necy
      * @date 2018/04/10
      */
    if (sourceTreeData && sourceTreeData['children'] && sourceTreeData['children'].length > 0
      || sourceTreeData && sourceTreeData['data'] && sourceTreeData['data']['is_root']) {
      sourceTreeData['state']['disabled'] = true;
      for (let child of sourceTreeData['children']) {
        this.setTreeDisabled(child);
      }
    } else {
      return false;
    }
  }

  private destroyTree() {
    /**
  * @brief reload tree
  * @author Necy
  * @date 2018/04/10
  */
    $('#tree').jstree('destroy');
    this.changeFlgs.columeSelectedChangeed = false;
    this.tree_id = '';
  }

  protected drawTree(treeData, treeType) {
    /**
    * @brief draw tree
    * @author Necy
    * @date 2018/04/10
    */
    let _t = this;
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
      'plugins': ['types', 'themes']
    };
    $('#tree').jstree(treeJson).bind('activate_node.jstree', function (obj, e) {
      _t.destroyTreeTable();
      _t.drawTreeTable(e, treeType);
    });
  }

  protected drawTreeTable(node: any, treeType) {

    /**
        * @brief draw  table which is shown by click tree node
        * @param node : the tree node clicked; treeType : cli or snmp
        * @author Necy
        * @date 2018/04/11
    */

    let lableName;
    let snmpTableModel: any = [
      { label: 'デバイス名', name: 'device_name', align: 'center', sortable: false },
      { label: 'Time Stamp', name: 'time_stamp', align: 'center', sortable: false, },
      { label: 'OID', name: 'oid', align: 'center' },
      { label: '值', name: 'value', align: 'center' }
    ];
    let cliTableModel: any = [
      { label: 'デバイス名', name: 'device_name', align: 'center', sortable: false },
      { label: 'Time Stamp', name: 'time_stamp', align: 'center', sortable: false, },
      { label: 'Path', name: 'path', align: 'center' },
      { label: 'Value', name: 'value', align: 'center' }
    ];
    this.tree_id = node['node']['data']['tree_id'];
    let tableData: any;
    let url = '';
    let tableJson: any = {
      url: '',
      datatype: 'local',
      mtype: 'get',
      colModel: '',
      data: '',
      loadComplete: function () { },
      gridComplete: function () {
      },
      autowidth: true,
      beforeSelectRow: function (rowid, e) { return false; },
      height: 'auto',
      jsonReader: {
        root: 'data.data',
        total: 'num_page',
        records: 'total_num',
        userData: 'status',
        repeatitems: false,
      },
    };
    if (treeType === 'snmp') {
      url = '/api_data_table_step4_table/?coll_id=' + this.selectedRowObj['policyNo'] +
        '&device_group_id=' + this.selectedRowObj['groupNo'] + '&policy_group_id=' + this.selectedRowObj['cpGroup_id'] +
        '&rule_name=' + '' + '&schedule_id=' + this.selectedRowObj['schedule_id'] + '&oid=' + this.selectedRowObj['oid'];
      // url = '/api_data_table_step4_table/?coll_id=1&device_group_id=1&policy_group_id=2&rule_name=OID&schedule_id=10&oid=1.1.1.1';
      tableJson['colModel'] = snmpTableModel;
    } else if (treeType === 'cli') {
      url = '/api_data_table_step4_table/?tree_id=' + this.tree_id + '&coll_id=' + this.selectedRowObj['policyNo'] +
        '&device_group_id=' + this.selectedRowObj['groupNo'] + '&policy_group_id=' + this.selectedRowObj['cpGroup_id'] +
        '&rule_name=' + '' + '&schedule_id=' + this.selectedRowObj['schedule_id'];
      // url = '/api_data_table_step4_table/?coll_id=1&device_group_id=1&policy_group_id=2&rule_name=OID&schedule_id=10&oid=1.1.1.1';
      tableJson['colModel'] = cliTableModel;
    }
    this.get(url).subscribe((res: any) => {
      if (res && res.status && res.status.status && res.status.status.toLowerCase() === 'true') {
        if (res.data.data) {
          this.getItemList(res.data.items_rule_name);
          // tableJson['data'] = this.tableDataFormat(res.data.data);

          if (treeType === 'cli') {
            if (res.data.items_rule_name.length > 0) {
              lableName = res.data.items_rule_name[0]['rule_name'];
              tableJson['colModel'][3]['label'] = lableName;
            }
          }
          $('#treeTable').jqGrid(tableJson);
          $('#treeTable').parents('div.ui-jqgrid-bdiv').css('max-height', '190px');
        }

      } else {
        let msg = res.status.message;
        alert(msg);
      }
    });
  }

  public destroyTreeTable() {
    this.item_id_str = '';
    this.tree_id = '';
    let treeTableGrid = $('#tree_div div.ui-jqgrid-bdiv table');
    if (treeTableGrid.length >= 1) {
      $('#treeTable').jqGrid('GridUnload');
    }
  }

  protected tableDataFormat(data: any) {
    for (let obj of data) {
      if (obj['time_stamp']) {
        obj['time_stamp'] = moment(obj['time_stamp'] * 1000).format('YYYY-MM-DD HH:mm:ss');
      }
    }
    return data;
  }

  private getItemList(data) {
    this.item_id_str = '';
    for (let obj of data) {
      if (obj['item_id']) {
        this.item_id_str = this.item_id_str + obj['item_id'] + ',';
      }
    }
    this.item_id_str = this.item_id_str.substring(0, this.item_id_str.length - 1);
  }

  public collectSaveData() {
    this.sendData = {
      'name': this.tableName,
      'desc': this.description,
      'coll_policy_id': this.selectedRowObj['policyNo'],
      'coll_policy_group_id': this.selectedRowObj['cpGroup_id'],
      'item_id': this.item_id_str,
      'group_id': this.selectedRowObj['groupNo']
    };
    if (this.tree_id) {
      if (this.tree_id !== 'snmp_oid') {
        this.sendData['tree_id'] = this.tree_id;
      }
      return true;
    } else {
      alert('リーフを選択してください！');
      return false;
    }
  }
  public saveTableData() {
    let isTreeId = this.collectSaveData();
    if (isTreeId) {
      if (this.item_id_str) {
        let url = '/api_data_table_step1/';
        this.post(url, this.sendData).subscribe((res: any) => {
          if (res && res.status) {
            if (res.status.status && res.status.status.toLowerCase() === 'false') {
              let msg = res.status.message;
              alert(msg);
            } else {
              this.bsModalRef.hide();
              alert('保存しました！');
              $('#tableTable').trigger('reloadGrid');
            }
          }
        });
      } else {
        alert('データ取得に異常が発生しました、アドミニストレータに連絡してください！');
      }
    }


  }

  // common function of http

  private get(url: string) {
    return this.httpClient.toJson(this.httpClient.get(url));
  }

  private post(url: string, bodyData: any) {
    return this.httpClient.toJson(this.httpClient.post(url, bodyData));
  }
}
