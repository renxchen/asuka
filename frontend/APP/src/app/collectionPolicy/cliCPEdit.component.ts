import { Component, ViewChild, OnInit, AfterViewInit, OnDestroy, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { CollectionPolicyService } from './collectionPolicy.service';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { CLICPEditPopComponent } from './cliCPEditPop.component';
import { CLIBlockComponent } from './cliBlock.component';
import { CLIDataComponent } from './cliData.component';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { ModalDirective } from 'ngx-bootstrap/modal';
import { Subscription } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'cli-edit',
    templateUrl: 'cliCPEdit.component.html',
    styleUrls: ['collectionPolicy.component.less'],
    providers: [CollectionPolicyService]
})

export class CLICPEditComponent implements OnInit, AfterViewInit, OnDestroy {
    @ViewChild('CLIDataComponent') cliModal: ModalDirective;
    cPId: string;
    apiPrefix: string;
    cPName: string;
    blockTreeData: any;
    dataTreeData: any;
    ruleTreeData: any;
    modalRef: BsModalRef;
    cliBlock: CLIBlockComponent;
    modalConfig = {
        animated: true,
        keyboard: false,
        backdrop: true,
        ignoreBackdropClick: true,
        class: 'modal-lg'
    };
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService,
        public service: CollectionPolicyService,
    ) {
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            this.cPId = cPIdeTmp;
            this.getCPInfo(this.cPId);
        } else {
            this.router.navigate(['/index/']);
        }

    }
    ngOnInit() { }
    ngAfterViewInit() {
        this.nodeCustomizeAndRoot();
    }
    public getCPInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree/?coll_policy_id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data']) {
                        let data = res['data'];
                        // console.log(data);
                        this.cPName = data['coll_policy_name'];
                        this.blockTreeData = data['block_rule_tree_json'];
                        this.dataTreeData = data['data_rule_tree_json'];
                        this.ruleTreeData = data['policy_tree_json'];
                        $('#input-wrap').html(data['cli_command_result']);
                        this.blockTree(this.blockTreeData);
                        this.dataTree(this.dataTreeData);
                        this.policyTree(this.ruleTreeData);
                    }
                }
            });
    }
    public nodeCustomizeAndRoot() {
        'use strict';
        // node_customize
        if ($.jstree.plugins.node_customize) { return; }
        $.jstree.defaults.node_customize = {};
        $.jstree.plugins.node_customize = function (options, parent) {
            this.redraw_node = function (obj, deep, callback, force_draw) {
                let node_id = obj;
                let node = this.get_node(obj);
                let el = parent.redraw_node.call(this, obj, deep, callback, force_draw);
                let i, j, tmp = null, elm = null;
                if (el && node && node.parent !== '#') {
                    for (i = 0, j = el.childNodes.length; i < j; i++) {
                        if (el.childNodes[i] && el.childNodes[i].className && el.childNodes[i].className.indexOf('jstree-anchor') !== -1) {
                            tmp = el.childNodes[i];
                            break;
                        }
                    }
                    if (tmp) {
                        let cfg = this.settings.node_customize;
                        for (let i = 0; i < cfg.length; i++) {
                            let $html = $(cfg[i].html);
                            $html.insertAfter(tmp);
                            $html.bind('click', { 'node': node }, cfg[i].click);
                        }


                    }
                }
                return el;
            };
        };

        // root_node
        if ($.jstree.plugins.root_node) { return; }
        $.jstree.defaults.root_node = {};
        $.jstree.plugins.root_node = function (options, parent) {
            this.redraw_node = function (obj, deep, callback, force_draw) {
                let node_id = obj;
                let node = this.get_node(obj);
                let el = parent.redraw_node.call(this, obj, deep, callback, force_draw);
                let i, j, tmp = null, elm = null;

                if (node.parent === '#') {
                    for (i = 0, j = el.childNodes.length; i < j; i++) {
                        if (el.childNodes[i] && el.childNodes[i].className && el.childNodes[i].className.indexOf('jstree-anchor') !== -1) {
                            tmp = el.childNodes[i];
                            break;
                        }
                    }
                    if (tmp) {
                        let cfg = this.settings.root_node;
                        for (let i = 0; i < cfg.length; i++) {
                            let $html = $(cfg[i].html);
                            $html.insertAfter(tmp);
                            $html.bind('click', { 'node': node }, cfg[i].click);
                        }


                    }
                }
                return el;
            };
        };
    }
    // root_node can not be moved
    public moveNodeRule(node) {
        if (node[0]['data'] && node[0]['data']['is_root']) {
            return false;
        }
        return true;
    }
    public policyMoveRule(operation, node, node_parent, node_position, more) {
        // console.log(node, operation, more);
        if (node_parent.parent === null) {
            return false;
        }
        // block_rule can't be dragged to data_rule;
        if (node['data']['rule_type'] && node['data']['rule_type'].indexOf('block_rule') !== -1
            && node_parent['data']['rule_type']
            && node_parent['data']['rule_type'].indexOf('data_rule') !== -1) {
            return false;
        }
        // data_rule be dragged to data
        if (node['data']['rule_type'] && node['data']['rule_type'].indexOf('data_rule') !== -1
            && node_parent['data']['rule_type']
            && node_parent['data']['rule_type'].indexOf('data_rule') !== -1) {
            return false;
        }
        // policy tree can keep open;
        if (operation === 'copy_node') {
            node_parent.state.opened = true;
        }
        return true;
    }
    // policy tree hightlight
    public getPlyTreeInfo() {
        let tree = $('#policyTree')
            .jstree(true)
            .get_json('#', {
                flat: false, no_state: true,
                no_li_attr: true, no_a_attr: true,
                no_data: false,
            });
        return tree[0];
    }
    // check ruleId on policy tree
    public findNode(tree: any, ruleId: any) {
        let data = tree['data'];
        if (_.has(data, 'rule_id')) {
            if (data['rule_id'].toString() === ruleId.toString()) {
                return true;
            }
        }
        if (_.has(tree, 'children')) {
            for (let child of tree['children']) {
                if (child) {
                    if (this.findNode(child, ruleId)) {
                        return true;
                    }
                }
            }
        }
    }
    // check before saving policy tree
    public checkPolicyTree(tree: any) {
        let data = tree['data'];
        if (_.has(data, 'rule_type')) {
            if (data['rule_type'].indexOf('data_rule') !== -1) {
                return true;
            }
        }
        if (_.has(tree, 'children')) {
            for (let child of tree['children']) {
                if (child) {
                    if (this.checkPolicyTree(child)) {
                        return true;
                    }
                }
            }
        }
    }
    // highlight
    public hightLight(param: any) {
        this.apiPrefix = '/v1';
        let highLightUrl = '/api_policy_tree_highlight/';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.post(highLightUrl, param)).subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        let data = res['data'];
                        // data
                        $('#highlight').html(data);
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                    }
                }
            });
    }
    public savePlyTree() {
        return;
        let tree = this.getPlyTreeInfo();
        if (this.checkPolicyTree(tree)) {
            let param = {
                'coll_policy_id': this.cPId,
                'tree': tree,
                'raw_data': $('#input-wrap').val()
            };
            this.apiPrefix = '/v1';
            let savePlytUrl = '/api_policy_tree/';
            this.httpClient.setUrl(this.apiPrefix);
            this.httpClient
                .toJson(this.httpClient.post(savePlytUrl, param)).subscribe(res => {
                    if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                        alert('保存しました');
                        this.router.navigate(['/index/cliCPDetail'], { queryParams: { 'id': this.cPId } });
                    } else {
                        if (res['status'] && res['status']['message']) {
                            alert(res['status']['message']);
                        }
                    }
                });
        } else {
            alert('There is no dataRule on the policy tree');
        }
    }
    public blockTree(data: any) {
        let _t = this;
        $('#blockTree').jstree({
            'core': {
                'check_callback': function (operation, node, node_parent, node_position, more) {
                    return false;
                },
                'data': data,
            },
            'plugins': ['types', 'dnd', 'crrm', 'node_customize', 'root_node'],
            'dnd': {
                'is_draggable': function (node) {
                    return _t.moveNodeRule(node);
                },
                'always_copy': true,
            },
            'root_node':
            [{
                'html': `<button class="btn btn-xs btn-primary"
                        style="margin-left:10px" type="button" >
                            <i class="fa fa-plus-square"></i>追加
                        </button>`,
                'click': function (event) {
                    let addBlockParam: any = {};
                    let node = event.data.node;
                    let actionType = 'create';
                    addBlockParam['ruleType'] = node['data']['rule_type'];
                    addBlockParam['actionType'] = 'create';
                    addBlockParam['cPId'] = _t.cPId;
                    _t.blockRuleAction(addBlockParam);
                }
            }],
            'node_customize': [{
                'html': `<button class="btn btn-outline btn-info btn-xs"
                        sytle="margin-left:10px;margin-bottom:2px;
                        " type="button">
                            <i class="fa fa-paste"></i>編集
                        </button>`,
                'click': function (event) {
                    let node = event.data.node;
                    let editBlockParam: any = {};
                    let tree = _t.getPlyTreeInfo();
                    let id = node['data']['rule_id'];
                    editBlockParam['ruleType'] = node['data']['rule_type'];
                    editBlockParam['ruleId'] = id;
                    editBlockParam['actionType'] = 'edit';
                    editBlockParam['delFlg'] = _t.findNode(tree, id);
                    editBlockParam['cPId'] = _t.cPId;
                    _t.blockRuleAction(editBlockParam);
                }
            }]
        });
        // .bind('move_node.jstree', function (e, data) {
        // }).bind('activate_node.jstree', function (e, node) {
        //     console.log(node);
        //     show_detail(node);
        // });
    }
    public dataTree(data: any) {
        let _t = this;
        $('#dataTree').jstree({
            'core': {
                'check_callback': function (operation, node, node_parent, node_position, more) {
                    return false;
                },
                'data': data,
            },
            'plugins': ['types', 'dnd', 'state', 'crrm', 'node_customize', 'root_node'],
            'dnd': {
                'is_draggable': function (node) {
                    return _t.moveNodeRule(node);
                },
                'always_copy': true,
            },
            'state': { 'opened': true },
            'root_node':
            [{
                'html': `<button class="btn btn-xs btn-primary"
                        style="margin-left:10px" type="button" >
                            <i class="fa fa-plus-square"></i>追加
                        </button>`,
                'click': function (event) {
                    let addDataParam: any = {};
                    let node = event.data.node;
                    addDataParam['ruleType'] = node['data']['rule_type'];
                    addDataParam['actionType'] = 'create';
                    addDataParam['cPId'] = _t.cPId;
                    _t.dataRuleAction(addDataParam);
                }
            }],
            'node_customize': [{
                'html': `<button class="btn btn-outline btn-info btn-xs"
                        sytle="margin-left:10px;margin-bottom:2px;
                        " type="button">
                            <i class="fa fa-paste"></i> 編集
                        </button>`,
                'click': function (event) {
                    let node = event.data.node;
                    let editDataParam: any = {};
                    let tree = _t.getPlyTreeInfo();
                    let id = node['data']['rule_id'];
                    editDataParam['ruleType'] = node['data']['rule_type'];
                    editDataParam['ruleId'] = id;
                    editDataParam['actionType'] = 'edit';
                    editDataParam['delFlg'] = _t.findNode(tree, id);
                    editDataParam['cPId'] = _t.cPId;
                    _t.dataRuleAction(editDataParam);
                }
            }]
        });
        // .bind('move_node.jstree', function (e, data) {
        //     console.log('move_node.jstree', e, data);
        // }).bind('activate_node.jstree', function (e, node) {
        //     console.log('regreshsh', e, data);
        // });
    }
    public policyTree(data: any) {
        let _t = this;
        $('#policyTree').jstree({
            'core': {
                'check_callback': function (operation, node, node_parent, node_position, more) {
                    return _t.policyMoveRule(operation, node, node_parent, node_position, more);
                },
                'data': data,
            },
            'plugins': ['type', 'dnd', 'crrm', 'node_customize', 'state'],
            'type': { 'opened': true },
            'dnd': {
                'is_draggable': function (node) {
                    return _t.moveNodeRule(node);
                }
            },
            'node_customize': [
                {
                    'html': `<button class="btn btn-outline btn-danger btn-xs"
                                sytle="margin-left:10px;margin-bottom:2px;"
                                type="button">
                                <i class="fa fa-minus-square"></i> 消除
                            </button>`,
                    'click': function (event) {
                        $('#policyTree').jstree(`delete_node`, event.data.node.id);
                    }
                },
                {
                    'html': `<button class="btn btn-success btn-outline btn-xs"
                                sytle="margin-left:10px;margin-bottom:2px;"
                                type="button">
                                <i class="fa fa-list"></i> ハイライト
                            </button>`,
                    'click': function (event) {
                        return;
                        let param = {
                            'coll_policy_id': _t.cPId,
                            'tree': _t.getPlyTreeInfo(),
                            'tree_id': event.data.node['id'],
                            'raw_data': $('#input-wrap').val()
                        };
                        // highlight;
                        if (param.raw_data) {
                            _t.hightLight(param);
                        } else {
                            alert('raw_data is null');
                        }
                    }
                }
            ],
        })
            .bind('move_node.jstree', function (e, data) { })
            .on('copy_node.jstree', function (e, data) {
                data.node.original = $.extend(true, data.node.original, data.original.original);
                data.node.data = $.extend(true, data.node.data, data.original.data);
            })
            .bind('activate_node.jstree', function (e, node) { });
    }
    public blockRuleAction(sendInfo: any) {
        this.modalRef = this.modalService.show(CLIBlockComponent, this.modalConfig);
        this.modalRef.content.info = sendInfo;
        let blockTree$ = this.modalService.onHidden.subscribe((res => {
            // console.log('456', res);
            if (res) {
                $('#dataTree').jstree('destroy');
                this.dataTree(res);
            }
            this.unsubscribe(blockTree$);
        }));
    }
    public dataRuleAction(sendInfo: any) {
        this.modalRef = this.modalService.show(CLIDataComponent, this.modalConfig);
        this.modalRef.content.info = sendInfo;
        let dataTree$ = this.modalService.onHidden.subscribe((res => {
            console.log('123');
            if (res) {
                $('#dataTree').jstree('destroy');
                this.dataTree(res);
            }
            this.unsubscribe(dataTree$);
        }));
    }
    // cli collecton policy edit
    public cPEdit() {
        return;
        let cPId = this.cPId;
        this.modalRef = this.modalService.show(CLICPEditPopComponent, this.modalConfig);
        this.modalRef.content.cPId = cPId;
        let cpName$ = this.modalService.onHidden.subscribe((res => {
            if (res) {
                this.cPName = res;
            }
            this.unsubscribe(cpName$);
        }));
    }
    ngOnDestroy(): void {
    }
    public unsubscribe(res: any) {
        res.unsubscribe();
    }
}
