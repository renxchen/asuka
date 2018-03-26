
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
    regFlg: Boolean = true;
    ostypeMFlg: Boolean = true;
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
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (typeof (this.id) !== 'undefined') {
                this.getOstype(this.id);
            }
        }, 0);
    }
    public startCmdsInit() {
        this.countStart = 1;
        let firstStartCmd = {
            'id': this.countStart,
            'name': '',
            'startCmdFlg': false,
            'cmdRegFlg': true
        };
        this.startCmds.push(firstStartCmd);
    }
    public endCmdsInit() {
        this.countEnd = 1;
        let firstEndCmd = {
            'id': this.countStart,
            'name': '',
            'endCmdFlg': false,
            'cmdRegFlg': true
        };
        this.endCmds.push(firstEndCmd);
    }
    public logsInit() {
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
                        this.snmpTimeout = _.get(data[0], 'snmp_timeout');
                        this.telTimeout = _.get(data[0], 'telnet_timeout');
                    }
                    if (verify) {
                        this.ostypeMFlg = _.get(verify, 'name');
                    }
                } else {
                    alert(msg);
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
                'cmdRegFlg': true,
                'startCmdFlg': (i + 1) === len ? false : true
            };
            startCmds.push(startCmdInfo);
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
                'cmdRegFlg': true,
                'endCmdFlg': (i + 1) === len ? false : true
            };
            endCmds.push(endCmdInfo);
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
        return logs;
    }
    public addStartCmd() {
        let startCmdInfo = {
            'id': this.startCmds.length + 1,
            'name': '',
            'cmdRegFlg': true,
            'startCmdFlg': false
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
            'cmdRegFlg': true,
            'endCmdFlg': false
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
            'logFlg': false
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
    public ostypeCheck() {
        this.startRegFlg = this.multiStartCmdRegFomatter(this.startCmds);
        this.endRegFlg = this.multiEndCmdRegFomatter(this.endCmds);
        this.regFlg = this.multiLogsFomatter(this.logs);
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.fullWithoutSpecial(this.name);
        }
        this.telPromptNotNull = Validator.notNullCheck(this.telPrompt);
        if (this.telPromptNotNull) {
            this.telPromptFlg = Validator.regTest(this.telPrompt);
        }
        this.telTimeoutNotNull = Validator.notNullCheck(this.telTimeout);
        if (this.telTimeoutNotNull) {
            this.telTimeoutFlg = Validator.numRegCheck(this.telTimeout);
        }
        this.snmpTimeoutNotNull = Validator.notNullCheck(this.snmpTimeout);
        if (this.snmpTimeoutNotNull) {
            this.snmpTimeoutNotNull = Validator.numRegCheck(this.snmpTimeout);
        }
        if (this.nameNotNull && this.nameFlg
            && this.telTimeoutNotNull && this.telTimeoutFlg
            && this.snmpTimeoutNotNull && this.snmpTimeoutFlg
            && this.telPromptNotNull && this.telPromptFlg
            && this.regFlg) {
            return true;
        } else {
            return false;
        }
    }
    // startCommandReg Check
    public multiStartCmdRegFomatter(multiStartCmds: any) {
        let regFlgTmp = true;
        let uniqData: any = _.uniqBy(multiStartCmds, 'name');
        _.remove(uniqData, function (value) {
            return value['name'] === '';
        });
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (!Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].cmdRegFlg = false;
                    regFlgTmp = false;
                } else {
                    uniqData[i].cmdRegFlg = true;
                }
            }
            uniqData[len - 1]['startCmdFlg'] = false;
        } else {
            uniqData.push(this.startCmdsInit());
        }
        this.logs = uniqData;
        return regFlgTmp;
    }
    // endCommandReg Check
    public multiEndCmdRegFomatter(multiendCmds: any) {
        let regFlgTmp = true;
        let uniqData: any = _.uniqBy(multiendCmds, 'name');
        _.remove(uniqData, function (value) {
            return value['name'] === '';
        });
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (!Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].cmdRegFlg = false;
                    regFlgTmp = false;
                } else {
                    uniqData[i].cmdRegFlg = true;
                }
            }
            uniqData[len - 1]['endCmdFlg'] = false;
        } else {
            uniqData.push(this.endCmdsInit());
        }
        this.logs = uniqData;
        return regFlgTmp;
    }
    public multiLogsFomatter(multiLogs: any) {
        let regFlgTmp = true;
        let uniqData: any = _.uniqBy(multiLogs, 'name');
        _.remove(uniqData, function (value) {
            return value['name'] === '';
        });
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (!Validator.regTest(uniqData[i].name)) {
                    uniqData[i].logRegFlg = false;
                    regFlgTmp = false;
                } else {
                    uniqData[i].logRegFlg = true;
                }
            }
            uniqData[len - 1]['logFlg'] = false;
        } else {
            uniqData.push(this.logsInit());
        }
        this.logs = uniqData;
        return regFlgTmp;
    }
    public multiDataFomatter(multiData: any) {
        let uniqData: any = _.uniqBy(multiData, 'name');
        _.remove(uniqData, function (value) {
            return value['name'] === '';
        });
        // let dataString: String = '';
        // _.each(uniqData, function (value) {
        //     dataString = dataString + value['name'] + ',';
        // });
        return uniqData;
        // // 返回格式以逗号分隔“，”包含“，”这种情况是否考虑;只能是数字和机会记号（指的是什么）
        // if (dataString !== '') {
        //     alert(dataString);
        //     alert(dataString.substring(0, dataString.length - 1));
        //     console.log('dataString', typeof (dataString), dataString.substring(0, dataString.length - 1));
        //     return dataString.substring(0, dataString.length - 1);
        // } else {
        //     console.log('null', dataString);
        //     return dataString;
        // }
    }
    public ostypeLogin() {
        if (this.ostypeCheck()) {
            this.apiPrefix = '/v1';
            let ostypeInfo: any = {
                'ostypeid': this.id,
                'name': this.name,
                'desc': this.desc,
                'start_default_commands': this.multiDataFomatter(this.startCmds),
                'end_default_commands': this.multiDataFomatter(this.endCmds),
                'log_fail_judges': this.multiDataFomatter(this.logs),
                'telnet_prompt': this.telPrompt,
                'snmp_timeout': this.snmpTimeout,
                'telnet_timeout': this.telTimeout,
                'status': this.status
            };
            // console.log(ostypeInfo);
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
                            alert(msg);
                        }
                    }
                });
        }

    }
}



