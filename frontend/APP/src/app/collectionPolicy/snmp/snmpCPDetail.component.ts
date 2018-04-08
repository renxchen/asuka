/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: snmpCPDetail.component.ts
* @time: 2017/01/25
* @desc: display snmp collection policy in detail
*/
import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalComponent } from '../../../components/modal/modal.component';
import * as _ from 'lodash';
@Component({
    selector: 'snmp-detail',
    templateUrl: './snmpCPDetail.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})

export class SNMPCPDetailComponent implements OnInit, AfterViewInit {
    cPId: any;
    apiPrefix: any;
    name: any;
    osType: any;
    snmpOid: any;
    desc: any;
    selectedOsType: any;
    selectedRtnType: any;
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService ) {
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
        * @brief get snmp info
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
                let snmpData: any = _.get(data, 'data');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (snmpData && snmpData.length > 0) {
                        this.name = _.get(snmpData[0], 'name');
                        this.desc = _.get(snmpData[0], 'desc');
                        this.snmpOid = _.get(snmpData[0], 'snmp_oid');
                        this.selectedRtnType = _.get(snmpData[0], 'value_type');
                        this.selectedOsType = _.get(snmpData[0], 'ostype');
                    }
                } else {
                    if (msg) {
                        this.modalMsg = msg;
                        this.closeMsg = '閉じる';
                        this.showAlertModal(this.modalMsg, this.closeMsg);
                    }
                }
            });
    }
    public getOsType() {
        /**
        * @brief get ostype info
        * @author Dan Lv
        * @date 2018/01/25
        */
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_ostype/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data']) {
                        this.osType = res['data'];
                        let osTypeTmp = _.clone(res['data']);
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
    public navSNMPEdit() {
        /**
        * @brief jump to the current snmp edit page
        * @author Dan Lv
        * @date 2018/01/25
        */
        this.router.navigate(['/index/snmpcpedit'], { queryParams: { 'id': this.cPId } });
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
