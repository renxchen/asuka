import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { Validator } from '../../components/validation/validation';
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
    splitChar: any = null;
    xOffset: any = null;
    yOffset: any = null;
    lineNums: any = null;
    // "split_char": null,分隔符按空格/，正则（data）0123
    // "extract_key": null,抽出数据的正则表达式（data）
    // "x_offset": null,横向偏移（data）
    // "y_offset": null,纵向偏移（data）
    // "line_nums": null,抽出行数（data）

    // warning flg
    descFlg: boolean;
    nameNotNull: boolean;
    nameFlg: boolean;
    mrkStrNotNull: boolean;
    mrkStrFlg: boolean;
    keyStrNotNull: boolean;
    keyStrFlg: boolean;
    lnNubFlg: boolean;
    sLnNubFlg: boolean;
    eLnNubFlg: boolean;
    endMrkNotNull: boolean;
    endMrkStrFlg: boolean;
    extractKeyNotNull: boolean;
    extractKeyFlg: boolean;

    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef) {
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (typeof (this.info) !== 'undefined') {
                // console.log('this', this.info);
                this.cpId = this.info['cpId'];
                this.ruleType = this.info['ruleType'];
                this.actionType = this.info['actionType'];
                // this.ruleId = this.info['ruleId'];
                this.ruleId = '5';
                if (this.info['actionType'] === 'edit') {
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
        this.keyStrNotNull = Validator.notNullCheck(this.keyStrNotNull);
        if (this.keyStrFlg) {
            this.keyStrFlg = Validator.noCommsymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        if (this.mrkStrNotNull) {
            this.mrkStrFlg = Validator.noCommsymbol(this.markString);
        }
        if (this.nameFlg && this.keyStrFlg && this.mrkStrFlg) {
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
        this.keyStrNotNull = Validator.notNullCheck(this.keyStrNotNull);
        if (this.keyStrNotNull) {
            this.keyStrFlg = Validator.notNullCheck(this.keyStr);
        }
        this.sLnNubFlg = Number.isInteger(this.startLnNum);
        this.eLnNubFlg = Number.isInteger(this.endLnNum);
        if (this.sLnNubFlg && this.eLnNubFlg) {
            this.lnNubFlg = this.startLnNum < this.endLnNum ? true : false;
        }
    }
    public blockRuleCCheck() {
        this.nameNotNull = Validator.notNullCheck(this.name);
        if (this.nameNotNull) {
            this.nameFlg = Validator.noSpecSymbol(this.name);
        }
        this.keyStrNotNull = Validator.notNullCheck(this.keyStrNotNull);
        if (this.keyStrFlg) {
            this.keyStrFlg = Validator.noCommsymbol(this.keyStr);
        }
        this.mrkStrNotNull = Validator.notNullCheck(this.markString);
        if (this.mrkStrNotNull) {
            this.mrkStrFlg = Validator.noCommsymbol(this.markString);
        }
        this.extractKeyNotNull = Validator.notNullCheck(this.extractKey);
        if (this.extractKey) {
            this.extractKeyFlg = Validator.noCommsymbol(this.extractKey);
        }
        this.endMrkNotNull = Validator.notNullCheck(this.endMrkStr);
        if (this.endMrkNotNull) {
            this.endMrkStrFlg = Validator.noCommsymbol(this.endMrkStr);
        }
        if (this.nameFlg && this.keyStrFlg && this.mrkStrFlg && this.endMrkStrFlg && this.extractKeyFlg) {
            return true;
        } else {
            return false;
        }

    }
    public blockRulePrepare() {
        let sendRuleInfo: any = {};
        let rule_info: any = {};
        rule_info['coll_policy'] = '1';
        rule_info['rule_type'] = this.ruleType;
        rule_info['name'] = this.name;
        rule_info['desc'] = this.desc;
        rule_info['mark_string'] = this.markString;
        rule_info['key_str'] = this.keyStr;
        rule_info['is_serial'] = this.typeFomatter(this.isSerial);
        sendRuleInfo['rule_info'] = rule_info;
        return sendRuleInfo;
        // if (this.ruleType === 'block_rule_1') {
        //     console.log('2222');
        //     if (this.blockRuleADCheck()) {
        //         console.log('33333');
        //         rule_info['coll_policy'] = this.cpId;
        //         rule_info['rule_type'] = this.ruleType;
        //         rule_info['name'] = this.name;
        //         rule_info['desc'] = this.desc;
        //         rule_info['mark_string'] = this.markString;
        //         rule_info['key_str'] = this.keyStr;
        //         rule_info['is_serial'] = this.typeFomatter(this.isSerial);
        //         console.log('rule_info', rule_info);
        //         sendRuleInfo['rule_info'] = rule_info;
        //         return sendRuleInfo;
        //     }
        // } else if (this.ruleType === 'block_rule_2') {
        //     if (this.blockRuleBCheck()) {
        //         rule_info['coll_policy'] = this.cpId;
        //         rule_info['rule_type'] = this.ruleType;
        //         rule_info['name'] = this.name;
        //         rule_info['desc'] = this.desc;
        //         rule_info['mark_string'] = this.markString;
        //         rule_info['key_str'] = this.keyStr;
        //         rule_info['start_line_num'] = this.startLnNum;
        //         rule_info['end_line_num'] = this.endLnNum;
        //         rule_info['is_serial'] = this.typeFomatter(this.isSerial);
        //         return rule_info;
        //     }
        //     return rule_info;
        // } else if (this.ruleType === 'block_rule_3') {
        //     rule_info['coll_policy'] = this.cpId;
        //     rule_info['rule_type'] = this.ruleType;
        //     rule_info['name'] = this.name;
        //     rule_info['desc'] = this.desc;
        //     rule_info['mark_string'] = this.markString;
        //     rule_info['end_mark_string'] = this.endMrkStr;
        //     rule_info['extractKey'] = this.extractKey;
        //     rule_info['key_str'] = this.keyStr;
        //     rule_info['is_serial'] = this.typeFomatter(this.isSerial);
        //     rule_info['is_include'] = this.typeFomatter(this.isInclude);
        //     return rule_info;
        // } else if (this.ruleType === 'block_rule_4') {
        //     if (this.blockRuleADCheck()) {
        //         rule_info['coll_policy'] = this.cpId;
                // rule_info['rule_type'] = this.ruleType;
        //         rule_info['name'] = this.name;
        //         rule_info['desc'] = this.desc;
        //         rule_info['mark_string'] = this.markString;
        //         rule_info['key_str'] = this.keyStr;
        //         return rule_info;
        //     }
        // }
        // return;
    }
    public save() {
    //     this.apiPrefix = '/v1';
    //     let editUrl = '/api_policy_tree_rule/?rule_id=' + this.ruleId;
    //     let createUrl = '/api_policy_tree_rule/';
    //     this.httpClient.setUrl(this.apiPrefix);
    //     if (this.actionType === 'create') {
    //         this.httpClient
    //             .toJson(this.httpClient.post(createUrl, this.blockRulePrepare()))
    //             .subscribe(res => {
    //                 console.log('res', res);
    //                 if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
    //                     alert('save success');
    //                 } else {
    //                     if (res['status'] && res['status']['message']) {
    //                         alert('modify failure');
    //                     }
    //                 }
    //             });

    //     } else {
    //         this.httpClient
    //             .toJson(this.httpClient.put(editUrl, this.blockRulePrepare()))
    //             .subscribe(res => {
    //                 if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
    //                     alert('modify success');
    //                 } else {
    //                     if (res['status'] && res['status']['message']) {
    //                         alert('modify failure');
    //                     }
    //                 }
    //             });
    //     }
    }
}
