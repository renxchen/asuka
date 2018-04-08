/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: cliBlock.component.ts
* @time: 2018/03/14
* @desc: create and edit block rule;
*/
import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../../components/utils/httpClient';
import { Validator } from '../../../components/validation/validation';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import * as _ from 'lodash';
@Component({
    selector: 'cli-block',
    templateUrl: './cliBlock.component.html',
    styleUrls: ['.././collectionPolicy.component.less']
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
    extractKey: any = null;
    // flg
    nameNotNull: Boolean = true;
    nameFlg: Boolean = true;
    uniqueFlg: Boolean = true;
    keyUnqFlg: Boolean = true;
    mrkStrNotNull: Boolean = true;
    mrkStrFlg: Boolean = true;
    mrkStrNotNull_A: Boolean = true;
    mrkStrFlg_A: Boolean = true;
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
    processFlg: Boolean = false;
    lockFlg: Boolean = false;

    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef,
        private modalService: BsModalService,
        ) {
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
                this.cpId = this.info['cPId'];
                this.ruleType = this.info['ruleType'];
                this.actionType = this.info['actionType'];
                if (this.actionType === 'edit') {
                    this.ruleId = this.info['ruleId'];
                    this.getDataRule(this.cpId, this.ruleId);
                }
            }
        }, 0);
    }
    public typeFomatter(param: any) {
        /**
        * @brief format the data in checkbox
        * @author Dan Lv
        * @date 2018/03/14
        */
        if (param && param.toString() === '0') {
            return false;
        } else if (param && param.toString() === '1') {
            return true;
        } else if (param && param === false) {
            return '0';
        } else if (param && param === true) {
            return '1';
        } else {
            return;
        }
    }
    public commInfo(cpId: any, ruleId: any) {
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree_rule/?coll_policy_id=' + cpId + '&rule_id=' + ruleId;
        this.httpClient.setUrl(this.apiPrefix);
        return this.httpClient.toJson(this.httpClient.get(url));
    }
    public getDataRule(cpId: any, ruleId: any) {
        /**
        * @brief get rule info
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.commInfo(cpId, ruleId).subscribe(res => {
            this.processFlg = _.get(res, 'is_processing');
            this.lockFlg = _.get(res, 'is_locked');
            let isUsed = _.get(res, 'rule_is_used');
            if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                if (res['data']) {
                    let data = res['data'];
                    this.name = _.get(data, 'name');
                    this.desc = _.get(data, 'desc');
                    this.markString = _.get(data, 'mark_string');
                    this.keyStr = _.get(data, 'key_str');
                    this.startLnNum = _.get(data, 'start_line_num');
                    this.endLnNum = _.get(data, 'end_line_num');
                    this.endMrkStr = _.get(data, 'end_mark_string');
                    this.isInclude = this.typeFomatter(_.get(data, 'is_include'));
                    this.isSerial = this.typeFomatter(_.get(data, 'is_serial'));
                    this.extractKey = _.get(data, 'extract_key');
                }
                if (isUsed || this.info['delFlg']) {
                    this.delBtn = false;
                } else {
                    this.delBtn = true;
                }
            }
        });
    }
    public blockRuleADCheck() {
        /**
        * @brief Verify the validity of the input information
        * @return true or false
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.uniqueFlg = true;
        this.keyUnqFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.halfWithoutSpecial(this.name);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        if (this.mrkStrNotNull) {
            this.mrkStrFlg = Validator.halfWidthReg(this.markString);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.halfWithoutSpecial(this.keyStr);
        }
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull && this.mrkStrFlg) {
            return true;
        } else {
            return false;
        }
    }
    public blockRuleBCheck() {
        /**
        * @brief Verify the validity of the input information
        * @return true or false
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.uniqueFlg = true;
        this.keyUnqFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.halfWithoutSpecial(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.halfWithoutSpecial(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        if (this.mrkStrNotNull) {
            this.mrkStrFlg = Validator.halfWidthReg(this.markString);
        }
        this.sLnNubFlg = Number.isInteger(this.startLnNum);
        this.eLnNubFlg = Number.isInteger(this.endLnNum);
        if (this.sLnNubFlg && this.eLnNubFlg) {
            this.lnNubFlg = this.startLnNum > this.endLnNum ? false : true;
        }
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.sLnNubFlg && this.eLnNubFlg
            && this.lnNubFlg && this.mrkStrNotNull
            && this.mrkStrFlg) {
            return true;
        } else {
            return false;
        }
    }
    public blockRuleCCheck() {
        /**
        * @brief Verify the validity of the input information
        * @return true or false
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.uniqueFlg = true;
        this.keyUnqFlg = true;
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.halfWithoutSpecial(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStr);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.halfWithoutSpecial(this.keyStr);
        }
        this.mrkStrNotNull_A = Validator.notNullCheck(this.markString);
        if (this.mrkStrNotNull_A) {
            this.mrkStrFlg_A = Validator.halfWidthReg(this.markString);
        }
        this.extractKeyNotNull = Validator.notNullCheck(this.extractKey);
        if (this.extractKey) {
            this.extractKeyFlg = Validator.halfWidthReg(this.extractKey);
        }
        this.endMrkNotNull = Validator.notNullCheck(this.endMrkStr);
        if (this.endMrkNotNull) {
            this.endMrkStrFlg = Validator.halfWidthReg(this.endMrkStr);
        }
        if (this.nameNotNull && this.nameFlg
            && this.keyStrNotNull && this.keyStrFlg
            && this.mrkStrNotNull_A && this.mrkStrFlg_A
            && this.endMrkNotNull && this.endMrkStrFlg
            && this.extractKeyNotNull && this.extractKeyFlg) {
            return true;
        } else {
            return false;
        }

    }
    public blockRulePrepare() {
        /**
        * @brief Collect data from the page
        * @author Dan Lv
        * @date 2018/03/14
        */
        let sendRuleInfo: any = {};
        let rule_info: any = {};
        if (this.ruleType === 'block_rule_1') {
            if (this.blockRuleADCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['is_serial'] = this.typeFomatter(this.isSerial);
                sendRuleInfo['rule_info'] = rule_info;
                return sendRuleInfo;
            }
        } else if (this.ruleType === 'block_rule_2') {
            if (this.blockRuleBCheck()) {
                rule_info['coll_policy'] = this.cpId;
                rule_info['rule_type'] = this.ruleType;
                rule_info['name'] = this.name;
                rule_info['desc'] = this.desc;
                rule_info['mark_string'] = this.markString;
                rule_info['key_str'] = this.keyStr;
                rule_info['start_line_num'] = this.startLnNum;
                rule_info['end_line_num'] = this.endLnNum;
                rule_info['is_serial'] = this.typeFomatter(this.isSerial);
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
                rule_info['extract_key'] = this.extractKey;
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
        /**
        * @brief save data
        * @post send the returned data to the 'cpEdit' page and close popup if save successly
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.apiPrefix = '/v1';
        let id = this.ruleId;
        let editUrl = '/api_policy_tree_rule/?rule_id=' + id;
        let createUrl = '/api_policy_tree_rule/';
        this.httpClient.setUrl(this.apiPrefix);
        let sendInfo = this.blockRulePrepare();
        if (this.actionType === 'create' && sendInfo !== '') {
            this.httpClient
                .toJson(this.httpClient.post(createUrl, sendInfo))
                .subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    let errMsg = _.get(res, 'verify_error_msg');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        if (data) {
                            let blockInfo: any = {};
                            blockInfo['blockTree'] = _.get(data, 'block_rule_tree_json');
                            alert('保存しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(blockInfo);
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
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    let errMsg = _.get(res, 'verify_error_msg');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        if (data) {
                            let blockInfo: any = {};
                            blockInfo['blockTree'] = _.get(data, 'block_rule_tree_json');
                            blockInfo['ruleName'] = _.get(data, 'new_name');
                            alert('保存しました。');
                            this.bsModalRef.hide();
                            this.modalService.setDismissReason(blockInfo);
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
        /**
        * @brief delete the block rule if it isn't in the database or on the policy tree.
        * @post send the returned data to the 'cpEdit' page and close popup if delete successly
        * @author Dan Lv
        * @date 2018/03/14
        */
        let alt = confirm('このルールを削除します。よろしいですか？');
        this.apiPrefix = '/v1';
        let delUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId + '&coll_policy_id=' + this.cpId;
        if (alt) {
            this.httpClient
                .toJson(this.httpClient.delete(delUrl)).subscribe(res => {
                    let status = _.get(res, 'status');
                    let msg = _.get(status, 'message');
                    let data = _.get(res, 'data');
                    if (status && status['status'].toString().toLowerCase() === 'true') {
                        if (data) {
                            let blockTree: any = {};
                            blockTree['blockTree'] = _.get(data, 'block_rule_tree_json');
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
