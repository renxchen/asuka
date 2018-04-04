import { Component, OnInit, AfterViewInit, enableProdMode} from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import * as _ from 'lodash';
declare var $: any;

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

    // minDate = new Date(2017, 5, 10);
    // maxDate = new Date(2018, 10, 15);
    bsValue: Date = new Date();
    isTimeMeridian: boolean = false;
    isValid: boolean;

    startDateTime: Date = new Date(2018, 0, 1, 0, 0);
    endDateTime: Date = new Date(2018, 0, 1, 23, 59);

    startTime: Date = new Date(2018, 1, 1, 0, 0);
    endTime: Date = new Date(2018, 1, 1, 23, 59);

    isEnabled: boolean = false;
    isLock: boolean = false;
    isProcessing: boolean = false;

    // bsRangeValue: any = [new Date(2017, 7, 4), new Date(2017, 7, 20)];

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
                    // if (res['data']) {
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

                    // }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
        // this.deviceGroups = [{id: 0, name: 'device group 1'}, {id:1, name: 'device group 2'}];
        // this.policyGroups = [{id: 0, name: 'cpg 1'}, {id:1, name: 'cpg 2'}];


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

                    // setTimeout(function () {
                    //     this.validPeriodType = _.get(data, 'valid_period_type');
                    //     this.dataScheduleType = _.get(data, 'data_schedule_type');
                    // },0);


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
                    // console.log(this.isProcessing);
                    this.setSchedule(this.isProcessing);
                    if (this.isProcessing){
                        this.isLock = true;
                    } else {
                        this.isLock = _.get(res, 'isLock');
                    }
                    this.setOsDgPg(this.isLock);

                    let start_period_time = _.get(data, 'start_period_time');
                    let end_period_time = _.get(data, 'end_period_time');
                    if(start_period_time != null && end_period_time != null){
                        $('input[name="startDate"]').val(_.get(data, 'start_period_time').split(' ')[0]);
                        $('input[name="endDate"]').val(_.get(data, 'end_period_time').split(' ')[0]);

                        let spt = _.get(data, 'start_period_time').split(' ')[1];
                        let ept = _.get(data, 'end_period_time').split(' ')[1];
                        this.startDateTime = this.updateTime(parseInt(spt.split(':')[0]),parseInt(spt.split(':')[1]));
                        this.endDateTime = this.updateTime(parseInt(ept.split(':')[0]),parseInt(ept.split(':')[1]));
                    }

                    let sst = _.get(data, 'schedule_start_time');
                    let set = _.get(data, 'schedule_end_time');
                    this.startTime = this.updateTime(parseInt(sst.split(':')[0]),parseInt(sst.split(':')[1]));
                    this.endTime = this.updateTime(parseInt(set.split(':')[0]),parseInt(set.split(':')[1]));

                    let weeks: any = _.get(data, 'weeks');
                    for (let i=0; i< this.weekdays.length; i++){
                        if (weeks.indexOf(this.weekdays[i]['id'].toString()) != -1){
                            this.weekdays[i]['ifCheck'] = 'checked';
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
        console.log(this.validPeriodType);
        if (id == 1){
            $('#validPeriod').show();
        } else {
            $('#validPeriod').hide();
        }
    }

    changeDataScheduleType(id: number){
        this.dataScheduleType = id;
        console.log(this.dataScheduleType);
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

    filledToTwoNumber(num){
        if (num < 10){
            num = "0" + num.toString();
        }
        return num
    }

    save() {
        let f = true;
        let m = "";
        if (this.startDateTime == null || this.endDateTime == null) {
            f = false;
            m += 'The format of date time is wrong';
        } else if(this.startTime == null || this.endTime == null){
            f = false;
            m += 'The format of period time is wrong';
        }
        console.log(this.startDateTime.getHours());
        if (!f) {
            // alert(m);
            return;
        }

        let startDate = $('input[name="startDate"]').val();
        let startPeriodTime = '';
        if (this.validPeriodType == 1 && startDate != ''){
            startPeriodTime = startDate+'@'
                +this.filledToTwoNumber(this.startDateTime.getHours())+':'
                +this.filledToTwoNumber(this.startDateTime.getMinutes());
        }

        let endDate = $('input[name="endDate"]').val();
        let endPeriodTime = '';
        if (this.validPeriodType == 1 && endDate != ''){
            endPeriodTime = endDate+'@'
                +this.filledToTwoNumber(this.endDateTime.getHours())+':'
                +this.filledToTwoNumber(this.endDateTime.getMinutes());
        }

        let dataScheduleStartTime = this.filledToTwoNumber(this.startTime.getHours())
            +':'+this.filledToTwoNumber(this.startTime.getMinutes());
        let dataScheduleEndTime = this.filledToTwoNumber(this.endTime.getHours())
            +':'+this.filledToTwoNumber(this.endTime.getMinutes());
        let dataScheduleTime = '';
        for (let i=0; i<this.weekdays.length; i++){
            if(this.weekdays[i]['ifCheck'] == 'checked'){
                dataScheduleTime += this.weekdays[i]['id']+';';
            }
        }
        if (dataScheduleTime != ''){
            dataScheduleTime = dataScheduleTime.substring(0,dataScheduleTime.length-1)+'@'+dataScheduleStartTime+'-'+dataScheduleEndTime;
        }

        let checkResult = this.doCheck(startDate, endDate, dataScheduleTime);
        let flag = checkResult['flag'];
        let message = checkResult['message'];

        if (flag) {
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
            // alert(flag);
            // return;
            if (this.id == -1){
                this.httpClient
                    .toJson(this.httpClient.post(url_new, scheduleInfo))
                    .subscribe(res => {
                        $('#dcTable').trigger("reloadGrid");
                        if (res['status']['status'].toString().toLowerCase() === 'true') {
                            if (res['status']['message'] == "Success") {
                               alert('データ取得追加しました。');
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
                                alert('データ取得更新しました。');
                                // let id = res['data']['coll_policy_id'];
                                // this.router.navigate(['/index/cliCPEdit'],
                                //     { queryParams: { 'id': id } });
                            }
                        } else {
                            alert(res['status']['message']);
                            // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                            //     this.uniqueFlg = false;
                            // } else {
                            //     alert(res['status']['message']);
                            // }
                        }
                });
                this.bsModalRef.hide();
            }
        } else {
            alert(message);
        }

    }

    doCheck(startDate, endDate, dataScheduleTime){
        let result: any = {};
        let flag: boolean = true;
        let message: string = '';
        console.log(startDate, endDate);
        console.log(this.startDateTime.getTime(), this.endDateTime.getTime());
        // check date and time when valid period type is 1 (with period)
        if (this.policyGroup == 0 || this.deviceGroup == 0){
            flag = false;
            message += "Please make sure correct group is selected.";
        }
        if (this.validPeriodType == 1) {
            let reg = /^\d{4}-\d{2}-\d{2}$/;
            if(startDate == "" || endDate == ""){
                flag = false;
                message += "Please set period date.";
                console.log(reg.test(startDate));
                console.log(reg.test(endDate));
            }else if (!reg.test(startDate) || !reg.test(endDate)){
                flag = false;
                message += "The format of date is wrong.";
            } else if(startDate > endDate) {
                flag = false;
                message += "The start date cannot earlier than the end date.";
            }  else if(startDate == endDate && this.startDateTime > this.endDateTime) {
                flag = false;
                message += "The start time cannot earlier than the end time for the same date.";
            }
            // check date all selected; format right; start<=end
            // if same date, check start time < end time
        }
        // check if any days has been select when data schedule type is 3 (periodic collection)
        if (this.dataScheduleType == 2) {
            if (dataScheduleTime == ''){
                flag = false;
                message += 'Periodic collection with no weekday selected!';
            } else if(this.startTime > this.endTime) {
                flag = false;
                message += "The start time cannot earlier than the end time for period collection.";
            }
        }

        result['flag'] = flag;
        result['message'] = message;
        console.log(result);
        return result;

    }

    delete() {
        let isDelete: boolean = confirm('delete?');
        if (isDelete){
            let url = '/api_data_collection/?id=' + this.id;
            this.httpClient
                .toJson(this.httpClient.delete(url))
                .subscribe(res => {
                    console.log('delete',res);
                    alert(res['status']['status'].toString());
                    $('#dcTable').trigger("reloadGrid");
                });

            this.bsModalRef.hide();
        } else {

        }
    }

}
