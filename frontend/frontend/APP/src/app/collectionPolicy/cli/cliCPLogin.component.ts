/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: cliCPLogin.component.ts
* @time: 2018/03/14
* @desc: create a cli collection policy
*/
import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Validator } from '../../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
declare var $: any;
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
    ostypeNotNull: Boolean = true;
    uniqueFlg: Boolean = true;
    modalRef: BsModalRef;
    closeMsg: any;
    modalMsg: any;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService) { }
    ngOnInit() {
        let cPTypeTmp: any = this.activedRoute.snapshot.queryParams['cPType'];
        if (cPTypeTmp && typeof (cPTypeTmp) !== 'undefined') {
            this.cPType = cPTypeTmp;
        } else {
            this.router.navigate(['/index/']);
        }
        this.getOsType();
    }
    ngAfterViewInit() {
        this.getOsType();
    }
    public cPLogin() {
        /**
       * @brief get and check the input infomation, then save
       * @post navigate to collection policy edit page
       * @author Dan Lv
       * @date 2018/03/14
       */
        let _t = this;
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        let cPLoginUrl = '/api_collection_policy/';
        let cPEditUrl = '/api_collection_policy/';
        if (_t.doCheck()) {
            cPInfo['name'] = _t.name;
            cPInfo['cli_command'] = _t.cliCommand;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = _t.selectedOsType;
            cPInfo['policy_type'] = _t.cPType;
            _t.httpClient.setUrl(_t.apiPrefix);
            _t.httpClient
                .toJson(_t.httpClient.post(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        if (data && data['data']) {
                            let id = _.get(data['data'], 'coll_policy_id');
                            _t.modalMsg = '保存しました。';
                            _t.closeMsg = 'ツリー構成へ';
                            _t.showAlertModal(_t.modalMsg, _t.closeMsg);
                            $('#modalButton').on('click', function () {
                                _t.router.navigate(['/index/clicpedit'],
                                    { queryParams: { 'id': id } });
                            });
                        }
                    } else {
                        // CP_NAME_DUPLICATE
                        if (msg && msg === 'Collection policy name is exist in system.') {
                            _t.uniqueFlg = false;
                        } else {
                            if (msg) {
                                this.modalMsg = msg;
                                this.closeMsg = '閉じる';
                                this.showAlertModal(this.modalMsg, this.closeMsg);
                            }
                        }
                    }
                });
        }
    }
    public getOsType() {
        /**
        * @brief get all of the ostype data
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_ostype/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        this.osType = res['data'];
                        let osTypeTmp = _.clone(res['data']);
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        this.modalMsg = res['status']['message'];
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }
    public doCheck(): boolean {
        /**
       * @brief Verify the validity of the input information
       * @return true or false
       * @author Dan Lv
       * @date 2018/03/14
       */
        this.uniqueFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.halfWithoutSpecial(this.name);
        }
        this.cmdNotNull = Validator.notNullCheck(this.cliCommand);
        if (this.cmdNotNull) {
            this.cmdFlg = Validator.halfWidthReg(this.cliCommand);
        }
        if (this.selectedOsType) {
            this.ostypeNotNull = true;
        } else {
            this.ostypeNotNull = false;
        }
        if (this.nameNotNull && this.nameFlg
            && this.cmdNotNull && this.cmdFlg
            && this.ostypeNotNull) {
            return true;
        } else {
            return false;
        }
    }

    public showAlertModal(modalMsg: any, closeMsg: any) {
        /**
        * @brief show modal dialog
        * @author Dan Lv
        * @date 2018/01/23
        */
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
