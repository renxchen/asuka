import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { ModalComponent } from '../../../components/modal/modal.component';
import { Validator } from '../../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';

@Component({
    selector: 'ostype-login',
    templateUrl: './ostypeLogin.component.html',
    styleUrls: ['.././device.component.less']
})
export class OstypeLoginComponent implements OnInit, AfterViewInit {
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
    telPromptFlg: Boolean = true;
    telPromptNotNull: Boolean = true;
    telTimeoutFlg: Boolean = true;
    telTimeoutNotNull: Boolean = true;
    snmpTimeoutFlg: Boolean = true;
    snmpTimeoutNotNull: Boolean = true;

    constructor(
        private httpClient: HttpClientComponent,
        private modalService: BsModalService,
        private bsModalRef: BsModalRef,
    ) { }
    ngOnInit() {
        this.startCmdsInit();
        this.endCmdsInit();
        this.logsInit();
    }
    ngAfterViewInit() {
    }
    public startCmdsInit() {
        this.startCmds = [];
        this.countStart = 1;
        let firstStartCmd = {
            'id': this.countStart,
            'name': '',
            'startCmdFlg': false,
            'startRegFlg': true,
        };
        this.startCmds.push(firstStartCmd);
        return firstStartCmd;
    }
    public endCmdsInit() {
        this.endCmds = [];
        this.countEnd = 1;
        let firstEndCmd = {
            'id': this.countEnd,
            'name': '',
            'endCmdFlg': false,
            'endRegFlg': true,
        };
        this.endCmds.push(firstEndCmd);
        return firstEndCmd;
    }
    public logsInit() {
        this.logs = [];
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
    public addStartCmd() {
        let startCmdInfo = {
            'id': this.startCmds.length + 1,
            'name': '',
            'startCmdFlg': false,
            'startRegFlg': true,
        };
        let id: any = startCmdInfo['id'];
        let penult = id - 1;
        if (this.startCmds[penult - 1]['id'] === penult) {
            this.startCmds[penult - 1]['startCmdFlg'] = true;
        }
        this.startCmds.push(_.cloneDeep(startCmdInfo));
    }
    public delStartCmd(startCmd: any) {
        for (let i = 0; i < this.startCmds.length; i++) {
            if (this.startCmds.length > 1 && this.startCmds[i]['id'] === startCmd['id']) {
                this.startCmds.splice(i, 1);
            }
        }
        for (let i = 0; i < this.startCmds.length; i++) {
            let num: number = i + 1;
            this.startCmds[i]['id'] = num;
            if (i === this.startCmds.length - 1) {
                this.startCmds[i]['startCmdFlg'] = false;
            }
        }
    }
    public addEndCmd() {
        let endCmdInfo = {
            'id': this.endCmds.length + 1,
            'name': '',
            'endCmdFlg': false,
            'endRegFlg': true,
        };
        let id: any = endCmdInfo['id'];
        let penult = id - 1;
        if (this.endCmds[penult - 1]['id'] === penult) {
            this.endCmds[penult - 1]['endCmdFlg'] = true;
        }
        this.endCmds.push(_.cloneDeep(endCmdInfo));
    }
    public delEndCmd(endCmd: any) {
        for (let i = 0; i < this.endCmds.length; i++) {
            if (this.endCmds.length > 1 && this.endCmds[i]['id'] === endCmd['id']) {
                this.endCmds.splice(i, 1);
            }
        }
        for (let i = 0; i < this.endCmds.length; i++) {
            let num: number = i + 1;
            this.endCmds[i]['id'] = num;
            if (i === this.endCmds.length - 1) {
                this.endCmds[i]['endCmdFlg'] = false;
            }
        }
    }
    public addLogCmd() {
        let logInfo = {
            'id': this.logs.length + 1,
            'name': '',
            'logFlg': false,
            'logRegFlg': true
        };
        let id: any = logInfo['id'];
        let penult = id - 1;
        if (this.logs[penult - 1]['id'] === penult) {
            this.logs[penult - 1]['logFlg'] = true;
        }
        this.logs.push(_.cloneDeep(logInfo));
    }
    public delLogCmd(log: any) {
        for (let i = 0; i < this.logs.length; i++) {
            if (this.logs.length > 1 && this.logs[i]['id'] === log['id']) {
                this.logs.splice(i, 1);
            }
        }
        for (let i = 0; i < this.logs.length; i++) {
            let num: number = i + 1;
            this.logs[i]['id'] = num;
            if (i === this.logs.length - 1) {
                this.logs[i]['logFlg'] = false;
            }
        }
    }
    trackByIndex(index: number, value: number) {
        return index;
    }
    public ostypeCheck() {
        let starts = _.cloneDeep(this.startCmds);
        let ends = _.cloneDeep(this.endCmds);
        let logs = _.cloneDeep(this.logs);
        this.startRegFlg = this.multiStartCmdRegFomatter(starts);
        this.endRegFlg = this.multiEndCmdRegFomatter(ends);
        this.logRegFlg = this.multiLogsFomatter(logs);
        this.uniqueFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.fullWithoutSpecial(this.name);
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
    public multiLogsFomatter(multiLogs: any) {
        let regFlgTmp = true;
        _.each(multiLogs, function (value) {
            return value['name'] = value['name'].trim();
        });
        _.remove(multiLogs, function (value) {
            return value['name'] === '';
        });
        let uniqData: any = [];
        uniqData = _.uniqBy(multiLogs, 'name');
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].logRegFlg = true;
                } else {
                    regFlgTmp = false;
                    uniqData[i].logRegFlg = false;
                }
            }
            uniqData[len - 1]['logFlg'] = false;
        } else {
            uniqData.push(this.logsInit());
        }
        this.logs = _.cloneDeep(uniqData);
        return regFlgTmp;
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
        uniqData = _.uniqBy(multiStartCmds, 'name');
        console.log('fina', uniqData);
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].startRegFlg = true;
                } else {
                    uniqData[i].startRegFlg = false;
                    regFlgTmp = false;
                }
            }
            uniqData[len - 1]['startCmdFlg'] = false;
        } else {
            uniqData.push(this.startCmdsInit());
        }
        this.startCmds = _.cloneDeep(uniqData);
        console.log('start1', this.startCmds);
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
        uniqData = _.uniqBy(multiendCmds, 'name');
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
        this.endCmds = _.cloneDeep(uniqData);
        return regFlgTmp;
    }
    //
    public multiDataFomatter(multiData: any) {
        let uniqData: any = _.uniqBy(multiData, 'name');
        _.remove(uniqData, function (value) {
            return value['name'] === '';
        });
        return uniqData;
    }
    public ostypeLogin() {
        if (this.ostypeCheck()) {
            this.apiPrefix = '/v1';
            let ostypeInfo: any = {
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
                .toJson(this.httpClient.post('/api_device_ostype/', ostypeInfo))
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
                            alert(msg);
                        }
                    }
                });
        }

    }
}
