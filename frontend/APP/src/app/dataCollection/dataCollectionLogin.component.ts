import { Component, OnInit, AfterViewInit, } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';

@Component({
    selector: 'dc-login',
    templateUrl: 'dataCollectionLogin.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DataCollectionLoginComponent implements OnInit, AfterViewInit {
    title: string;
    id: number = -1;
    selectedOsType: string;
    osType: any = [];
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
        {id: 2, value: '火', ifCheck: ''},
        {id: 3, value: '水', ifCheck: ''},
        {id: 4, value: '木', ifCheck: ''},
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

    }

    ngAfterViewInit() {
        setTimeout(() => {
           if(this.id == -1){
                this.setInitSelect();
                $('#validPeriod').hide();
                $('#dataSchedule').hide();
            } else {
                //set init value for this id
            }
        },0);
    }

    getOsTypes() {

    }

    setInitSelect() {
        $('input[value="0"]').attr('checked',true);
    }

    changeOsType() {
        let _p = $('#osType').val();
        // send this os type id to API and get groups information
        let _this = this;
        _this.deviceGroups = [];
        _this.policyGroups = [];
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
        if (this.id == -1){
            // save as new
        } else {
            // save
        }
    }

}
