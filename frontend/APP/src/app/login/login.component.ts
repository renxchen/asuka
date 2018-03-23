import { Component, OnInit, Input, AfterViewInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Rx';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { TranslateService } from '@ngx-translate/core';
import * as _ from 'lodash';
@Component({
    selector: 'login',
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.less'],
})
export class LoginComponent implements OnInit, AfterViewInit {
    username: string;
    password: string;
    apiPrefix: string;
    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private translate: TranslateService) {
        translate.setDefaultLang('ja');
    }
    ngOnInit() {
        localStorage.setItem('requestFailed', '');
    }
    ngAfterViewInit() {
        let sessionTimeOut = localStorage.getItem('sessionTimeOut');
        if (sessionTimeOut) {
            localStorage.removeItem('sessionTimeOut');
        }
    }
    public login() {
        this.apiPrefix = '/v1';
        let loginUrl = '/login/';
        if (this.username && this.password && this.username.trim() && this.password.trim()) {
            this.httpClient.setUrl(this.apiPrefix);
            this
                .httpClient
                .toJson(this.httpClient.post(loginUrl, { 'username': this.username, 'password': this.password }))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (localStorage.getItem('sessionTimeOut')) {
                            localStorage.removeItem('sessionTimeOut');
                        }
                        if (data && _.get(data, 'username')) {
                            localStorage.setItem('token', _.get(res, 'new_token'));
                            // localStorage.setItem('username', _.get(data, 'username'));
                        }
                        this.router.navigate(['/index/']);
                    } else {
                        alert(_.get(status, 'message'));
                    }

                });
        }
    }
}

