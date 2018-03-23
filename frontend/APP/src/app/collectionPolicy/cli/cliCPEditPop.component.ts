import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { ModalComponent } from '../../../components/modal/modal.component';
import { CollectionPolicyService } from '.././collectionPolicy.service';
import { Validator } from '../../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';
@Component({
    selector: 'cliCP-pop',
    templateUrl: './cliCPEditPop.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})

export class CLICPEditPopComponent implements OnInit, AfterViewInit {
    cPId: any;
    cPName: any;
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
    ostypeFlg: Boolean = true;
    cliCmdFlg: Boolean = true;
    modalMsg: any;
    closeMsg: any;
    constructor(
        private httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private modalRef: BsModalRef,
        private service: CollectionPolicyService
    ) { }
    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (this.cPId) {
                this.getCPInfo(this.cPId);
            }
        }, 0);
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
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public getCPInfo(id: any) {
        this.apiPrefix = '/v1';
        // backend provide
        let url = '/api_collection_policy_edit_page/?coll_policy_id=' + this.cPId;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data = _.get(res, 'data');
                let verify: any = _.get(data, 'verify_result');
                let policy: any = _.get(data, 'policy_detail');
                if (status && status['status'].toLowerCase() === 'true') {
                    if (policy) {
                        this.name = _.get(policy, 'name');
                        this.desc = _.get(policy, 'desc');
                        this.cliCommand = _.get(policy, 'cli_command');
                        this.selectedOsType = _.get(policy, 'ostype');
                    }
                    if (verify) {
                        this.ostypeFlg = _.get(verify, 'ostype');
                        this.cliCmdFlg = _.get(verify, 'cli_command');
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
    public cPEdit() {
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        // backend provide
        let cPEditUrl = '/api_collection_policy_edit_page/';
        if (this.doCheck()) {
            cPInfo['coll_policy_id'] = this.cPId;
            cPInfo['coll_policy_name'] = this.name;
            cPInfo['command'] = this.cliCommand;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = this.selectedOsType;
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(cPEditUrl, cPInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        if (data) {
                            this.cPName = _.get(data, 'name');
                            alert('保存しました。');
                            this.modalRef.hide();
                            this.modalService.setDismissReason(this.cPName);
                        }
                        // this.modalMsg = '保存しました。';
                        // this.closeMsg = '一覧へ戻る';
                        // this.showAlertModal(this.modalMsg, this.closeMsg);
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
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
