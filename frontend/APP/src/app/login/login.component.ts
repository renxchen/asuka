import { Component, OnInit, Input, AfterViewInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/observable';
import { HttpClientComponent } from '../../components/utils/httpClient';
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
    ) { }
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
                    if (res['status']) {
                        let status = res['status'];
                        if (status['status'] && status['status'].toLowerCase() === 'true') {
                            if (localStorage.getItem('sessionTimeOut')) {
                                localStorage.removeItem('sessionTimeOut');
                            }
                            if (res['username'] && res['token']) {
                                localStorage.setItem('token', res['token']);
                                localStorage.setItem('username', res['username']);
                            }
                            this.router.navigate(['/index/']);
                        } else {
                            alert(res['status']['message']);
                        }
                    }
                });
        }
    }
}

