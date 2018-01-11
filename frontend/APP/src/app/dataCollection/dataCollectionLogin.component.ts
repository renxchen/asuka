import { Component, OnInit, AfterViewInit, enableProdMode} from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
// import * as _ from 'lodash';

enableProdMode();

@Component({
    selector: 'dc-login',
    templateUrl: 'dataCollectionLogin.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DataCollectionLoginComponent implements OnInit, AfterViewInit {
    title: string;
    id: number = -1;
    // minDate = new Date(2017, 5, 10);
    maxDate = new Date(2018, 10, 15);
    bsValue: Date = new Date();

    isTimeMeridian: boolean = false;
    startTime: Date = new Date(2018, 1, 1, 0, 0);
    endTime: Date = new Date(2018, 1, 1, 23, 59);
    startDateTime: Date = new Date(2018, 1, 1, 0, 0);
    endDateTime: Date = new Date(2018, 1, 1, 23, 59);
    // bsRangeValue: any = [new Date(2017, 7, 4), new Date(2017, 7, 20)];

    selectedOsType: string;
    osType: any = [{id: 0, name: 'os type 1'}, {id:1, name: 'os type 2'}];
    priority: any;
    priorities: any = [{id: 0, value: '標準'}, {id:1, value: '高'}];
    deviceGroup: any;
    deviceGroups: any = [];
    policyGroup: any;
    policyGroups:any = [];
    validPeriodTypes: any = [{id:0, value:'期間なし'}, {id:1, value: '期間あり'}];
    dataScheduleTypes: any = [{id:0, value:'常に取得'}, {id:1, value: '取得停止'}, {id:2, value: '周期取得'}];
    weekdays: any = [
        {id: 1, value: '月', ifCheck: 'checked'},
        {id: 2, value: '火', ifCheck: 'checked'},
        {id: 3, value: '水', ifCheck: 'checked'},
        {id: 4, value: '木', ifCheck: 'checked'},
        {id: 5, value: '金', ifCheck: 'checked'},
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
        this.getOsTypes();
        this.deviceGroups = [{id: 0, name: 'device group 1'}, {id:1, name: 'device group 2'}];
        this.policyGroups = [{id: 0, name: 'cpg 1'}, {id:1, name: 'cpg 2'}];

    }

    ngAfterViewInit() {
        setTimeout(() => {
           if(this.id == -1){
                this.setInitSelect();
                $('button.btn-danger').hide();
                $('#validPeriod').hide();
                $('#dataSchedule').hide();
            } else {
                //set init value for this id
               // $('button.btn-primary').attr('disabled','disabled');
            }
        },0);
    }

    getOsTypes() {

    }

    setInitSelect() {
        $('input[value="0"]').attr('checked','checked');
    }

    changeOsType() {
        let _p = $('#osType').val();
        // send this os type id to API and get groups information
        let _this = this;
        _this.deviceGroups = [{id: 0, name: 'device group 1'}, {id:1, name: 'device group 2'}];
        _this.policyGroups = [{id: 0, name: 'cpg 1'}, {id:1, name: 'cpg 2'}];
    }

    changeValidPeriodType(id: number){
        if (id == 1){
            $('#validPeriod').show();
        } else {
            $('#validPeriod').hide();
        }
    }

    changeDataScheduleType(id: number){
        if (id == 2){
            $('#dataSchedule').show();
        } else {
            $('#dataSchedule').hide();
        }
    }

    save() {
        let startDate = $('input[name="startDate"]').val();
        // console.log(startDate);
        let endDate = $('input[name="endDate"]').val();
        // console.log(endDate);
        let timeFormat = this.startTime.getHours();
        console.log(timeFormat);
        let timeFormat2 = this.startTime.getMinutes();
        console.log(timeFormat2);
        if (this.id == -1){
            // save as new
        } else {
            // save
        }
    }

    delete() {
        let isDelete: boolean = confirm('delete?');
        if (isDelete){
            let _id = this.id;
            console.log(_id);
        }

    }

}
