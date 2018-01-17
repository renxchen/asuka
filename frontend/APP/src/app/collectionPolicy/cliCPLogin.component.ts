import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Validator } from '../../components/validation/validation';
import * as _ from 'lodash';

@Component({
    selector: 'cli-login',
    templateUrl: 'cliCPLogin.component.html',
    styleUrls: ['collectionPolicy.component.less']
})

export class CLICPLoginComponent implements OnInit, AfterViewInit {
    cPType: any;
    apiPrefix: string;
    name: any;
    osType: any;
    cliCommand: any;
    desc: any;
    selectedOsType: any;
    regExp: string;
    nameFlg: Boolean = true;
    cmdFlg: Boolean = true;
    descFlg: Boolean = false;
    nameNotNull: Boolean = true;
    cmdNotNull: Boolean = true;
    uniqueFlg: Boolean = true;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent) { }
    ngOnInit() {
        // this.selectedOsType = 'null';
        let cPTypeTmp: any = this.activedRoute.snapshot.queryParams['cPType'];
        if (cPTypeTmp && typeof (cPTypeTmp) !== 'undefined') {
            this.cPType = cPTypeTmp;
        }
        this.getOsType();
        this.labelParentAlert();
    }
    ngAfterViewInit() {
    }
    public cPLogin() {
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        let cPLoginUrl = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        let cPEditUrl = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        if (this.doCheck()) {
            cPInfo['name'] = this.name;
            cPInfo['cli_command'] = this.cliCommand;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = this.selectedOsType;
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['data']) {
                            let id = res['data']['coll_policy_id'];
                            this.router.navigate(['/index/cliCPEdit'],
                                { queryParams: { 'id': id } });
                        }
                    } else {
                        if (res['status'] && res['status']['message'] === 'CP_NAME_DUPLICATE') {
                            this.uniqueFlg = false;
                        } else {
                            alert(res['status']['message']);
                        }
                    }
                });
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
                        let osTypeTmp = _.clone(res['data']);
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public doCheck(): boolean {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.descFlg = Validator.includeChinese(this.desc);
        this.cmdNotNull = Validator.notNullCheck(this.cliCommand);
        if (this.cmdNotNull) {
            this.cmdFlg = Validator.noCommsymbol(this.cliCommand);
        }
        if (this.nameNotNull && this.nameFlg
            && this.cmdNotNull && this.cmdFlg
            && !this.descFlg) {
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
