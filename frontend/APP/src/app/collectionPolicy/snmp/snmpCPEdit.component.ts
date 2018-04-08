/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: snmpCPEdit.component.ts
* @time: 2017/01/25
* @desc: edit snmp collection policy
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
    selector: 'snmp-edit',
    templateUrl: './snmpCPEdit.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})

export class SNMPCPEditComponent implements OnInit, AfterViewInit {
    cPId: any;
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
    nameFlg: Boolean = true;
    nameMFlg: Boolean = true;
    ostypeNotNull: Boolean = true;
    oidNotNull: Boolean = true;
    oidFlg: Boolean = true;
    uniqueFlg: Boolean = true;
    osFlg: Boolean = true;
    snmpFlg: Boolean = true;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService) {
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            this.cPId = cPIdeTmp;
            this.getSNMPCPInfo(this.cPId);
        } else {
            this.router.navigate(['/index/cpview'], { queryParams: { 'cptype': '1' } });
        }
    }
    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
    }
    public getSNMPCPInfo(id: any) {
        /**
        * @brief get snmp collection policy data and assignment variable
        * @author Dan Lv
        * @date 2018/01/25
        */
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy/?id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data = _.get(res, 'data');
                let verify = _.get(data, 'verify_result');
                let snmpData: any = _.get(data, 'data');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (snmpData && snmpData.length > 0) {
                        this.name = _.get(snmpData[0], 'name');
                        this.desc = _.get(snmpData[0], 'desc');
                        this.snmpOid = _.get(snmpData[0], 'snmp_oid');
                        this.selectedRtnType = _.get(snmpData[0], 'value_type');
                        this.selectedOsType = _.get(snmpData[0], 'ostype');
                    }
                    if (verify) {
                        this.nameMFlg = _.get(verify, 'coll_policy_name');
                        this.osFlg = _.get(verify, 'ostype');
                        this.snmpFlg = _.get(verify, 'snmp_oid');
                    }
                } else {
                    if (msg) {
                        alert(msg);
                    }
                }
            });
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
                let status = _.get(res, 'status');
                let data: any = _.get(res, 'data');
                let msg = _.get(status, 'message');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (data && data.length > 0) {
                        this.osType = data;
                    }
                } else {
                    // if (res['status'] && res['status']['message']) {
                    //     alert(res['status']['message']);
                    // }
                    this.modalMsg = msg;
                    this.closeMsg = '閉じる';
                    this.showAlertModal(this.modalMsg, this.closeMsg);
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
        this.oidNotNull = Validator.notNullCheck(this.snmpOid);
        if (this.oidNotNull) {
            this.oidFlg = Validator.oidRegCheck(this.snmpOid);
        }
        if (this.selectedOsType) {
            this.ostypeNotNull = true;
        } else {
            this.ostypeNotNull = false;
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
            cPInfo['ostype'] = this.selectedOsType.toString();
            cPInfo['id'] = this.cPId;
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        // if (res['data']) {
                        //     let id = res['data']['coll_policy_id'];
                        //     this.router.navigate(['/index/snmpcpedit'],
                        //     { queryParams: {'id' : id }});
                        // }
                        this.modalMsg = '保存しました。';
                        this.closeMsg = '一覧へ戻る';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                        $('#modalButton').on('click', function () {
                            _t.router.navigate(['/index/cpview/'], { queryParams: { 'cptype': 1 } });
                        });
                    } else {
                        // CP_NAME_DUPLICATE
                        if (msg === 'Collection policy name is exist in system.') {
                            this.uniqueFlg = false;
                        } else {
                            // alert(msg);
                            this.modalMsg = msg;
                            this.closeMsg = '閉じる';
                            this.showAlertModal(this.modalMsg, this.closeMsg);
                        }
                    }
                });
        }
    }
}
