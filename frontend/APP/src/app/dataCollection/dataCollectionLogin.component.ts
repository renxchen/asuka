import { Component, OnInit, AfterViewInit, enableProdMode} from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import * as _ from 'lodash';
declare var $: any;
import * as flatpickr from 'flatpickr';

enableProdMode();

@Component({
    selector: 'dc-login',
    templateUrl: 'dataCollectionLogin.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DataCollectionLoginComponent implements OnInit, AfterViewInit {
    apiPrefix: any = '/v1';
    title: string;
    id: number = -1;

    startDateTime: any;
    endDateTime: any;

    flatPickrStartDateTime: any;
    flatPickrEndDateTime: any;

    pickrOption: any = {
        enableTime: true,
        time_24hr: true,
        static: true
    };

    startTime: any;
    endTime: any;

    flatPickrStartTime: any;
    flatPickrEndTime: any;

    isEnabled: boolean = false;
    isLock: boolean = false;
    isProcessing: boolean = false;

    selectedOsType: string;
    osType: any = [];

    priority: any;
    priorities: any = [{id: 0, value: '標準'}, {id: 1, value: '高'}];

    deviceGroup: any;
    deviceGroups: any = [];

    policyGroup: any;
    policyGroups: any = [];

    validPeriodType: any;
    validPeriodTypes: any = [{id: 0, value:'期間なし'}, {id: 1, value: '期間あり'}];

    dataScheduleType: any;
    dataScheduleTypes: any = [{id: 0, value:'常に取得'}, {id: 1, value: '取得停止'}, {id: 2, value: '周期取得'}];
    weekdays: any = [
        {id: 1, value: '月', ifCheck: ''},
        {id: 2, value: '火', ifCheck: ''},
        {id: 3, value: '水', ifCheck: ''},
        {id: 4, value: '木', ifCheck: ''},
        {id: 5, value: '金', ifCheck: ''},
        // {id: 5, value: '金', ifCheck: 'checked'},
        {id: 6, value: '土', ifCheck: ''},
        {id: 7, value: '日', ifCheck: ''}
    ];

    constructor(
        private router: Router,
        private activeRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        public bsModalRef: BsModalRef
    ) { }

    ngOnInit() {
        this.httpClient.setUrl(this.apiPrefix);

    }

    ngAfterViewInit() {
        this.initPickr();
        this.initPickrTime();
        setTimeout(() => {
            $('#validPeriod').hide();
            $('#dataSchedule').hide();
            if(this.id == -1){
                this.getOsTypes();
                this.setInitSelect();
                $('button.btn-danger').hide();
            } else {
                this.getDetailById(this.id);
            }
        },0);
    }

    getOsTypes() {
        this.httpClient
            .toJson(this.httpClient.get('/api_new_data_collection/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        this.osType = res['data'];
                        if(this.selectedOsType == null){
                            this.selectedOsType = this.osType[0]['ostypeid'].toString();
                        }
                        this.getGroups();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }

    getGroups() {
        this.httpClient
            .toJson(this.httpClient.get('/api_new_data_collection/?ostype_id='+this.selectedOsType))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    this.deviceGroups = res['device_groups'];
                    this.policyGroups = res['cp_groups'];

                    if (this.deviceGroups.length == 0){
                        this.deviceGroup = 0;
                    } else {
                        if (this.id == -1) {
                            this.deviceGroup = this.deviceGroups[0]['group_id'].toString();
                        }
                    }

                    if (this.policyGroups.length == 0){
                        this.policyGroup = 0;
                    } else {
                        if (this.id == -1) {
                            this.policyGroup = this.policyGroups[0]['policy_group_id'].toString();
                        }
                        if (this.priority == 1){
                            this.policyGroups.unshift({policy_group_id:-1, name: '全機能OFF'});
                        }
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }

    changePriority(){
        if (this.policyGroups.length != 0){
            if (this.priority == 1 && this.policyGroups[0]['policy_group_id'] != -1) {
                this.policyGroups.unshift({policy_group_id:-1, name: '全機能OFF'});
            } else if(this.priority == 0 && this.policyGroups[0]['policy_group_id'] == -1) {
                this.policyGroups.shift();
                $('input[name="dataScheduleType"][value="1"]').attr('disabled', false);
                if (this.policyGroup == -1) {
                    this.policyGroup = this.policyGroups[0]['policy_group_id'].toString();
                }
            }
        }
    }

    changeCPG(){
        if (this.policyGroup == -1) {
            $('input[name="dataScheduleType"][value="1"]').attr('disabled', true).prop('checked', false);
            if (this.dataScheduleType == 1) {
                this.dataScheduleType = 0;
                $('input[name="dataScheduleType"][value="0"]').prop('checked', true);
                console.log(this.dataScheduleType);
            }
        } else {
            $('input[name="dataScheduleType"][value="1"]').attr('disabled', false);
        }
    }

    initPickr() {
        let startDateEle = document.getElementById('startDateTimeInput');
        let endDateEle = document.getElementById('endDateTimeInput');
        this.flatPickrStartDateTime = new flatpickr(startDateEle, this.pickrOption);
        this.flatPickrEndDateTime = new flatpickr(endDateEle, this.pickrOption);
    }

    initPickrTime() {
        let startOp: any = {
            noCalendar: true,
            dateFormat: 'H:i',
            enableTime: true,
            time_24hr: true,
            defaultDate: '00:00'
        };
        let endOp: any = {
            noCalendar: true,
            dateFormat: 'H:i',
            enableTime: true,
            time_24hr: true,
            defaultDate: '23:59'
        };

        this.startTime = '00:00';
        this.endTime = '23:59';
        let startEle = document.getElementById('startTimeInput');
        let endEle = document.getElementById('endTimeInput');
        this.flatPickrStartTime = new flatpickr(startEle, startOp);
        this.flatPickrEndTime = new flatpickr(endEle, endOp);
    }

    setMaxAndMinDate(type) {
        /**
         * Date:20180416
         * @author necy
         * @param type : starttime or endtime flg
         * brief :set the max value or min value of flatpickr plugin
         */
        if (this.startDateTime && type === 'start') {
          this.flatPickrEndDateTime.set('minDate', this.startDateTime, this.endDateTime);
        }
        if (this.endDateTime && type === 'end') {
          this.flatPickrStartDateTime.set('maxDate', this.endDateTime, this.startDateTime);
        }
    }

    setMaxAndMinTime(type) {
        /**
         * Date:20180416
         * @author necy
         * @param type : starttime or endtime flg
         * brief :set the max value or min value of flatpickr plugin
         */
        if (this.startTime && type === 'start') {
          this.flatPickrEndTime.set('minDate', this.startTime, this.endTime);
        }
        if (this.endTime && type === 'end') {
          this.flatPickrStartTime.set('maxDate', this.endTime, this.startTime);
        }
    }

    updateTime(hour:number, minute:number){
        let d = new Date();
        d.setHours(hour);
        d.setMinutes(minute);
        return d;
    }

    getDetailById(id){
        let url = '/api_data_collection/?id=' + id;
        this.httpClient.toJson(this.httpClient.get(url)).subscribe(res => {
            if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                if (res['data']) {
                    let data = res['data'];
                    let valid_period_type = _.get(data, 'valid_period_type');
                    $('input[name="validPeriodType"][value="'+valid_period_type+'"]').attr('checked','checked');
                    this.changeValidPeriodType(valid_period_type);
                    let data_schedule_type = _.get(data, 'data_schedule_type');
                    $('input[name="dataScheduleType"][value="'+data_schedule_type+'"]').attr('checked','checked');
                    this.changeDataScheduleType(data_schedule_type);

                    this.id = _.get(data, 'schedule_id');
                    this.selectedOsType = _.get(data, 'ostype_id');
                    this.priority = _.get(data, 'priority');
                    this.deviceGroup = _.get(data, 'device_group_id');
                    this.policyGroup = _.get(data, 'policy_group_id');
                    this.getOsTypes();

                    this.isProcessing = _.get(res, 'isProcessing');
                    this.setSchedule(this.isProcessing);
                    if (this.isProcessing){
                        this.isLock = true;
                    } else {
                        this.isLock = _.get(res, 'isLock');
                    }
                    this.setOsDgPg(this.isLock);

                    if (this.validPeriodType == 1){
                        let start_period_time = _.get(data, 'start_period_time');
                        let end_period_time = _.get(data, 'end_period_time');
                        if(start_period_time != null && end_period_time != null){
                            this.startDateTime = start_period_time.replace('@', ' ');
                            this.endDateTime = end_period_time.replace('@', ' ');
                        }
                    }

                    if (this.dataScheduleType == 2){
                        this.startTime = _.get(data, 'schedule_start_time');
                        this.endTime = _.get(data, 'schedule_end_time');

                        let weeks: any = _.get(data, 'weeks');
                        for (let i=0; i< this.weekdays.length; i++){
                            if (weeks.indexOf(this.weekdays[i]['id'].toString()) != -1){
                                this.weekdays[i]['ifCheck'] = 'checked';
                            }
                        }
                    }
                }
            } else {
                if (res['status'] && res['status']['message']) {
                    alert(res['status']['message']);
                }
            }
        });
    }

    setInitSelect() {
        $('input[value="0"]').prop('checked', true);
        // $('input[name="dataScheduleType"][value="1"]').prop('checked', true);
        this.dataScheduleType = 0;
        this.validPeriodType = 0;
        this.priority = 0;
    }

    setOsDgPg(flag: boolean){
        $('#osType').prop('disabled', flag);
        $('#deviceGroup').prop('disabled', flag);
        $('#policyGroup').prop('disabled', flag);
    }

    setSchedule(flag: boolean){
        $('#priority').prop('disabled', flag);
        $('input[name="validPeriodType"]').prop('disabled', flag);
        $('input[name="startDate"]').prop('disabled', flag);
        $('input[name="endDate"]').prop('disabled', flag);
        if (flag) {
            this.isEnabled = flag;
            $('div.down-place').css('margin-top', '25px');
            if(this.dataScheduleType == 0){
                $('input[name="dataScheduleType"][value="2"]').prop('disabled', flag);
            }
        }
        $('input[name="weekday"]').prop('disabled', flag);
    }

    changeOsType() {
        this.getGroups();
    }

    changeValidPeriodType(id: number){
        this.validPeriodType = id;
        // console.log(this.validPeriodType);
        if (id == 1){
            $('#validPeriod').show();
        } else {
            $('#validPeriod').hide();
        }
    }

    changeDataScheduleType(id: number){
        this.dataScheduleType = id;
        // console.log(this.dataScheduleType);
        if (id == 2){
            $('#dataSchedule').show();
        } else {
            $('#dataSchedule').hide();
        }
    }

    changeWeekdays(id) {
        if (this.weekdays[id-1]['ifCheck'] == 'checked'){
            this.weekdays[id-1]['ifCheck'] = '';
        } else {
            this.weekdays[id-1]['ifCheck'] = 'checked';
        }
    }

    save() {
        let dataScheduleTime = '';
        for (let i=0; i<this.weekdays.length; i++){
            if(this.weekdays[i]['ifCheck'] == 'checked'){
                dataScheduleTime += this.weekdays[i]['id']+';';
            }
        }

        let checkResult = this.doCheck(dataScheduleTime);
        let flag = checkResult['flag'];
        let message = checkResult['message'];

        if (flag) {
            let startPeriodTime = '';
            let endPeriodTime = '';
            if (this.validPeriodType == 1){
                startPeriodTime = this.startDateTime.replace(' ', '@');
                endPeriodTime = this.endDateTime.replace(' ', '@');
            }

            if (dataScheduleTime != '' && this.dataScheduleType == 2){
                dataScheduleTime = dataScheduleTime.substring(0,dataScheduleTime.length-1)+'@'+this.startTime+'-'+this.endTime;
            } else {
                dataScheduleTime = '';
            }

            let scheduleInfo: any = {};
            let url_new = '/api_new_data_collection/';
            let url_edit = '/api_data_collection/';

            scheduleInfo['ostype_id'] = this.selectedOsType;
            scheduleInfo['priority'] = this.priority.toString();
            scheduleInfo['device_group_id'] = this.deviceGroup;
            scheduleInfo['policy_group_id'] = this.policyGroup;
            scheduleInfo['valid_period_type'] = this.validPeriodType.toString();
            scheduleInfo['start_period_time'] = startPeriodTime;
            scheduleInfo['end_period_time'] = endPeriodTime;
            scheduleInfo['data_schedule_type'] = this.dataScheduleType.toString();
            scheduleInfo['data_schedule_time'] = dataScheduleTime;
            scheduleInfo['period_time'] = '';
            scheduleInfo['weeks'] = '';
            scheduleInfo['is_lock'] = this.isLock;
            scheduleInfo['is_processing'] = this.isProcessing;

            console.log(scheduleInfo);

            if (this.id == -1){
                this.httpClient
                    .toJson(this.httpClient.post(url_new, scheduleInfo))
                    .subscribe(res => {
                        $('#dcTable').trigger("reloadGrid");
                        if (res['status']['status'].toString().toLowerCase() === 'true') {
                            if (res['status']['message'] == "Success") {
                               alert('追加しました。');
                            }
                        } else {
                            alert(res['status']['message']);
                        }
                });
                this.bsModalRef.hide();
            } else {
                scheduleInfo['schedule_id'] = this.id.toString();
                this.httpClient
                    .toJson(this.httpClient.put(url_edit, scheduleInfo))
                    .subscribe(res => {
                        $('#dcTable').trigger("reloadGrid");
                        if (res['status']['status'].toString().toLowerCase() === 'true') {
                            if (res['status']['message'] == "Success") {
                                alert('更新しました。');
                            }
                        } else {
                            alert(res['status']['message']);
                        }
                });
                this.bsModalRef.hide();
            }
        } else {
            alert(message);
        }
    }

    doCheck(dataScheduleTime){
        let result: any = {};
        let flag: boolean = true;
        let message: string = '';
        console.log(this.startDateTime, this.endDateTime);
        if (this.policyGroup == 0 || this.deviceGroup == 0){
            flag = false;
            message += "Please make sure correct group is selected.";
        }
        // check date and time when valid period type is 1 (with period)
        if (this.validPeriodType == 1) {
            if(!this.startDateTime || !this.endDateTime){
                flag = false;
                message += "Please set period date.";
            }
        }
        // // check if any days has been select when data schedule type is 2 (periodic collection)
        if (this.dataScheduleType == 2) {
            if (dataScheduleTime == ''){
                flag = false;
                message += 'Periodic collection with no weekday selected!';
            }
        }
        result['flag'] = flag;
        result['message'] = message;
        return result;
    }

    delete() {
        let isDelete: boolean = confirm('該当データ取得を削除します。よろしいですか？');
        if (isDelete){
            let url = '/api_data_collection/?id=' + this.id;
            this.httpClient
                .toJson(this.httpClient.delete(url))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['status']['message'] == "Success") {
                            alert('削除しました。');
                            $('#dcTable').trigger("reloadGrid");
                        }
                    } else {
                        alert(res['status']['message']);
                    }
                });
            this.bsModalRef.hide();
        } else {
        }
    }

}
