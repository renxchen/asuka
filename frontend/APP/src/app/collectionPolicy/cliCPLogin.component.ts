import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';

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
    msgFlg: Boolean = true;
    nameFlg;
    cmdFlg;
    nameNotNull;
    cmdNotNull;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent) { }
    ngOnInit() {
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
        let cPViewUrl = '/api_collection_policy/?policy_type=' + parseInt(this.cPType, 0);
        if (this.regExpCheck() === true) {
            console.log('cpLogin');
            this.msgFlg = true;
            cPInfo['name'] = this.name;
            cPInfo['cli_command'] = this.cliCommand;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = this.selectedOsType;
            console.log(cPInfo);
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        console.log('res', res);
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
    public regExpCheck() {
        this.regExp = '^[A-Za-z0-9]+$';
        let reg = new RegExp(this.regExp);
        if (this.name && this.name.trim()) {
            this.nameNotNull = true;
            if (reg.test(this.name) === true) {
                this.nameFlg = true;
            } else {
                this.nameFlg = false;
            }
        } else {
            this.nameNotNull = false;
            this.nameFlg = true;
        }
        if (this.cliCommand && this.cliCommand.trim()) {
            this.cmdNotNull = true;
            if (reg.test(this.cliCommand) === true) {
                this.cmdFlg = true;
            } else {
                this.cmdFlg = false;
            }
        } else {
            this.cmdNotNull = false;
            this.cmdFlg = true;
        }
        if (this.nameFlg === true
            && this.nameNotNull === true
            && this.cmdFlg === true
            && this.cmdNotNull === true
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
