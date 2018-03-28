import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { ModalComponent } from '../../../components/modal/modal.component';
import { Validator } from '../../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';

@Component({
    selector: 'group-login',
    templateUrl: './groupLogin.component.html',
    styleUrls: ['.././device.component.less']
})
export class GroupLoginComponent implements OnInit, AfterViewInit {
    id: any;
    apiPrefix: string;
    name: any;
    osType: any;
    desc: any;
    selectedOsType: any;
    nameFlg: Boolean = true;
    cmdFlg: Boolean = true;
    descFlg: Boolean = false;
    nameNotNull: Boolean = true;
    uniqueFlg: Boolean = true;
    modalMsg: any;
    closeMsg: any;
    constructor(
        private httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private bsModalRef: BsModalRef
    ) { }

    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
        setTimeout(() => {
            // if (this.id) {
            //     this.getCPInfo(this.cPId);
            // }
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
                        let osTypeTmp = _.clone(res['data']);
                        this.selectedOsType = res['data'][0]['ostypeid'].toString();
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public doCheck() {
        this.uniqueFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            // japanese is ok, need to check;
            this.nameFlg = Validator.fullWithoutSpecial(this.name);
        }
        if (this.nameNotNull && this.nameFlg && this.selectedOsType) {
            return true;
        } else {
            return false;
        }
    }
    public loginGroup() {
        this.apiPrefix = '/v1';
        let url = '/api_device_groups/';
        let group: any = {};
        if (this.doCheck()) {
            group['name'] = this.name;
            group['ostype_id'] = this.selectedOsType;
            group['desc'] = this.desc;
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(url, group))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    if (status && status['status'].toLowerCase() === 'true') {
                        alert('保存しました。');
                        this.bsModalRef.hide();
                        this.modalService.setDismissReason('true');
                    } else {
                        if (msg && msg === 'GROUPNAME_ALREADY_EXISTS') {
                            this.uniqueFlg = false;
                        } else {
                            alert(msg);
                        }
                    }
                });
        }
    }
}

