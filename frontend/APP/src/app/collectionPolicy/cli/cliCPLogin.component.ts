import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Validator } from '../../../components/validation/validation';
import * as _ from 'lodash';

@Component({
    selector: 'cli-login',
    templateUrl: './cliCPLogin.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})

export class CLICPLoginComponent implements OnInit, AfterViewInit {
    cPType: any;
    apiPrefix: string;
    name: any;
    osType: any;
    cliCommand: any;
    desc: any;
    selectedOsType: any;
    nameFlg: Boolean = true;
    cmdFlg: Boolean = true;
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
        } else {
            this.router.navigate(['/index/index']);
        }
        this.getOsType();
        // this.labelParentAlert();
    }
    ngAfterViewInit() {
        this.getOsType();
    }
    public cPLogin() {
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        let cPLoginUrl = '/api_collection_policy/';
        let cPEditUrl = '/api_collection_policy/';
        if (this.doCheck()) {
            cPInfo['name'] = this.name;
            cPInfo['cli_command'] = this.cliCommand;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = this.selectedOsType;
            cPInfo['policy_type'] = this.cPType;
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data && data['data']) {
                            let id = _.get(data['data'], 'coll_policy_id');
                            this.router.navigate(['/index/clicpedit'],
                                { queryParams: { 'id': id } });
                        }
                    } else {
                        if (msg && msg === 'CP_NAME_DUPLICATE') {
                            this.uniqueFlg = false;
                        } else {
                            alert(msg);
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
                    if (res['data'] && res['data'].length > 0) {
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
            this.nameFlg = Validator.halfWithoutSpecial(this.name);
        }
        this.cmdNotNull = Validator.notNullCheck(this.cliCommand);
        if (this.cmdNotNull) {
            this.cmdFlg = Validator.halfWidthReg(this.cliCommand);
        }
        if (this.nameNotNull && this.nameFlg
            && this.cmdNotNull && this.cmdFlg) {
            return true;
        } else {
            return false;
        }
    }
    // public labelParentAlert() {
    //     let _t = this;
    //     $('a[id ="labelParent"]').click(function () {
    //         let r = confirm('作業中の内容は破棄されます。よろしいですか？');
    //         if (r) {
    //             _t.router.navigate(['/index/cpview/']);
    //         }
    //     });
    // }
}
