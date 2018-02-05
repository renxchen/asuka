import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { TranslateService } from '@ngx-translate/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
import { Validator } from '../../../components/validation/validation';
import * as _ from 'lodash';
@Component({
    selector: 'snmp-edit',
    templateUrl: 'snmpCPEdit.component.html',
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
    descFlg: Boolean = false;
    oidNotNull: Boolean = true;
    oidFlg: Boolean = true;
    uniqueFlg: Boolean = true;
    constructor(
        private translate: TranslateService,
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService) {
        // translate.setDefaultLang('en');
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            this.cPId = cPIdeTmp;
            this.getSNMPCPInfo(this.cPId);
        } else {
            this.router.navigate(['/index/']);
        }
    }
    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
    }
    public getSNMPCPInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy/?id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        let data = res['data'][0];
                        this.name = _.get(data, 'name');
                        this.desc = _.get(data, 'desc');
                        this.snmpOid = _.get(data, 'snmp_oid');
                        this.selectedRtnType = _.get(data, 'value_type');
                        this.selectedOsType = _.get(data, 'ostype');
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
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
    public doCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.descFlg = Validator.includeChinese(this.desc);
        this.oidNotNull = Validator.notNullCheck(this.snmpOid);
        if (this.oidNotNull) {
            this.oidFlg = Validator.oidRegCheck(this.snmpOid);
        }
        if (this.nameNotNull && this.nameFlg
            && this.oidNotNull && this.oidFlg
            && !this.descFlg) {
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
                _t.router.navigate(['/index/cpview/']);
            }
        });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
    public cPLogin() {
        let _t = this;
        let cPInfo: any = {};
        this.apiPrefix = '/v1';
        let cPLoginUrl = '/api_collection_policy/?id=' + this.cPId;
        if (this.doCheck()) {
            cPInfo['name'] = this.name;
            cPInfo['snmp_oid'] = this.snmpOid;
            cPInfo['value_type'] = this.selectedRtnType;
            cPInfo['desc'] = this.desc;
            cPInfo['ostype'] = this.selectedOsType.toString();
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(cPLoginUrl, cPInfo))
                .subscribe(res => {
                    if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                        // if (res['data']) {
                        //     let id = res['data']['coll_policy_id'];
                        //     this.router.navigate(['/index/snmpcpedit'],
                        //     { queryParams: {'id' : id }});
                        // }
                        this.modalMsg = '保存しました。';
                        this.closeMsg = '一覧へ戻る';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                        $('#modalButton').on('click', function () {
                            _t.router.navigate(['/index/']);
                        });
                    } else {
                        if (res['status']['message'] === 'CP_NAME_DUPLICATE') {
                            this.uniqueFlg = false;
                        }
                    }
                });
        }
    }
}
