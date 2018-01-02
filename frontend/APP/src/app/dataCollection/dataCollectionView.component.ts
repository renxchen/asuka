import { Component, OnInit, ComponentFactoryResolver, AfterViewInit, ElementRef } from '@angular/core';
import * as _ from 'lodash';
declare var $: any;
// import { DataCollectionService } from './dataCollection.service';
@Component({
    selector: 'dc-view',
    templateUrl: 'dataCollectionView.component.html',
    styleUrls: ['dataCollection.component.less']
})
export class DataCollectionViewComponent implements OnInit, AfterViewInit {
    cpType: any;
    model: any;
    testData: any = [
        {dcNo: 1, priority: '標準', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '期間なし', scheduleType: '常に取得',  status: '無効'},
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
        {label: 'コレクションポリシーグループ名',  name: 'cpGroup', width: 80, align: 'center'},
        {label: '有効期間',  name: 'validPeriod', width: 50, align: 'center'},
        {label: '取得方法', name: 'scheduleType', width: 50, align: 'center'},
        {label: 'ステータス', name: 'status', width: 50, align: 'center', class: 'btn btn-success'},
        {label: 'アクション', name: 'action', width: 50, align: 'center', search: false,
        formatter: this.fomatterBtn
        }
    ];
    constructor(
      // private dataCollectionService: DataCollectionService
    ) {}
    ngOnInit() {
        // this.cpType = 'cli';
        this.model = this.dcModel;
    }
    ngAfterViewInit() {
        this.drawCPTable();
    }
    public fomatterBtn(cellvalue, options, rowObject) {
        // console.log(options);
        return '<button class="btn btn-xs btn-success edit"><i class="fa fa-pencil-square"></i> 編集</button>'
        // return '<input type="button" value="delete" class="btn-default" name=' + cellvalue + ' >';
    };
    public newDC() {
      alert("new!");
      // init and open modal
    }

    public drawCPTable() {
        $('#dcTable').jqGrid({
            // url: 'getTableData',
            // mtype: 'GET',
            colModel: this.model,
            datatype: 'local',
            data: this.testData,
            viewrecords: true,
            rowNum: 10,
            rowList: [ 10, 20, 30],
            autowidth: true,
            // height: 400,
            pager: '#dcPager',
            emptyrecords: 'Nothing to display'
        });
        $('#dcTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}
