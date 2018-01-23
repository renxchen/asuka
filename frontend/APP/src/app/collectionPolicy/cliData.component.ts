import { Component, OnInit, AfterViewInit, OnDestroy, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Validator } from '../../components/validation/validation';
import { CollectionPolicyService } from './collectionPolicy.service';
import { Subject } from 'rxjs/Subject';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';
@Component({
    selector: 'cli-data',
    templateUrl: './cliData.component.html',
    styleUrls: ['./collectionPolicy.component.less']
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
    command: any;
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
    xOffsetFlg: Boolean = true;
    yOffsetFlg: Boolean = true;
    extKeyNotNull: Boolean = true;
    delBtn: Boolean = false;
    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef,
        private modalService: BsModalService,
        public service: CollectionPolicyService) {
    }
    ngOnInit() {
        this.selSplitChar = '0';
        this.xOffset = 0;
        this.yOffset = 0;
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
                    if (this.info['delFlg']) {
                    } else {
                        this.delBtn = true;
                    }
                    this.ruleId = this.info['ruleId'];
                    this.getDataRule(this.ruleId);
                }
            }
        }, 0);
    }
    public commInfo(ruleId: any) {
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree_rule/?rule_id=' + ruleId;
        this.httpClient.setUrl(this.apiPrefix);
        return this.httpClient.toJson(this.httpClient.get(url));
    }
    public getDataRule(ruleId: any) {
        this.commInfo(ruleId).subscribe(res => {
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
                    this.lineNums = _.get(data, 'line_nums');
                    // 后台定义改字段
                    this.command = _.get(data, 'command');
                }
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
        this.xOffsetFlg = Number.isInteger(this.xOffset);
        // this.yOffsetFlg = Number.isInteger(this.yOffset);
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull && this.xOffsetFlg) {
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
        this.xOffsetFlg = Number.isInteger(this.xOffset);
        this.yOffsetFlg = Number.isInteger(this.yOffset);
        if (this.nameNotNull && this.nameFlg && this.yOffsetFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull && this.xOffsetFlg) {
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
        this.mrkStrNotNull = Validator.notNullCheck(this.extractKey);
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
        this.keyStrNotNull = Validator.notNullCheck(this.lineNums);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.lineNums);
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
        this.keyStrNotNull = Validator.notNullCheck(this.command);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.command);
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
                // console.log(rule_info);
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_3') {
            if (this.dataRuleCCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.extractKey;
                rule_info['key_str'] = this.keyStr;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_4') {
            if (this.dataRuleDCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['line_nums'] = this.lineNums;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'data_rule_5') {
            if (this.dataRuleDCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                // 后台未给出该字段
                rule_info['command'] = this.command;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        }
        return '';
    }
    public saveRule() {
        // this.apiPrefix = '/v1';
        // let id = this.cpId;
        // let editUrl = '/api_policy_tree_rule/?rule_id=' + id;
        // let createUrl = '/api_policy_tree_rule/';
        // this.httpClient.setUrl(this.apiPrefix);
        // let sendInfo = this.dataRulePrepare();
        // // console.log('sendInfo', sendInfo);
        // if (this.actionType === 'create' && sendInfo !== '') {
        //     this.httpClient
        //         .toJson(this.httpClient.post(createUrl, sendInfo))
        //         .subscribe(res => {
        //             // console.log(res);
        //             let status = _.get(res, 'status');
        //             let msg = _.get(status, 'message');
        //             let data = _.get(status, 'data');
        //             if (status && status['status'].toLowerCase() === 'true') {
        //                 // if (data) {
        //                 //     let dataTree: any = {};
        //                 //     dataTree = _.get(data, 'data_rule_tree_json');
        //                 //     alert('削除しました。');
        //                 //     this.bsModalRef.hide();
        //                 //     this.modalService.setDismissReason(dataTree);
        //                 // }
        //                 if (res['data_rule_tree_json']) {
        //                     let datarule = res['data_rule_tree_json'];
        //                     alert('保存しました。');
        //                     this.bsModalRef.hide();
        //                     this.modalService.setDismissReason(datarule);
        //                 }
        //             } else {
        //                 if (msg && msg === 'the same name rule is existence') {
        //                     this.uniqueFlg = false;
        //                 } else if (msg && msg === 'key_str duplicatoin') {
        //                     this.keyUnqFlg = false;
        //                 } else {
        //                     alert(msg);
        //                 }
        //             }
        //         });

        // } else if (this.actionType === 'edit' && sendInfo !== '') {
        //     this.httpClient
        //         .toJson(this.httpClient.put(editUrl, this.dataRulePrepare()))
        //         .subscribe(res => {
        //             // console.log(res);
        //             let status = _.get(res, 'status');
        //             let msg = _.get(status, 'message');
        //             let data = _.get(status, 'data');
        //             if (status && status['status'].toLowerCase() === 'true') {
        //                 // if (data) {
        //                 //     let dataTree: any = {};
        //                 //     dataTree = _.get(data, 'data_rule_tree_json');
        //                 //     alert('編集しました。');
        //                 //     this.bsModalRef.hide();
        //                 //     this.modalService.setDismissReason(dataTree);
        //                 // }
        //                 if (res['data_rule_tree_json']) {
        //                     let datarule = res['data_rule_tree_json'];
        //                     alert('編集しました。');
        //                     this.bsModalRef.hide();
        //                     this.modalService.setDismissReason(datarule);
        //                 }
        //             } else {
        //                 // backendInfo: data valid error in saving the rule; the same name rule is existence
        //                 if (msg && msg === 'CP_NAME_DUPLICATE') {
        //                     this.uniqueFlg = false;
        //                 } else if (msg && msg === 'key_str duplicatoin') {
        //                     // 后台未做check
        //                     this.keyUnqFlg = false;
        //                 } else {
        //                     alert(msg);
        //                 }
        //             }
        //         });
        // }
    }
    public deleteRule() {
        // let alt = confirm('このルールを削除します。よろしいですか？');
        // this.apiPrefix = '/v1';
        // // let delUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId + '&coll_policy_id=' + this.cpId;
        // let delUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId + '&policy_tree_id=' + this.cpId;
        // if (alt) {
        //     this.httpClient
        //         .toJson(this.httpClient.delete(delUrl)).subscribe(res => {
        //             let status = _.get(res, 'status');
        //             let msg = _.get(status, 'message');
        //             let data = _.get(status, 'data');
        //             if (status && status['status'].toLowerCase() === 'true') {
        //                 // if (data) {
        //                 //     let dataTree: any = {};
        //                 //     dataTree = _.get(data, 'data_rule_tree_json');
        //                 //     alert('削除しました。');
        //                 //     this.bsModalRef.hide();
        //                 //     this.modalService.setDismissReason(dataTree);
        //                 // }
        //                 if (res['data_rule_tree_json']) {
        //                     let dataTree = res['data_rule_tree_json'];
        //                     alert('削除しました。');
        //                     this.bsModalRef.hide();
        //                     this.modalService.setDismissReason(dataTree);
        //                 }
        //             } else {
        //                 alert(msg);
        //             }
        //         });
        // }
    }
}
