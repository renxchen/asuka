/*!@brief data collection view page

* @author Necy Wang
* @date 2018/01/04
*/
import { Component, OnInit, AfterViewInit} from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Router } from '@angular/router';
import { DataCollectionLoginComponent } from './dataCollectionLogin.component';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'dc-view',
    templateUrl: 'dataCollectionView.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DataCollectionViewComponent implements OnInit, AfterViewInit {

    testData: any = [
        {dcNo: 10, priority: '標準', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '期間なし', scheduleType: '常に取得',  status: '無効'},
        {dcNo: 20, priority: '高', ostype: 'Cisco_IOSXR',
        deviceGroup: 'Cisco AER', cpGroup: 'Cisco AER 基本監視',
        validPeriod: '2017/12/12 23:59\n– 2018/1/12 23:59', scheduleType: '取得停止',  status: '有効'},
    ];
    dcModel: any = [
        {label: 'No', hidden: true, name: 'schedule_id', index: 'schedule_id'},
        {label: '優先度',  name: 'priority', width: 30, align: 'center',
            formatter: this.formatterPriority},
        {label: 'OS Type', name: 'ostype_name', width: 50, align: 'center'},
        {label: 'DeviceGroupNo', hidden: true, name: 'device_group_id', index: 'device_group_id'},
        {label: 'デバイスグループ',  name: 'device_group_name', width: 80, align: 'center', classes: 'deviceGroup'},
        {label: 'PolicyGroupNo', hidden: true, name: 'policy_group_id', index: 'policy_group_id'},
        {label: 'コレクションポリシーグループ名',  name: 'policy_group_name', width: 100, align: 'center',
            classes: 'policyGroup', formatter: this.formatterCollectionPolicyGroup
        },
        {label: '開始日時',  name: 'start_period_time', width: 65, align: 'center',
            formatter: this.formatterTime,
        },
        {label: '終了日時',  name: 'end_period_time', width: 65, align: 'center',
            formatter: this.formatterTime,
        },
        {label: '取得方法', name: 'data_schedule_type', width: 45, align: 'center',
            formatter: this.formatterScheduleType
        },
        {label: 'ステータス', name: 'schedules_is_valid', width: 45, align: 'center', classes: 'status',
            formatter: this.formatterStatus
        },
        {label: 'アクション', name: 'action', width: 45, align: 'center', search: false,
            formatter: this.fomatterBtn, sortable: false
        }
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
    ) {}

    ngOnInit() {

    }

    ngAfterViewInit() {
        this.drawDCTable();
    }

    fomatterBtn(cellvalue, options, rowObject) {
        /*!@brief
        * @param
        * @pre
        * @return
        */
        return '<button class="btn btn-xs btn-success edit" id='+ rowObject["schedule_id"] + '><i class="fa fa-pencil-square"></i> 編集</button>'
    }

    formatterCollectionPolicyGroup(cellvalue, options, rowObject){
        let result;
        if (cellvalue == "ALL FUNCTIONS OFF"){
            result = '全機能OFF';
        } else {
            result = cellvalue;
        }
        return result;
    }

    formatterStatus(cellvalue, options, rowObject){
        let result;
        if (rowObject['schedules_is_valid'] == 0){
            // result = '無効';
            result = '<a href="#" class = "btn btn-default btn-xs disabled">無効</a>';
        } else if (rowObject['schedules_is_valid'] == 1){
            // result = '有効';
            result = '<a href="#" class = "btn btn-primary btn-xs disabled">有効</a>'
        } else {
            result = rowObject['schedules_is_valid'];
        }
        return result;
    }

    formatterPriority(cellvalue, options, rowObject){
        let result;
        if (rowObject['priority'] == 0){
            result = '標準';
        } else if (rowObject['priority'] == 1){
            result = '高';
        } else {
            result = rowObject['priority'];
        }
        return result;
    }

    formatterScheduleType(cellvalue, options, rowObject){
        let result;
        if (rowObject['data_schedule_type'] == 0){
            result = '常に取得';
        } else if(rowObject['data_schedule_type'] == 1) {
            result = '取得停止';
        } else if(rowObject['data_schedule_type'] == 2) {
            result = '周期取得';
        } else {
            result = rowObject['data_schedule_type'];
        }
        return result;
    }

    formatterTime(cellvalue, options, rowObject){
        if (cellvalue == null){
            return '——';
        } else {
            return cellvalue.replace('@', ' ');
        }

    }

    renderLink(){
        /*
        @brief Render jump lick for device group and policy group
        @pre After loading table data
         */
        let _this = this;
        let _deviceGroup = $('.deviceGroup');
        for (let i=0;i<_deviceGroup.length;i++){
            let _target = $(_deviceGroup[i]);
            let _content = '<div style="color:blue; text-decoration: underline;cursor: pointer">';
            _content += _target.html() + '</div>';
            _target.html(_content);
            let deviceGroupNo = _target.prev().html();
            _target.click( function (event) {
                if (deviceGroupNo != ""){
                   _this.router.navigate(['/index/devicegroup'],{queryParams:{'id':deviceGroupNo}});
                }

            })
        }

        let _policyGroup = $('.policyGroup');
        for (let i=0;i<_policyGroup.length;i++){
            let _target = $(_policyGroup[i]);
            let _content = '';
            if (_target.html() != '全機能OFF'){
                _content += '<div style="color:blue; text-decoration: underline;cursor: pointer">';
                _content += _target.html() + '</div>';
                let policyGroupNo = _target.prev().html();
                _target.click( function (event) {
                    if (policyGroupNo != ""){
                        _this.router.navigate(['/index/cpgdetail'],{queryParams:{'id':policyGroupNo}});
                    }

                });
            } else {
                _content = _target.html();
            }
            _target.html(_content);

        }
    }

    newDC() {
        // open modal
        this.modalRef = this.modalService.show(DataCollectionLoginComponent, this.modalConfig);
        // init the title of modal
        this.modalRef.content.title = 'データ取得新規';

    }

    editDC(){
        let _this = this;
        $('.edit').click(function (event) {
            let id = $(event)[0].target.id;
            // open modal and init the title and id of modal
            _this.modalRef = _this.modalService.show(DataCollectionLoginComponent, _this.modalConfig);
            _this.modalRef.content.title = 'データ取得編集';
            _this.modalRef.content.id = id;
        });
    }


    drawDCTable() {
        let _this = this;
        $('#dcTable').jqGrid({
            url: '/v1/api_data_collection/',
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: this.dcModel,
            // postData: { '': '' },
            // data: this.testData,
            // viewrecords: true,
            loadComplete: function(res) {
                let status = _.get(_.get(res, 'status'), 'status');
                let code: any = _.get(_.get(res, 'status'), 'code');
                let msg: any = _.get(_.get(res, 'status'), 'message');
                if (status === 'False') {
                    if (code === 102 || code === 103) {
                        localStorage.setItem('sessionTimeOut', msg);
                        _this.router.navigate(['/login/']);
                    }
                }
                _this.editDC();
                _this.renderLink();
                // _this.renderColor();
            },
            rowNum: 10,
            rowList: [ 10, 20, 30],
            autowidth: true,
            beforeSelectRow: function(rowid, e) { return false; },
            height: 230,
            pager: '#dcPager',
            jsonReader: {
                root: 'data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });
        $('#dcTable').jqGrid('filterToolbar', {defaultSearch: 'cn'});
    }
}
