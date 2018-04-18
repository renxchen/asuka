/**
 * @author: Zizhuang Jiang
 * @contact: zizjiang@cisco.com
 * @file: groupEdit.component.ts
 * @time: 2018/03/08
 * @desc: edit device group
 */
import { Component, OnInit, AfterViewInit, OnDestroy } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { ModalComponent } from '../../../components/modal/modal.component';
import { Validator } from '../../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';

@Component({
    selector: 'group-edit',
    templateUrl: './groupEdit.component.html',
    styleUrls: ['.././device.component.less']
})
export class GroupEditComponent implements OnInit, AfterViewInit, OnDestroy {
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
    ostypeNotNull: Boolean = true;
    uniqueFlg: Boolean = true;
    groupFlg: Boolean = true;
    osFlg: Boolean = true;
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    constructor(
        private httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private bsModalRef: BsModalRef,
        private bsModalRefEdit: BsModalRef
    ) { }

    ngOnInit() {
        this.getOsType();
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (this.id) {
                this.getGroupInfo(this.id);
            }
        }, 0);
    }
    public getOsType() {
        /**
        * @brief get all of the ostype data
        * @author Zizhuang Jiang
        * @date 2018/03/18
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
    public getGroupInfo(id: any) {
        /**
        * @brief get device group info
        * param id: device group id
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.apiPrefix = '/v1';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get('/api_device_groups/?group_id=' + id))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data: any = _.get(res, 'data');
                let verify = _.get(res, 'verify_result');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (data && data.length > 0) {
                        this.name = _.get(data[0], 'name');
                        this.selectedOsType = _.get(_.get(data[0], 'ostype'), 'ostypeid');
                        this.desc = _.get(data[0], 'desc');
                    }
                    if (verify) {
                        this.groupFlg = _.get(verify, 'name');
                        this.osFlg = _.get(verify, 'ostype');
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
    public doCheck() {
        /**
        * @brief Verify the validity of the input information
        * @return true or false
        * @author Zizhuang Jiang
        * @date 2018/03/08
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
        if (this.nameNotNull && this.nameFlg && this.ostypeNotNull) {
            return true;
        } else {
            return false;
        }
    }
    public editGroup() {
        /**
        * @brief get and check the input infomation, then save
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.apiPrefix = '/v1';
        let url = '/api_device_groups/';
        let group: any = {};
        if (this.doCheck()) {
            group['group_id'] = parseInt(this.id, 0);
            group['name'] = this.name;
            group['ostype_id'] = this.selectedOsType;
            group['desc'] = this.desc;
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put(url, group))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let type = _.get(status, 'type');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        alert('保存しました。');
                        this.bsModalRefEdit.hide();
                        this.modalService.setDismissReason('true');
                    } else {
                        if (type && type === 'NAME_DUPLICATE') {
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
    public showAlertModal(modalMsg: any, closeMsg: any) {
        /**
        * @brief show modal dialog
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
    ngOnDestroy() {
        if (this.modalRef) {
            this.modalRef.hide();
        }
    }
}
