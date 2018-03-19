import { Component, OnInit, AfterViewInit, OnDestroy, Input } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Validator } from '../../../components/validation/validation';
import { CollectionPolicyService } from '.././collectionPolicy.service';
import { Subject } from 'rxjs/Subject';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';
@Component({
    selector: 'cli-data',
    templateUrl: './cliData.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
})
export class CLIDataComponent implements OnInit, AfterViewInit {
    data: any;
    apiPrefix: any;
    cpId: any;
    info: any;
    actionType: any;
    ruleType: any;
    ruleId: any;
    name: any;
    desc: any;
    markString: any;
    keyStr: any;
    selSplitChar: any;
    xOffset: any;
    yOffset: any;
    extractKey: any;
    lineNums: any;
    selectedRtnType: any;
    otherChar: any;
    // Flg
    nameNotNull: Boolean = true;
    nameFlg: Boolean = true;
    uniqueFlg: Boolean = true;
    mrkStrNotNull: Boolean = true;
    keyStrNotNull: Boolean = true;
    keyStrFlg: Boolean = true;
    keyUnqFlg: Boolean = true;
    commandNotNull: Boolean = true;
    commandFlg: Boolean = true;
    commandUnqFlg: Boolean = true;
    lineNumsNotNull: Boolean = true;
    lineNumsFlg: Boolean = true;
    lineNumsUnqFlg: Boolean = true;
    xOffsetNotNull: Boolean = true;
    xOffsetNotNullB: Boolean = true;
    xOffsetFlg: Boolean = true;
    xOffsetFlgB: Boolean = true;
    yOffsetNotNull: Boolean = true;
    yOffsetFlg: Boolean = true;
    extKeyNotNull: Boolean = true;
    delBtn: Boolean = false;
    otherCharFlg: Boolean = true;
    processFlg: Boolean = false;
    lockFlg: Boolean = false;
    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef,
        private modalService: BsModalService,
        public service: CollectionPolicyService) {
    }
    ngOnInit() {
        this.selSplitChar = '4';
        this.xOffset = 0;
        this.yOffset = 0;
        this.selectedRtnType = '1';
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (typeof (this.info) !== 'undefined') {
                // console.log('this', this.info);
                this.cpId = this.info['cPId'];
                // console.log('cpid', this.info);
                this.ruleType = this.info['ruleType'];
                this.actionType = this.info['actionType'];
                if (this.actionType === 'edit') {
                    this.ruleId = this.info['ruleId'];
                    this.getDataRule(this.cpId, this.ruleId);
                }
            }
        }, 0);
    }
    public commInfo(cpId: any, ruleId: any) {
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree_rule/?coll_policy_id=' + cpId + '&rule_id=' + ruleId;
        this.httpClient.setUrl(this.apiPrefix);
        return this.httpClient.toJson(this.httpClient.get(url));
    }
    public getDataRule(cpId: any, ruleId: any) {
        this.commInfo(cpId, ruleId).subscribe(res => {
            this.processFlg = _.get(res, 'is_processing');
            this.lockFlg = _.get(res, 'is_locked');
            let isUsed = _.get(res, 'rule_is_used');
            if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                if (res['data']) {
                    let data = res['data'];
                    this.name = _.get(data, 'name');
                    this.desc = _.get(data, 'desc');
                    this.markString = _.get(data, 'mark_string');
                    this.keyStr = _.get(data, 'key_str');
                    this.selSplitChar = _.get(data, 'split_char');
                    this.xOffset = _.get(data, 'x_offset');
                    this.yOffset = _.get(data, 'y_offset');
                    // this.lineNums = _.get(data, 'line_nums');
                    this.extractKey = _.get(data, 'extract_key');
                    this.selectedRtnType = _.get(data, 'value_type');
                    this.otherChar = _.get(data, 'other_char');
                }
            }
            if (isUsed || this.info['delFlg']) {
                console.log(33);
                this.delBtn = false;
            } else {
                this.delBtn = true;
            }
        });
    }
    public dataRuleACheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        this.xOffsetNotNull = Validator.notNullCheck(this.xOffset.toString());
        if (this.xOffsetNotNull) {
            this.xOffsetFlg = Validator.xOffsetCheck(this.xOffset.toString());
        }
        if (this.selSplitChar === '3') {
            if (this.otherChar) {
                this.otherCharFlg = true;
            } else {
                this.otherChar = false;
            }
        }
        // this.yOffsetFlg = Number.isInteger(this.yOffset);
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull && this.xOffsetNotNull
            && this.xOffsetFlg && this.otherCharFlg) {
            return true;
        } else {
            return false;
        }
    }
    public dataRuleBCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        this.xOffsetNotNullB = typeof (this.xOffset) === 'number' ? true : false;
        if (this.xOffsetNotNullB) {
            this.xOffsetFlgB = Validator.offsetCheck(this.xOffset);
        }
        this.yOffsetNotNull = typeof (this.yOffset) === 'number' ? true : false;
        if (this.yOffsetNotNull) {
            this.yOffsetFlg = Validator.offsetCheck(this.yOffset);
        }
        if (this.selSplitChar === '3') {
            if (this.otherChar) {
                this.otherCharFlg = true;
            } else {
                this.otherCharFlg = false;
            }
        }
        if (this.nameNotNull && this.nameFlg && this.yOffsetNotNull
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull && this.xOffsetNotNullB
            && this.xOffsetFlgB && this.otherCharFlg
            && this.yOffsetNotNull && this.yOffsetFlg) {
            return true;
        } else {
            return false;
        }
    }
    public dataRuleCCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        if (this.nameNotNull && this.nameFlg && this.keyStrNotNull
            && this.keyStrFlg && this.mrkStrNotNull) {
            return true;
        } else {
            return false;
        }
    }
    // backend feedback:data valid error in saving the rule
    public dataRuleDCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        if (this.nameNotNull && this.nameFlg && this.keyStrNotNull
            && this.keyStrFlg) {
            return true;
        } else {
            return false;
        }
    }
    public dataRuleECheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        if (this.nameNotNull && this.nameFlg && this.keyStrNotNull
            && this.keyStrFlg) {
            return true;
        } else {
            return false;
        }
    }
    public dataRulePrepare() {
        let sendRuleInfo: any = {};
        let rule_info: any = {};
        if (this.ruleType === 'data_rule_1') {
            if (this.dataRuleACheck()) {
                // console.log('b1');
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['split_char'] = this.selSplitChar;
                rule_info['x_offset'] = this.xOffset;
                rule_info['extract_key'] = this.extractKey;
                rule_info['value_type'] = this.selectedRtnType;
                rule_info['other_char'] = this.otherChar;
                // console.log('rule_info', rule_info);
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_2') {
            // console.log(12);
            if (this.dataRuleBCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['split_char'] = this.selSplitChar;
                rule_info['x_offset'] = this.xOffset;
                rule_info['y_offset'] = this.yOffset;
                rule_info['extract_key'] = this.extractKey;
                rule_info['value_type'] = this.selectedRtnType;
                rule_info['other_char'] = this.otherChar;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_3') {
            if (this.dataRuleCCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['value_type'] = this.selectedRtnType;
                sendRuleInfo['rule_info'] = rule_info;
                // console.log('da3', sendRuleInfo);
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_4') {
            if (this.dataRuleDCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['key_str'] = this.keyStr;
                rule_info['value_type'] = this.selectedRtnType;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_9') {
            if (this.dataRuleDCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['key_str'] = this.keyStr;
                rule_info['value_type'] = this.selectedRtnType;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        }
        return '';
    }
    public saveRule() {
        this.apiPrefix = '/v1';
        let id = this.ruleId;
        let editUrl = '/api_policy_tree_rule/?rule_id=' + id;
        let createUrl = '/api_policy_tree_rule/';
        this.httpClient.setUrl(this.apiPrefix);
        let sendInfo = this.dataRulePrepare();
        // console.log('sendInfo', sendInfo);
        if (this.actionType === 'create' && sendInfo !== '') {
            this.httpClient
                .toJson(this.httpClient.post(createUrl, sendInfo))
                .subscribe(res => {
                    // console.log(res);
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    let errMsg = _.get(res, 'verify_error_msg');

                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data) {
                            let dataInfo: any = {};
                            dataInfo['dataTree'] = _.get(data, 'data_rule_tree_json');
                            alert('保存しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(dataInfo);
                        }
                    } else {
                        if (errMsg) {
                            if (!_.get(errMsg, 'rule_name')) {
                                this.uniqueFlg = false;
                            } else {
                                this.uniqueFlg = true;
                            }
                            if (!_.get(errMsg, 'key_str_name')) {
                                this.keyUnqFlg = false;
                            } else {
                                this.keyUnqFlg = true;
                            }
                        } else {
                            alert(msg);
                        }
                    }
                });

        } else if (this.actionType === 'edit' && sendInfo !== '') {
            this.httpClient
                .toJson(this.httpClient.put(editUrl, sendInfo))
                .subscribe(res => {
                    // console.log(res);
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    let errMsg = _.get(res, 'verify_error_msg');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data) {
                            let dataInfo: any = {};
                            dataInfo['dataTree'] = _.get(data, 'data_rule_tree_json');
                            dataInfo['ruleName'] = _.get(data, 'new_name');
                            alert('保存しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(dataInfo);
                        }
                    } else {
                        if (errMsg) {
                            if (!_.get(errMsg, 'rule_name')) {
                                this.uniqueFlg = false;
                            } else {
                                this.uniqueFlg = true;
                            }
                            if (!_.get(errMsg, 'key_str_name')) {
                                this.keyUnqFlg = false;
                            } else {
                                this.keyUnqFlg = true;
                            }
                        } else {
                            alert(msg);
                        }
                    }
                });
        }
    }
    public deleteRule() {
        let alt = confirm('このルールを削除します。よろしいですか？');
        this.apiPrefix = '/v1';
        let delUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId + '&coll_policy_id=' + this.cpId;
        if (alt) {
            this.httpClient
                .toJson(this.httpClient.delete(delUrl)).subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data) {
                            let dataTree: any = {};
                            dataTree['dataTree'] = _.get(data, 'data_rule_tree_json');
                            alert('削除しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(dataTree);
                        }
                    } else {
                        alert(msg);
                    }
                });
        }
    }
}
