import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Validator } from '../../components/validation/validation';
import { CollectionPolicyService } from './collectionPolicy.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import * as _ from 'lodash';
@Component({
    selector: 'cli-block',
    templateUrl: './cliBlock.component.html',
    styleUrls: ['./collectionPolicy.component.less']
})

export class CLIBlockComponent implements OnInit, AfterViewInit {
    apiPrefix: any;
    cpId: any;
    info: any;
    actionType: any;
    ruleType: any;
    ruleId: any;
    // block rule
    name: any;
    desc: any;
    markString: any;
    keyStr: any;
    startLnNum: any;
    endLnNum: any;
    endMrkStr: any;
    isInclude: any;
    isSerial: any;
    // data rule
    extractKey: any = null;
    // warning flg
    // descFlg: Boolean = false;
    nameNotNull: Boolean = true;
    nameFlg: Boolean = true;
    uniqueFlg: Boolean = true;
    keyUnqFlg: Boolean = true;
    mrkStrNotNull: Boolean = true;
    mrkStrNotNull_A: Boolean = true;
    keyStrNotNull: Boolean = true;
    keyStrFlg: Boolean = true;
    lnNubFlg: Boolean = true;
    sLnNubFlg: Boolean = true;
    eLnNubFlg: Boolean = true;
    endMrkNotNull: Boolean = true;
    endMrkStrFlg: Boolean = true;
    extractKeyNotNull: Boolean = true;
    extractKeyFlg: Boolean = true;
    delBtn: Boolean = false;

    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef,
        private modalService: BsModalService,
        private service: CollectionPolicyService) {
    }
    ngOnInit() {
        this.startLnNum = 0;
        this.endLnNum = 0;
        this.isSerial = true;
        this.isInclude = true;
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (typeof (this.info) !== 'undefined') {
                // console.log('this', this.info);
                this.cpId = this.info['cPId'];
                console.log('cpid', this.info);
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
    public typeFomatter(param: any) {
        if (param.toString() === '0') {
            return false;
        } else if (param.toString() === '1') {
            return true;
        } else if (param === false) {
            return '0';
        } else {
            return '1';
        }
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
                    this.startLnNum = _.get(data, 'start_line_num');
                    this.endLnNum = _.get(data, 'end_line_num');
                    this.endMrkStr = _.get(data, 'end_mark_string');
                    this.isInclude = _.get(data, 'is_include');
                    this.isSerial = _.get(data, 'is_serial');
                }
            }
        });
    }
    public blockRuleADCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull) {
            return true;
        } else {
            return false;
        }
    }
    public blockRuleBCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        this.sLnNubFlg = Number.isInteger(this.startLnNum);
        this.eLnNubFlg = Number.isInteger(this.endLnNum);
        if (this.sLnNubFlg && this.eLnNubFlg) {
            this.lnNubFlg = this.startLnNum > this.endLnNum ? false : true;
        }
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.sLnNubFlg && this.eLnNubFlg
            && this.lnNubFlg && this.mrkStrNotNull) {
            return true;
        } else {
            return false;
        }
    }
    public blockRuleCCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrFlg) {
            this.keyStrFlg = Validator.noSpecSymbol(this.keyStr);
        }
        this.mrkStrNotNull_A = Validator.notNullCheck(this.markString);
        this.extractKeyNotNull = Validator.notNullCheck(this.extractKey);
        // if (this.extractKey) {
        //     this.extractKeyFlg = Validator.noCommsymbol(this.extractKey);
        // }
        this.endMrkNotNull = Validator.notNullCheck(this.endMrkStr);
        // if (this.endMrkNotNull) {
        //     this.endMrkStrFlg = Validator.noCommsymbol(this.endMrkStr);
        // }
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull_A && this.endMrkStrFlg && this.extractKeyFlg) {
            return true;
        } else {
            return false;
        }

    }
    public blockRulePrepare() {
        let sendRuleInfo: any = {};
        let rule_info: any = {};
        if (this.ruleType === 'block_rule_1') {
            if (this.blockRuleADCheck()) {
                console.log('b1');
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['is_serial'] = this.typeFomatter(this.isSerial);
                console.log('rule_info', rule_info);
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'block_rule_2') {
            console.log(12);
            if (this.blockRuleBCheck()) {
                console.log('b2');
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['start_line_num'] = this.startLnNum;
                rule_info['end_line_num'] = this.endLnNum;
                rule_info['is_serial'] = this.typeFomatter(this.isSerial);
                console.log(rule_info);
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'block_rule_3') {
            if (this.blockRuleCCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['end_mark_string'] = this.endMrkStr;
                // same as marktring
                rule_info['extractKey'] = this.extractKey;
                rule_info['key_str'] = this.keyStr;
                rule_info['is_serial'] = this.typeFomatter(this.isSerial);
                rule_info['is_include'] = this.typeFomatter(this.isInclude);
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'block_rule_4') {
            if (this.blockRuleADCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        }
        return '';
    }
    public saveRule() {
        return;
        this.apiPrefix = '/v1';
        let id = this.cpId;
        let editUrl = '/api_policy_tree_rule/?rule_id=' + id;
        let createUrl = '/api_policy_tree_rule/';
        this.httpClient.setUrl(this.apiPrefix);
        let sendInfo = this.blockRulePrepare();
        console.log('sendInfo', sendInfo);
        if (this.actionType === 'create' && sendInfo !== '') {
            this.httpClient
                .toJson(this.httpClient.post(createUrl, sendInfo))
                .subscribe(res => {
                    console.log(res);
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(status, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data) {
                            let blockTree: any = {};
                            blockTree = _.get(data, 'block_rule_tree_json');
                            alert('保存しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(blockTree);
                        }
                    } else {
                        if (msg && msg === 'the same name rule is existence') {
                            this.uniqueFlg = false;
                        } else if (msg && msg === 'key_str duplicatoin') {
                            this.keyUnqFlg = false;
                        } else {
                            alert(msg);
                        }
                    }
                });

        } else if (this.actionType === 'edit' && sendInfo !== '') {
            this.httpClient
                .toJson(this.httpClient.put(editUrl, this.blockRulePrepare()))
                .subscribe(res => {
                    console.log(res);
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(status, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data) {
                            let blockTree: any = {};
                            blockTree = _.get(data, 'block_rule_tree_json');
                            alert('編集しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(blockTree);
                        }
                    } else {
                        if (msg && msg === 'the same name rule is existence') {
                            this.uniqueFlg = false;
                        } else if (msg && msg === 'key_str duplicatoin') {
                            this.keyUnqFlg = false;
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
        // let delUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId + '&coll_policy_id=' + this.cpId;
        let delUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId + '&policy_tree_id=' + this.cpId;
        if (alt) {
            this.httpClient
                .toJson(this.httpClient.delete(delUrl)).subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(status, 'data');
                    if (status && status['status'].toLowerCase() === 'true') {
                        if (data) {
                            let blockTree: any = {};
                            blockTree = _.get(data, 'block_rule_tree_json');
                            alert('削除しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(blockTree);
                        }
                    } else {
                        alert(msg);
                    }
                });
        }
    }
}
