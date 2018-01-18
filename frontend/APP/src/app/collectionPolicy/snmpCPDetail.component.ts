import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import * as _ from 'lodash';
import { TranslateService } from '@ngx-translate/core';
@Component({
    selector: 'snmp-detail',
    templateUrl: 'snmpCPDetail.component.html',
    styleUrls: ['collectionPolicy.component.less']
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
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        let data = res['data'][0];
                        this.name = _.get(data, 'name');
                        this.desc = _.get(data, 'desc');
                        this.snmpOid = _.get(data, 'snmp_oid');
                        this.selectedRtnType = _.get(data, 'value_type');
                        this.selectedOsType = _.get(data, 'ostype');
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
        this.router.navigate(['/index/snmpCPEdit'], { queryParams: { 'id': this.cPId } });
    }
}
