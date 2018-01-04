import { Component, OnInit, ComponentFactoryResolver, AfterViewInit, ElementRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { DataCollectionLoginComponent } from './dataCollectionLogin.component';
import { CLICPLoginComponent } from '../collectionPolicy/cliCPLogin.component'
import * as _ from 'lodash';
declare var $: any;
// import { DataCollectionService } from './dataCollection.service';
@Component({
    selector: 'dc-view',
    templateUrl: 'dataCollectionView.component.html',
    styleUrls: ['dataCollection.component.less']
})
export class DataCollectionViewComponent implements OnInit, AfterViewInit {

    model: any;
    testData: any = [
        {dcNo: 10, priority: '標準', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '期間なし', scheduleType: '常に取得',  status: '無効'},
        {dcNo: 20, priority: '高', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '2017/12/12 23:59\n– 2018/1/12 23:59', scheduleType: '取得停止',  status: '有効'},
        // {cpNo: 2, cPName: 'ishiba_test_01', ostype: 'cisco-ios', oid: '$#$3', commond: 'show interface', summary: 'test'},
        // {cpNo: 3, cPName: 'ishiba_test_02', ostype: 'cisco-ios', oid: '$#$8', commond: 'show file systems', summary: 'file'},
        // {cpNo: 4, cPName: 'ishiba_test_03', ostype: 'cisco-ios', oid: '$#$2', commond: 'show data', summary: 'data'},
        // {cpNo: 5, cPName: 'masaykan_test_01', ostype: 'cisco-ios', oid: '$#$6', commond: 'show ip route', summary: 'route'},
        // {cpNo: 6, cPName: 'masaykan_test', ostype: 'cisco-ios', oid: '$#$7', commond: 'show file', summary: 'open_file'},
    ];
    dcModel: any = [
        {label: 'No', hidden: true, name: 'dcNo', index: 'dcNo'},
        {label: '優先度',  name: 'priority', width: 30, align: 'center'},
        {label: 'OS Type', name: 'ostype', width: 50, align: 'center'},
        {label: 'デバイスグループ',  name: 'deviceGroup', width: 80, align: 'center'},
        {label: 'コレクションポリシーグループ名',  name: 'cpGroup', width: 100, align: 'center'},
        {label: '有効期間',  name: 'validPeriod', width: 60, align: 'center'},
        {label: '取得方法', name: 'scheduleType', width: 50, align: 'center'},
        {label: 'ステータス', name: 'status', width: 50, align: 'center', classes: 'status'},
        {label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
        formatter: this.fomatterBtn
        }
    ];
    modalRef: BsModalRef;
    config = {
        animated: true,
        keyboard: true,
        backdrop: true,
        ignoreBackdropClick: false
      };
    constructor(private modalService: BsModalService) {}

    ngOnInit() {
        // this.cpType = 'cli';
        this.model = this.dcModel;
        // this.drawCPTable();
    }
    ngAfterViewInit() {
        this.drawCPTable();
    }
    public fomatterBtn(cellvalue, options, rowObject) {
        // console.log(rowObject);
        return '<button class="btn btn-xs btn-success edit" id='+ rowObject["dcNo"] + '><i class="fa fa-pencil-square"></i> 編集</button>'
    };
    newDC() {
        console.log("aaa");
        this.modalRef = this.modalService.show(CLICPLoginComponent, this.config);
      // init and open modal
    }
    public editDC(){
        $('.edit').click(function (event) {
            let id = $(event)[0].target.id;
            console.log('id', id);
            alert("id="+id);

        });
    }

    public renderColor(){
        let _this = $('.status');
        for (let i=0;i<_this.length;i++){
            let _target = $(_this[i]);
            if (_target.html().search('無効') != -1){
                _target.html('<a href="#" class = "btn btn-default btn-xs disabled">無 効</a>');
            } else {
                _target.html('<a href="#" class = "btn btn-primary btn-xs disabled">有 効</a>');
            }
        }


    }

    public drawCPTable() {
        let _t = this;
        $('#dcTable').jqGrid({
            // url: 'getTableData',
            // mtype: 'GET',
            colModel: this.model,
            datatype: 'local',
            data: this.testData,
            viewrecords: true,
            gridComplete: function() {
                _t.editDC();
                _t.renderColor();
            },
            rowNum: 10,
            rowList: [ 10, 20, 30],
            autowidth: true,
            beforeSelectRow: function(rowid, e) { return false; },
            // height: 400,
            pager: '#dcPager',
            // emptyrecords: 'Nothing to display'
        });
        $('#dcTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}
