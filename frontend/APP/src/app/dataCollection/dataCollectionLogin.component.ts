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

    startDateTime: Date = new Date(2018, 0, 1, 0, 0);
    endDateTime: Date = new Date(2018, 0, 1, 23, 59);

    startTime: Date = new Date(2018, 1, 1, 0, 0);
    endTime: Date = new Date(2018, 1, 1, 23, 59);

    // bsRangeValue: any = [new Date(2017, 7, 4), new Date(2017, 7, 20)];

    selectedOsType: string;
    osType: any = [];

    priority: any;
    priorities: any = [{id: 0, value: '標準'}, {id: 1, value: '高'}];

    deviceGroup: any;
    deviceGroups: any = [];

    policyGroup: any;
    policyGroups:any = [];

    validPeriodType:any;
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

    // modalTitle:string;
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
           if(this.id == -1){
                this.getOsTypes();
                this.setInitSelect();
                $('button.btn-danger').hide();
                $('#validPeriod').hide();
                $('#dataSchedule').hide();
            } else {
                this.getOsTypes();
                //set init value for this id
               // $('button.btn-primary').attr('disabled','disabled');
            }
        },0);
    }

    getOsTypes() {
        this.httpClient
            .toJson(this.httpClient.get('/api_new_data_collection/new/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        this.osType = res['data'];
                        this.selectedOsType = this.osType[0]['ostypeid'].toString();
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
                        if (this.id == -1) {
                            this.deviceGroup = this.deviceGroups[0]['group_id'].toString();
                            this.policyGroup = '-1';
                        } else {
                            this.getDetailById(this.id);
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

    getDetailById(id){
        console.log("schedule id "+id);
        let url = '/api_data_collection/?id=' + id;
        this.httpClient.toJson(this.httpClient.get(url)).subscribe(res => {
            if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        let data = res['data'];
                        console.log(res.data);
                        this.id = _.get(data, 'schedule_id');
                        this.selectedOsType = _.get(data, 'ostype_id').toString();
                        this.priority = _.get(data, 'priority');
                        this.deviceGroup = _.get(data, 'device_group_id').toString();
                        this.policyGroup = _.get(data, 'policy_group_id').toString();

                        let spt = _.get(data, 'start_period_time').split('@')[1];
                        let ept = _.get(data, 'end_period_time');
                        let sst = _.get(data, 'schedule_start_time');
                        let set = _.get(data, 'schedule_end_time');
                        this.startDateTime.setHours(parseInt(spt.split(':')[0]));
                        this.startDateTime.setMinutes(parseInt(spt.split(':')[1]));
                        this.endDateTime.setHours(parseInt(ept.split(':')[0]));
                        this.endDateTime.setMinutes(parseInt(ept.split(':')[1]));
                        this.startTime.setHours(parseInt(sst.split(':')[0]));
                        this.startTime.setMinutes(parseInt(sst.split(':')[1]));
                        this.endTime.setHours(parseInt(set.split(':')[0]));
                        this.endTime.setMinutes(parseInt(set.split(':')[1]));

                        let weeks: any = _.get(data, 'weeks');
                        for (let i=0; i< this.weekdays.length; i++){
                            if (this.weekdays[i] in weeks){
                                this.weekdays[i]['ifCheck'] = 'checked';
                            }
                        }

                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }

            // scheduleInfo['valid_period_type'] = this.validPeriodType.toString();
            // scheduleInfo['start_period_time'] = startPeriodTime;
            // scheduleInfo['end_period_time'] = endPeriodTime;
            // scheduleInfo['data_schedule_type'] = this.dataScheduleType.toString();
            // scheduleInfo['data_schedule_time'] = dataScheduleTime;

        });
        // console.log(result);
    }

    setInitSelect() {
        $('input[value="0"]').attr('checked','checked');
        this.dataScheduleType = 0;
        this.validPeriodType = 0;
        this.priority = 0;
    }

    changeOsType() {
        this.getGroups();
    }

    changeValidPeriodType(id: number){
        this.validPeriodType = id;
        if (id == 1){
            $('#validPeriod').show();
        } else {
            $('#validPeriod').hide();
        }
    }

    changeDataScheduleType(id: number){
        this.dataScheduleType = id;
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
        let startDate = $('input[name="startDate"]').val();
        let startPeriodTime = startDate+'@'
            +this.filledToTwoNumber(this.startDateTime.getHours())+':'
            +this.filledToTwoNumber(this.startDateTime.getMinutes());
        let endDate = $('input[name="endDate"]').val();
        let endPeriodTime = endDate+'@'
            +this.filledToTwoNumber(this.endDateTime.getHours())+':'
            +this.filledToTwoNumber(this.endDateTime.getMinutes());
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
        dataScheduleTime = dataScheduleTime.substring(0,dataScheduleTime.length-1)+'@'+dataScheduleStartTime+'-'+dataScheduleEndTime;

        // let url = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        if (this.doCheck()) {
            let scheduleInfo: any = {};
            let url = '/api_new_data_collection/';

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

            console.log(scheduleInfo);
            // return;
            if (this.id == -1){
                this.httpClient
                .toJson(this.httpClient.post(url, scheduleInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['data']) {
                            // let id = res['data']['coll_policy_id'];
                            // this.router.navigate(['/index/cliCPEdit'],
                            //     { queryParams: { 'id': id } });
                        }
                    } else {
                        // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                        //     this.uniqueFlg = false;
                        // } else {
                        //     alert(res['status']['message']);
                        // }
                    }
                });
            } else {
                scheduleInfo['schedule_id'] = this.id.toString();
                this.httpClient
                .toJson(this.httpClient.put(url, scheduleInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['data']) {
                            // let id = res['data']['coll_policy_id'];
                            // this.router.navigate(['/index/cliCPEdit'],
                            //     { queryParams: { 'id': id } });
                        }
                    } else {
                        // if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                        //     this.uniqueFlg = false;
                        // } else {
                        //     alert(res['status']['message']);
                        // }
                    }
                });
            }


        }


    }
    doCheck(){
        let flag: boolean = true;
        return flag;

    }

    delete() {
        let isDelete: boolean = confirm('delete?');
        if (isDelete){
            let url = '/api_data_collection/?id=' + this.id;
            this.httpClient
                .toJson(this.httpClient.delete(url))
                .subscribe(res => {
                    console.log('delete',res);
                });
        }
    }

}
