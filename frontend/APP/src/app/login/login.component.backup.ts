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
    ) {}
    ngOnInit() {
        localStorage.setItem('requestFailed', '');
    }
    ngAfterViewInit() {
        let sessionTimeOut = localStorage.getItem('sessionTimeOut');
        if (sessionTimeOut) {
            // 添加alert
            console.log('sessionTimeOut', sessionTimeOut);
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
            .toJson(this.httpClient.post(loginUrl, {'username': this.username, 'password': this.password}))
            .subscribe(res => {
                console.log('res', res);
                console.log('status', res['meta']['status']);
                if (res['meta']['status'] && res['meta']['status'] === true) {
                    localStorage.setItem('token', res['data']['token']);
                    localStorage.setItem('username', res['data']['username']);
                    if (localStorage.getItem('sessionTimeOut')) {
                        localStorage.removeItem('sessionTimeOut');
                    }
                    this.router.navigate(['/index']);
                } else {
                        // alert(res['meta']['info']);
                        alert(res['meta']['message']);
                }
            });
        }
    }
    // ngOnDestroy(): {
    // }
}



