import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { ModalComponent } from '../../components/modal/modal.component';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'cli-detail',
    templateUrl: './cliCPDetail.component.html',
    styleUrls: ['./collectionPolicy.component.less']
})
export class CLICPDetailComponent implements OnInit, AfterViewInit {
    cPId: any;
    apiPrefix: any;
    cpName: any;
    osType: any;
    cliCommand: any;
    cpDesc: any;
    policyTree: any;
    modalRef: BsModalRef;
    closeMsg: any;
    modalMsg: any;
    // blockruleInfo
    ruleType: any;
    ruleTypeName: any;
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
    // dataruleInfo
    startLnNum: any;
    endLnNum: any;
    endMrkStr: any;
    isInclude: any;
    isSerial: any;
    ruleFlg: Boolean = false;
    iconFlg: boolean;
    treeData: any = [
        {
            'text': 'data_rule_3_subscription',
            'icon': 'fa fa-text-height fa-lg',
            'data': {
                'rule_id': '37',
                'rule_type': 'data_rule_3',
            }
        }
    ];
    constructor(
        private httpClient: HttpClientComponent,
        private activatedRoute: ActivatedRoute,
        private router: Router,
        private modalService: BsModalService
    ) {
        let cPIdTmp = this.activatedRoute.snapshot.queryParams['id'];
        if (cPIdTmp) {
            this.cPId = cPIdTmp;
            this.getCPDetailInfo(this.cPId);
        } else {
            this.router.navigate(['/index/']);
        }
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
        // this.drawPlyTree(this.treeData);
    }
    public getCPDetailInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_collection_policy/?id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data'] && res['data'].length > 0) {
                        let data = res['data'][0];
                        this.cpName = _.get(data, 'name');
                        this.osType = _.get(data, 'ostype_name');
                        this.cliCommand = _.get(data, 'cli_command');
                        this.cpDesc = _.get(data, 'desc');
                        if (res['policy_tree']) {
                            let policy = res['policy_tree'];
                            let tree = _.get(policy, 'children');
                            this.drawPlyTree(tree);
                        }
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public drawPlyTree(data: any) {
        let _t = this;
        $('#policyTree').jstree({
            core: {
                'check_callback': function (operation, node, node_parent, node_position, more) {
                    return false;
                },
                data: data
            },
            plugins: ['types', 'dnd', 'state', 'crrm', 'node_customize', 'root_node']
        }).bind('activate_node.jstree', function (e, data) {
            _t.ruleFlg = true;
            if (data.node) {
                let ruleData = data.node.data;
                _t.ruleId = _.get(ruleData, 'rule_id');
                _t.ruleType = _.get(ruleData, 'rule_type');
                _t.getDataRule(_t.ruleId);
                _t.ruleTypeName = _t.ruleNameFormatter(_t.ruleType);
            }
        });
    }
    public ruleNameFormatter(name: any) {
        if (name.indexOf('block_rule') !== -1) {
            this.iconFlg = true;
        } else {
            this.iconFlg = false;
        }
        this.ruleType = name;
        if (name === 'block_rule_1') {
            return 'インデントによるブロック定義';
        } else if (name === 'block_rule_2') {
            return '行数によるブロック定義';
        } else if (name === 'block_rule_3') {
            return '指定文字列-指定文字列でのブロック抽出';
        } else if (name === 'block_rule_4') {
            return '正規表現を含むブロック抽出';
        } if (name === 'data_rule_1') {
            return '特定文字からの距離での抽出';
        } else if (name === 'data_rule_2') {
            return '行数による抽出';
        } else if (name === 'data_rule_3') {
            return '正規表現による抽出';
        } else if (name === 'data_rule_4') {
            return '行数の抽出';
        } else {
            return '出力全抽出';
        }
    }
    public commInfo(ruleId: any) {
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree_rule/?rule_id=' + ruleId + '&coll_policy_id=' + this.cPId;
        this.httpClient.setUrl(this.apiPrefix);
        return this.httpClient.toJson(this.httpClient.get(url));
    }
    public getDataRule(ruleId: any) {
        this.commInfo(ruleId).subscribe(res => {
            let status = _.get(res, 'status');
            let data = _.get(res, 'data');
            let msg = _.get(status, 'message');
            if (status && status['status'].toLowerCase() === 'true') {
                if (data) {
                    this.name = _.get(data, 'name');
                    this.desc = _.get(data, 'desc');
                    this.markString = _.get(data, 'mark_string');
                    this.keyStr = _.get(data, 'key_str');
                    this.startLnNum = _.get(data, 'start_line_num');
                    this.endLnNum = _.get(data, 'end_line_num');
                    this.endMrkStr = _.get(data, 'end_mark_string');
                    this.isInclude = _.get(data, 'is_include');
                    this.isSerial = _.get(data, 'is_serial');
                    this.selSplitChar = _.get(data, 'split_char');
                    this.xOffset = _.get(data, 'x_offset');
                    this.yOffset = _.get(data, 'y_offset');
                    this.lineNums = _.get(data, 'line_nums');
                } else {
                    alert(msg);
                }
            }
        });
    }
    public naviCPEdit() {
        // this.apiPrefix = '/v1';
        // let url = '/api_collection_policy/?policy_type=0';
        // this.httpClient.setUrl(this.apiPrefix);
        // this.httpClient
        //     .toJson(this.httpClient.get(url + '?id=' + this.cPId))
        //     .subscribe(res => {
        //         if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
        // this.router.navigate(['/index/cliCPEdit'], { queryParams: { 'id': this.cPId } });
        //     } else {
        //         // check this cp occupation, add 'occupation' feedback
        //         if (res['status']['message'] && ['status']['message'] === 'occupation') {
        //             this.modalMsg = 'This collection policy is being occupied';
        //             this.closeMsg = 'close';
        //             this.showAlertModal(this.modalMsg, this.closeMsg);
        //         } else {
        //             if (res['status'] && res['status']['message']) {
        //                 alert(res['status']['message']);
        //             }
        //         }
        //     }
        // });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
