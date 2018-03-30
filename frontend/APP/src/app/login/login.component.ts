import { Component, OnInit, Input, AfterViewInit, ViewChild } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs/Rx';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../components/modal/modal.component';
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
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private translate: TranslateService,
        private modalService: BsModalService
    ) {
        translate.setDefaultLang('ja');
    }
    ngOnInit() {
        localStorage.setItem('requestFailed', '');
    }
    ngAfterViewInit() {
        let sessionTimeOut = localStorage.getItem('sessionTimeOut');
        if (sessionTimeOut) {
            if (sessionTimeOut) {
                this.modalMsg = sessionTimeOut;
                this.closeMsg = '閉じる';
                this.showAlertModal(this.modalMsg, this.closeMsg);
                localStorage.removeItem('sessionTimeOut');
            }
            localStorage.removeItem('sessionTimeOut');
        }
    }
    public login() {
        /**
        * @brief collect data from page and login stystem
        * @post jump to page "/index/deviceView" if login successly
        * @author Dan Lv
        * @date 2018/01/25
        */
        this.apiPrefix = '/v1';
        let loginUrl = '/login/';
        if (this.username
            && this.password
            && this.username.trim()
            && this.password.trim()) {
            this.httpClient.setUrl(this.apiPrefix);
            this
                .httpClient
                .toJson(this.httpClient.post(loginUrl, { 'username': this.username, 'password': this.password }))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        // change token to new_token
                        if (localStorage.getItem('sessionTimeOut')) {
                            localStorage.removeItem('sessionTimeOut');
                        }
                        if (data && _.get(data, 'username')) {
                            localStorage.setItem('token', _.get(res, 'new_token'));
                        }
                        this.router.navigate(['/index/']);
                    } else {
                        // alert(_.get(status, 'message'));
                        this.modalMsg = _.get(status, 'message');
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }

                });
        } else {
            let _t = this;
            _t.modalMsg = 'ユーザー名とパスワードを入力してください';
            _t.closeMsg = '閉じる';
            _t.showAlertModal(_t.modalMsg, this.closeMsg);
        }
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        /**
        * @brief show modal dialog
        * @author Dan Lv
        * @date 2018/01/25
        */
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}

