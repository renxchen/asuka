import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import * as _ from 'lodash';
import { TranslateService } from '@ngx-translate/core';
@Component({
    selector: 'snmp-detail',
    templateUrl: 'snmpCPDetail.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})

export class SNMPCPDetailComponent implements OnInit, AfterViewInit {
    cPId: any;
    apiPrefix: any;
    name: any;
    osType: any;
    snmpOid: any;
    desc: any;
    selectedOsType: any;
    selectedRtnType: any;
    constructor(private translate: TranslateService,
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent, ) {
        // translate.setDefaultLang('en');
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            this.cPId = cPIdeTmp;
            this.getSNMPCPInfo(this.cPId);
        } else {
            this.router.navigate(['/index/']);
        }
    }
    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
    }
    public getSNMPCPInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy/?id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data = _.get(res, 'data');
                let snmpData: any = _.get(data, 'data');
                if (status && status['status'].toLowerCase() === 'true') {
                    if (snmpData && snmpData.length > 0) {
                        this.name = _.get(snmpData[0], 'name');
                        this.desc = _.get(snmpData[0], 'desc');
                        this.snmpOid = _.get(snmpData[0], 'snmp_oid');
                        this.selectedRtnType = _.get(snmpData[0], 'value_type');
                        this.selectedOsType = _.get(snmpData[0], 'ostype');
                    }
                } else {
                    if (msg) {
                        alert(msg);
                    }
                }
            });
    }
    public getOsType() {
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_ostype/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        this.osType = res['data'];
                        let osTypeTmp = _.clone(res['data']);
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public navSNMPEdit() {
        this.router.navigate(['/index/snmpcpedit'], { queryParams: { 'id': this.cPId } });
    }
}
