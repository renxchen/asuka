/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: snmpCPLogin.component.ts
* @time: 2017/01/25
* @desc: create snmp collection policy
*/
import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
import { Validator } from '../../../components/validation/validation';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'snmp-login',
    templateUrl: './snmpCPLogin.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
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
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    nameNotNull: Boolean = true;
    ostypeNotNull: Boolean = true;
    nameFlg: Boolean = true;
    oidNotNull: Boolean = true;
    oidFlg: Boolean = true;
    uniqueFlg: Boolean = true;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService
    ) {
    }
    ngOnInit() {
        let cPTypeTmp: any = this.activedRoute.snapshot.queryParams['cPType'];
        if (cPTypeTmp && typeof (cPTypeTmp) !== 'undefined') {
            this.cPType = cPTypeTmp;
        } else {
            this.router.navigate(['/index/']);
        }
        this.selectedRtnType = '1';
        this.getOsType();
    }
    ngAfterViewInit() {
    }
    public cPLogin() {
        /**
        * @brief get and check the input infomation, then save
        * @post navigate to collection policy summary page
        * @author Dan Lv
        * @date 2018/01/25
        */
        let _t = this;
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        let cPLoginUrl = '/api_collection_policy/';
        if (this.doCheck()) {
            cPInfo['name'] = this.name;
            cPInfo['snmp_oid'] = this.snmpOid;
            cPInfo['value_type'] = this.selectedRtnType;
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
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        if (data && data['data']) {
                            this.modalMsg = '保存しました。';
                            this.closeMsg = '一覧へ戻る';
                            this.showAlertModal(this.modalMsg, this.closeMsg);
                            $('#modalButton').on('click', function () {
                                _t.router.navigate(['/index/cpview/'], { queryParams: { 'cptype': 1 } });
                            });
                        }
                    } else {
                        // CP_NAME_DUPLICATE
                        if (msg && msg === 'Collection policy name is exist in system.') {
                            this.uniqueFlg = false;
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
        * @brief get ostype data
        * @author Dan Lv
        * @date 2018/01/25
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
    public doCheck() {
        /**
        * @brief Verify the validity of the input information
        * @return true or false
        * @author Dan Lv
        * @date 2018/01/25
        */
        this.uniqueFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.halfWithoutSpecial(this.name);
        }
        if (this.selectedOsType) {
            this.ostypeNotNull = true;
        } else {
            this.ostypeNotNull = false;
        }
        this.oidNotNull = Validator.notNullCheck(this.snmpOid);
        if (this.oidNotNull) {
            this.oidFlg = Validator.oidRegCheck(this.snmpOid);
        }
        if (this.nameNotNull && this.nameFlg
            && this.oidNotNull && this.oidFlg
            && this.ostypeNotNull) {
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
