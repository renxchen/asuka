import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';

@Component({
    selector: 'snmp-login',
    templateUrl: 'snmpCPLogin.component.html',
    styleUrls: ['collectionPolicy.component.less']
})

export class SNMPCPLoginComponent implements OnInit, AfterViewInit {
    cPType: any;
    apiPrefix: string;
    name: any;
    osType: any;
    snmpOid: any;
    desc: any;
    selectedOsType: any;
    selectedRtnType: any;
    nameRegExp: string;
    oidRegExp: string;
    msgFlg: Boolean = true;
    nameFlg: boolean;
    oidFlg: boolean;
    nameNotNull;
    oidNotNull;
    osTypeFlg: boolean;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent) {
    }
    ngOnInit() {
        this.selectedOsType = 'null';
        this.selectedRtnType = '1';
        let cPTypeTmp: any = this.activedRoute.snapshot.queryParams['cPType'];
        if (cPTypeTmp && typeof (cPTypeTmp) !== 'undefined') {
            this.cPType = cPTypeTmp;
        }
        this.getOsType();
        this.selectedOsType = 'null';
        this.labelParentAlert();
    }
    ngAfterViewInit() {
    }
    public cPLogin() {
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        let cPLoginUrl = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        let cPEditUrl = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        if (this.doCheck() === true) {
            console.log('cpLogin');
            this.msgFlg = true;
            cPInfo['name'] = this.name;
            cPInfo['snmp_oid'] = this.snmpOid;
            cPInfo['value_type'] = this.selectedRtnType;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = this.selectedOsType;
            console.log(cPInfo);
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['data']) {
                            let id = res['data']['coll_policy_id'];
                            this.router.navigate(['/index/snmpCPEdit'],
                            { queryParams: {'id' : id }});
                        }
                        console.log('res', res);
                    } else {
                        if (['status']['message']) {
                            alert(res['status']['message']);
                        }
                    }
                });
        } else {
            this.msgFlg = false;
        }
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
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public doCheck() {
        this.nameRegExp = '[- 0-9a-zA-Z_]{1,256}';
        this.oidRegExp  = '[0-9]+?(\.[0-9]+?)+';
        let nameReg = new RegExp(this.nameRegExp);
        let oidReg = new RegExp(this.oidRegExp);
        console.log(oidReg.test('1.1.1'));
        if (this.name && this.name.trim()) {
            this.nameNotNull = true;
            if (nameReg.test(this.name) === true) {
                this.nameFlg = true;
            } else {
                this.nameFlg = false;
            }
        } else {
            this.nameNotNull = false;
            this.nameFlg = true;
        }
        if (this.snmpOid && this.snmpOid.trim()) {
            this.oidNotNull = true;
            if (oidReg.test(this.snmpOid) === true) {
                this.oidFlg = true;
            } else {
                this.oidFlg = false;
            }
        } else {
            this.oidNotNull = false;
            this.oidFlg = true;
        }
        if (this.selectedOsType !== 'null') {
            this.osTypeFlg = true;
        } else {
            this.osTypeFlg = false;
        }
        if (this.nameFlg === true
            && this.nameNotNull === true
            && this.oidFlg === true
            && this.oidNotNull === true
            && this.selectedOsType !== 'null'
            ) {
            return true;
        } else {
            return false;
        }
    }
    public labelParentAlert() {
        let _t = this;
        $('a[id ="labelParent"]').click(function () {
            let r = confirm('作業中の内容は破棄されます。よろしいですか？');
            if (r) {
                _t.router.navigate(['/index/cPView/']);
            }
        });
    }
}
