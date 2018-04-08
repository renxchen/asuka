
import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { ModalComponent } from '../../../components/modal/modal.component';
import { Validator } from '../../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';

@Component({
    selector: 'ostype-edit',
    templateUrl: './ostypeEdit.component.html',
    styleUrls: ['.././device.component.less']
})

export class OstypeEditComponent implements OnInit, AfterViewInit {
    id: any;
    apiPrefix: any;
    name: any;
    desc: any;
    countStart: number;
    countEnd: number;
    countLog: number;
    startCmds: any = [];
    endCmds: any = [];
    logs: any = [];
    telPrompt: any;
    telTimeout: any;
    snmpTimeout: any;
    status: any = 1;
    nameFlg: Boolean = true;
    nameNotNull: Boolean = true;
    uniqueFlg: Boolean = true;
    startRegFlg: Boolean = true;
    endRegFlg: Boolean = true;
    logRegFlg: Boolean = true;
    ostypeMFlg: Boolean = true;
    telPromptFlg: Boolean = true;
    telPromptNotNull: Boolean = true;
    telTimeoutFlg: Boolean = true;
    telTimeoutNotNull: Boolean = true;
    snmpTimeoutFlg: Boolean = true;
    snmpTimeoutNotNull: Boolean = true;
    startTrashBinFlg: Boolean = true;
    endTrashBinFlg: Boolean = true;
    logTrashBinFlg: Boolean = true;
    modalRef: BsModalRef;
    modalMsg: any;
    closeMsg: any;
    constructor(
        private httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private bsModalRef: BsModalRef,
    ) { }
    ngOnInit() {
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (typeof (this.id) !== 'undefined') {
                this.getOstype(this.id);
            }
        }, 0);
    }
    public startCmdsInit() {
        this.startTrashBinFlg = true;
        this.countStart = 1;
        let firstStartCmd = {
            'id': this.countStart,
            'name': '',
            'startCmdFlg': false,
            'startRegFlg': true
        };
        this.startCmds.push(firstStartCmd);
        return firstStartCmd;
    }
    public endCmdsInit() {
        this.endTrashBinFlg = true;
        this.countEnd = 1;
        let firstEndCmd = {
            'id': this.countEnd,
            'name': '',
            'endCmdFlg': false,
            'endRegFlg': true
        };
        this.endCmds.push(firstEndCmd);
        return firstEndCmd;
    }
    public logsInit() {
        this.logTrashBinFlg = true;
        this.countLog = 1;
        let firstLog = {
            'id': this.countLog,
            'name': '',
            'logFlg': false,
            'logRegFlg': true
        };
        this.logs.push(firstLog);
        return firstLog;
    }
    public getOstype(id: any) {
        /**
        * @brief get ostype info
        * param id: ostype id
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        this.apiPrefix = '/v1';
        let url = '/api_device_ostype/?id=' + this.id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                let data: any = _.get(res, 'data');
                let verify: any = _.get(res, 'verify_result');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    if (data) {
                        this.name = _.get(data[0], 'name');
                        this.desc = _.get(data[0], 'desc');
                        this.telPrompt = _.get(data[0], 'telnet_prompt');
                        let startCmdsTmp: any = _.get(data[0], 'start_default_commands');
                        let endCmdsTmp: any = _.get(data[0], 'end_default_commands');
                        let logsTmp: any = _.get(data[0], 'log_fail_judges');
                        if (typeof (startCmdsTmp) !== 'string') {
                            this.startCmdsInit();
                        } else {
                            this.startCmds = this.startCmdsToList(startCmdsTmp);
                        }
                        if (typeof (endCmdsTmp) !== 'string') {
                            this.endCmdsInit();
                        } else {
                            this.endCmds = this.endCmdsToList(endCmdsTmp);
                        }
                        if (typeof (logsTmp) !== 'string') {
                            this.logsInit();
                        } else {
                            this.logs = this.logsToList(logsTmp);
                        }
                        this.snmpTimeout = _.get(data[0], 'snmp_timeout').toString();
                        this.telTimeout = _.get(data[0], 'telnet_timeout').toString();
                    }
                    if (verify) {
                        this.ostypeMFlg = _.get(verify, 'name');
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

    public startCmdsToList(data: any) {
        let startCmds: any = [];
        let dataList: any = data.split('，');
        let len = dataList.length;
        for (let i = 0; i < dataList.length; i++) {
            let startCmdInfo: any = {};
            startCmdInfo = {
                'id': i + 1,
                'name': dataList[i],
                'startRegFlg': true,
                'startCmdFlg': (i + 1) === len ? false : true
            };
            startCmds.push(startCmdInfo);
        }
        if (startCmds.length === 1) {
            this.startTrashBinFlg = true;
        } else {
            this.startTrashBinFlg = false;
        }
        return startCmds;
    }
    public endCmdsToList(data: any) {
        let endCmds: any = [];
        let dataList: any = data.split('，');
        let len = dataList.length;
        for (let i = 0; i < dataList.length; i++) {
            let endCmdInfo: any = {};
            endCmdInfo = {
                'id': i + 1,
                'name': dataList[i],
                'endRegFlg': true,
                'endCmdFlg': (i + 1) === len ? false : true
            };
            endCmds.push(endCmdInfo);
        }
        if (endCmds.length === 1) {
            this.endTrashBinFlg = true;
        } else {
            this.endTrashBinFlg = false;
        }
        return endCmds;
    }
    public logsToList(data: any) {
        let logs: any = [];
        let dataList: any = data.split('，');
        let len = dataList.length;
        for (let i = 0; i < dataList.length; i++) {
            let logInfo: any = {};
            logInfo = {
                'id': i + 1,
                'name': dataList[i],
                'logRegFlg': true,
                'logFlg': (i + 1) === len ? false : true
            };
            logs.push(logInfo);
        }
        if (logs.length === 1) {
            this.logTrashBinFlg = true;
        } else {
            this.logTrashBinFlg = false;
        }
        return logs;
    }
    public addStartCmd() {
        this.startTrashBinFlg = false;
        let addStartTmp: any = [];
        addStartTmp = _.cloneDeep(this.startCmds);
        let startCmdInfo = {
            'id': addStartTmp.length + 1,
            'name': '',
            'startCmdFlg': false,
            'startRegFlg': true,
        };
        let id: any = startCmdInfo['id'];
        let penult = id - 1;
        if (addStartTmp[penult - 1]['id'] === penult) {
            addStartTmp[penult - 1]['startCmdFlg'] = true;
        }
        addStartTmp.push(startCmdInfo);
        this.startCmds = addStartTmp;
    }
    public delStartCmd(startCmd: any) {
        let delStartTmp: any = [];
        delStartTmp = _.cloneDeep(this.startCmds);
        for (let i = 0; i < delStartTmp.length; i++) {
            if (delStartTmp.length > 1 && delStartTmp[i]['id'] === startCmd['id']) {
                delStartTmp.splice(i, 1);
            }
        }
        for (let i = 0; i < delStartTmp.length; i++) {
            let num: number = i + 1;
            delStartTmp[i]['id'] = num;
            if (i === delStartTmp.length - 1) {
                delStartTmp[i]['startCmdFlg'] = false;
                if (delStartTmp.length === 1) {
                    this.startTrashBinFlg = true;
                } else {
                    this.startTrashBinFlg = false;
                }
            }
        }
        this.startCmds = delStartTmp;
    }
    public addEndCmd() {
        this.endTrashBinFlg = false;
        let addEndTmp: any = [];
        addEndTmp = _.cloneDeep(this.endCmds);
        let endCmdInfo = {
            'id': addEndTmp.length + 1,
            'name': '',
            'endCmdFlg': false,
            'endRegFlg': true,
        };
        let id: any = endCmdInfo['id'];
        let penult = id - 1;
        if (addEndTmp[penult - 1]['id'] === penult) {
            addEndTmp[penult - 1]['endCmdFlg'] = true;
        }
        addEndTmp.push(endCmdInfo);
        this.endCmds = addEndTmp;
    }
    public delEndCmd(endCmd: any) {
        let delEndTmp: any = [];
        delEndTmp = _.cloneDeep(this.endCmds);
        for (let i = 0; i < delEndTmp.length; i++) {
            if (delEndTmp.length > 1 && delEndTmp[i]['id'] === endCmd['id']) {
                delEndTmp.splice(i, 1);
            }
        }
        for (let i = 0; i < delEndTmp.length; i++) {
            let num: number = i + 1;
            delEndTmp[i]['id'] = num;
            if (i === delEndTmp.length - 1) {
                delEndTmp[i]['endCmdFlg'] = false;
                if (delEndTmp.length === 1) {
                    this.endTrashBinFlg = true;
                } else {
                    this.endTrashBinFlg = false;
                }
            }
        }
        this.endCmds = delEndTmp;
    }
    public addLogCmd() {
        this.logTrashBinFlg = false;
        let addlogTmp: any = [];
        addlogTmp = _.cloneDeep(this.logs);
        let logInfo = {
            'id': addlogTmp.length + 1,
            'name': '',
            'logFlg': false,
            'logRegFlg': true
        };
        let id: any = logInfo['id'];
        let penult = id - 1;
        if (addlogTmp[penult - 1]['id'] === penult) {
            addlogTmp[penult - 1]['logFlg'] = true;
        }
        addlogTmp.push(logInfo);
        this.logs = addlogTmp;
    }
    public delLogCmd(log: any) {
        let dellogTmp: any = [];
        dellogTmp = _.cloneDeep(this.logs);
        for (let i = 0; i < dellogTmp.length; i++) {
            if (dellogTmp.length > 1 && dellogTmp[i]['id'] === log['id']) {
                dellogTmp.splice(i, 1);
            }
        }
        for (let i = 0; i < dellogTmp.length; i++) {
            let num: number = i + 1;
            dellogTmp[i]['id'] = num;
            if (i === dellogTmp.length - 1) {
                dellogTmp[i]['logFlg'] = false;
                if (dellogTmp.length === 1) {
                    this.logTrashBinFlg = true;
                } else {
                    this.logTrashBinFlg = false;
                }
            }
        }
        this.logs = dellogTmp;
    }
    public ostypeCheck() {
        /**
        * @brief Verify the validity of the input information
        * @return true or false
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        let starts = _.cloneDeep(this.startCmds);
        let ends = _.cloneDeep(this.endCmds);
        let logs = _.cloneDeep(this.logs);
        this.startRegFlg = this.multiStartCmdRegFomatter(starts);
        this.endRegFlg = this.multiEndCmdRegFomatter(ends);
        this.logRegFlg = this.multiLogsFomatter(logs);
        this.uniqueFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.fullWithoutSpecial(this.name) && this.name.length < 31;
        }
        this.telPromptNotNull = Validator.notNullCheck(this.telPrompt);
        if (this.telPromptNotNull) {
            this.telPromptFlg = Validator.halfWidthReg(this.telPrompt);
        }
        this.telTimeoutNotNull = Validator.notNullCheck(this.telTimeout);
        if (this.telTimeoutNotNull) {
            this.telTimeoutFlg = Validator.numRegCheck(this.telTimeout);
        }
        this.snmpTimeoutNotNull = Validator.notNullCheck(this.snmpTimeout);
        if (this.snmpTimeoutNotNull) {
            this.snmpTimeoutFlg = Validator.numRegCheck(this.snmpTimeout);
        }
        if (this.nameNotNull && this.nameFlg
            && this.telTimeoutNotNull && this.telTimeoutFlg
            && this.snmpTimeoutNotNull && this.snmpTimeoutFlg
            && this.telPromptNotNull && this.telPromptFlg
            && this.logRegFlg && this.startRegFlg && this.endRegFlg) {
            return true;
        } else {
            return false;
        }
    }
    // startCommandReg Check
    public multiStartCmdRegFomatter(multiStartCmds: any) {
        let regFlgTmp = true;
        _.each(multiStartCmds, function (value) {
            return value['name'] = value['name'].trim();
        });
        _.remove(multiStartCmds, function (value) {
            return value['name'] === '';
        });
        let uniqData: any = [];
        // uniqData = _.uniqBy(multiStartCmds, 'name');
        uniqData = _.cloneDeep(multiStartCmds);
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].startRegFlg = true;
                } else {
                    regFlgTmp = false;
                    uniqData[i].startRegFlg = false;
                }
            }
            uniqData[len - 1]['startCmdFlg'] = false;
        } else {
            uniqData.push(this.startCmdsInit());
        }
        if (uniqData.length === 1) {
            this.startTrashBinFlg = true;
        } else {
            this.startTrashBinFlg = false;
        }
        this.startCmds = _.cloneDeep(uniqData);
        return regFlgTmp;
    }
    // endCommandReg Check
    public multiEndCmdRegFomatter(multiendCmds: any) {
        let regFlgTmp = true;
        _.each(multiendCmds, function (value) {
            return value['name'] = value['name'].trim();
        });
        _.remove(multiendCmds, function (value) {
            return value['name'] === '';
        });
        let uniqData: any = [];
        // uniqData = _.uniqBy(multiendCmds, 'name');
        uniqData = _.cloneDeep(multiendCmds);
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].endRegFlg = true;
                } else {
                    regFlgTmp = false;
                    uniqData[i].endRegFlg = false;
                }
            }
            uniqData[len - 1]['endCmdFlg'] = false;
        } else {
            uniqData.push(this.endCmdsInit());
        }
        if (uniqData.length === 1) {
            this.endTrashBinFlg = true;
        } else {
            this.endTrashBinFlg = false;
        }
        this.endCmds = _.cloneDeep(uniqData);
        return regFlgTmp;
    }
    public multiLogsFomatter(multiLogs: any) {
        let regFlgTmp = true;
        _.each(multiLogs, function (value) {
            return value['name'] = value['name'].trim();
        });
        _.remove(multiLogs, function (value) {
            return value['name'] === '';
        });
        let uniqData: any = [];
        // uniqData = _.uniqBy(multiLogs, 'name');
        uniqData = _.cloneDeep(multiLogs);
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].logRegFlg = true;
                } else {
                    uniqData[i].logRegFlg = false;
                    regFlgTmp = false;
                }
            }
            uniqData[len - 1]['logFlg'] = false;
        } else {
            uniqData.push(this.logsInit());
        }
        if (uniqData.length === 1) {
            this.logTrashBinFlg = true;
        } else {
            this.logTrashBinFlg = false;
        }
        this.logs = _.cloneDeep(uniqData);
        return regFlgTmp;
    }
    public multiDataFomatter(multiData: any) {
        let uniqData: any = _.uniqBy(multiData, 'name');
        _.remove(uniqData, function (value) {
            return value['name'] === '';
        });
        return uniqData;
    }
    public ostypeLogin() {
        /**
        * @brief get and check the input infomation, then save
        * @author Zizhuang Jiang
        * @date 2018/03/08
        */
        if (this.ostypeCheck()) {
            this.apiPrefix = '/v1';
            let ostypeInfo: any = {
                'ostypeid': parseInt(this.id, 0),
                'name': this.name,
                'desc': this.desc,
                'start_default_commands': this.startCmds,
                'end_default_commands': this.endCmds,
                'log_fail_judges': this.logs,
                'telnet_prompt': this.telPrompt,
                'snmp_timeout': this.snmpTimeout,
                'telnet_timeout': this.telTimeout,
                'status': this.status
            };
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.put('/api_device_ostype/', ostypeInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        alert('保存しました。');
                        this.bsModalRef.hide();
                        this.modalService.setDismissReason('true');
                    } else {
                        if (msg && msg === 'NAME_IS_EXISTENCE') {
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
}



