/**
* @author: Dan Lv
* @contact: danlv@cisco.com
* @file: cliCPEdit.component.ts
* @time: 2018/03/14
* @desc: edit cli collection policy and display tree
*/
import { Component, ViewChild, OnInit, AfterViewInit, OnDestroy, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../../components/utils/httpClient';
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
    templateUrl: './cliCPEdit.component.html',
    styleUrls: ['.././collectionPolicy.component.less'],
    providers: []
})

export class CLICPEditComponent implements OnInit, AfterViewInit, OnDestroy {
    @ViewChild('CLIDataComponent') cliModal: ModalDirective;
    plyNode: any;
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
    ) {
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            this.cPId = cPIdeTmp;
            this.getCPInfo(this.cPId);
        } else {
            this.router.navigate(['/index/cpview']);
        }

    }
    ngOnInit() { }
    ngAfterViewInit() {
        this.nodeCustomizeAndRoot();
    }
    public getCPInfo(id: any) {
        /**
        * @brief get cli collection policy info
        * @param id: collection policy id
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree/?coll_policy_id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data']) {
                        let data = res['data'];
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
        /**
        * @brief customize tree plugin
        * @author Dan Lv
        * @date 2018/03/14
        */
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
    public moveNodeRule(node) {
        /**
        * @brief root_node can not be moved
        * @author Dan Lv
        * @date 2018/03/14
        */
        if (node[0]['data'] && node[0]['data']['is_root']) {
            return false;
        }
        return true;
    }
    public policyMoveRule(operation, node, node_parent, node_position, more) {
        /**
        * @brief moving limitation of policy tree
        * @author Dan Lv
        * @date 2018/03/14
        */
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
        // block_rule_4 can not have the type of 'block_rule' children except block_rule_4
        if (node['data']['rule_type']
            && node['data']['rule_type'].indexOf('block_rule') !== -1
            && node_parent['data']['rule_type']
            && node_parent['data']['rule_type'] === 'block_rule_4') {
            if (node['data']['rule_type'] === 'block_rule_4') {
                return true;
            }
            return false;
        }
        return true;
    }
    public getPlyTreeInfo() {
        /**
        * @brief get policy tree json data
        * @return policy tree data
        * @author Dan Lv
        * @date 2018/03/14
        */
        let tree = $('#policyTree')
            .jstree(true)
            .get_json('#', {
                flat: false,
                no_state: true,
                no_li_attr: true,
                no_a_attr: true,
                no_data: false,
            });
        return tree[0];
    }
    public plyTreeFlat() {
        /**
        * @brief get flat policy tree json data
        * @return policy tree data
        * @author Dan Lv
        * @date 2018/03/14
        */
        return $('#policyTree').jstree(true).get_json('#', {
            flat: true,
            no_state: false,
            no_li_attr: false,
            no_a_attr: false,
            no_data: false,
        }
        );
    }
    // update policy name
    public findNode(ruleId: any) {
        /**
        * @brief search rule info from policy tree
        * @parma ruleId: rule id
        * @return collection policy data
        * @author Dan Lv
        * @date 2018/03/14
        */
        let plyNode: any = [];
        let tree = this.plyTreeFlat();
        for (let i = 0; i < tree.length; i++) {
            let data = tree[i]['data'];
            if (data['rule_id'] && data['rule_id'] === ruleId) {
                plyNode.push(tree[i]);
            }
        }
        return plyNode;
    }
    // check before saving policy tree
    // public checkPolicyTree() {
    //     let tree = this.plyTreeFlat();
    //     if (tree.length > 1) {
    //         for (let i = 0; i < tree.length; i++) {
    //             let data = tree[i]['data'];
    //             if (data['rule_type'] && data['rule_type'].indexOf('data_rule') !== -1) {
    //                 return true;
    //             }
    //         }
    //     } else {
    //         return true;
    //     }
    // }
    // highlight
    public hightLight(param: any) {
        /**
        * @brief highlight data
        * @parma param: data required by highlight operation
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.apiPrefix = '/v1';
        let highLightUrl = '/api_policy_tree_highlight/';
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.post(highLightUrl, param)).subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data']) {
                        let data = res['data'];
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
        /**
        * @brief save policy tree data
        * @author Dan Lv
        * @date 2018/03/14
        */
        let tree = this.getPlyTreeInfo();
        if (tree && this.cPId) {
            let param = {
                'coll_policy_id': this.cPId,
                'tree': this.getPlyTreeInfo(),
                'raw_data': $('#input-wrap').val()
            };
            this.apiPrefix = '/v1';
            let savePlytUrl = '/api_policy_tree/';
            this.httpClient.setUrl(this.apiPrefix);
            this
            .httpClient
            .toJson(this.httpClient.post(savePlytUrl, param)).subscribe(res => {
                let status = _.get(res, 'status');
                let msg = _.get(status, 'message');
                if (status && status['status'].toString().toLowerCase() === 'true') {
                    alert('保存しました');
                    this.router.navigate(['/index/clicpdetail'], { queryParams: { 'id': this.cPId } });
                } else {
                    if (msg) {
                        alert(msg);
                    }
                }
            });
        }
    }
    public blockTree(data: any) {
        /**
        * @brief get data and display it on the block_rule_tree
        * @param data: block_rule_tree data
        * @author Dan Lv
        * @date 2018/03/14
        */
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
                    let id = node['data']['rule_id'];
                    let plyNode = _t.findNode(id);
                    editBlockParam['ruleType'] = node['data']['rule_type'];
                    editBlockParam['ruleId'] = id;
                    editBlockParam['actionType'] = 'edit';
                    editBlockParam['delFlg'] = plyNode.length > 0 ? true : false;
                    editBlockParam['cPId'] = _t.cPId;
                    editBlockParam['node'] = plyNode;
                    _t.blockRuleAction(editBlockParam);
                }
            }]
        });
    }
    public dataTree(data: any) {
        /**
        * @brief get data and display it on data_rule_tree
        * @param data: data_rule_tree data
        * @author Dan Lv
        * @date 2018/03/14
        */
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
                    let plyNode = _t.findNode(id);
                    editDataParam['ruleType'] = node['data']['rule_type'];
                    editDataParam['ruleId'] = id;
                    editDataParam['actionType'] = 'edit';
                    editDataParam['delFlg'] = plyNode.length > 0 ? true : false;
                    editDataParam['cPId'] = _t.cPId;
                    editDataParam['node'] = plyNode;
                    _t.dataRuleAction(editDataParam);
                }
            }]
        });
    }
    public policyTree(data: any) {
        /**
        * @brief get data and display it on policy_rule_tree
        * @param data: policy_rule_tree data
        * @author Dan Lv
        * @date 2018/03/14
        */
        let _t = this;
        $('#policyTree').jstree({
            'core': {
                'check_callback': function (operation, node, node_parent, node_position, more) {
                    return _t.policyMoveRule(operation, node, node_parent, node_position, more);
                },
                'data': data,
            },
            'plugins': ['types', 'dnd', 'crrm', 'node_customize', 'state'],
            'types': {
                '#': { 'max_depth': 4 }
            },
            'state': { 'opened': true },
            'expand_selected_onload': true,
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
            .bind('activate_node.jstree', function (e, node) { })
            .on('select_node.jstree', function (e, data) { })
            .on('rename_node.jstree', function (node, obj) {
                $('#policyTree').jstree(true).redraw(true);
            });
    }
    public blockRuleAction(sendInfo: any) {
        /**
        * @brief show data_rule popup or rename block_rule name on policy tree
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.modalRef = this.modalService.show(CLIBlockComponent, this.modalConfig);
        this.modalRef.content.info = sendInfo;
        let blockTree$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                $('#blockTree').jstree('destroy');
                let tree = _.get(res, 'blockTree');
                let nodes = sendInfo.node;
                let text = _.get(res, 'ruleName');
                this.blockTree(tree);
                if (nodes && nodes.length > 0 && text) {
                    $('#policyTree').jstree('rename_node', nodes[0], text);
                }
            }
            this.unsubscribe(blockTree$);
        });
    }
    public dataRuleAction(sendInfo: any) {
        /**
        * @brief show data_rule popup or rename data_rule name on policy tree
        * @author Dan Lv
        * @date 2018/03/14
        */
        this.modalRef = this.modalService.show(CLIDataComponent, this.modalConfig);
        this.modalRef.content.info = sendInfo;
        let dataTree$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                $('#dataTree').jstree('destroy');
                let tree = _.get(res, 'dataTree');
                let nodes = sendInfo.node;
                let text = _.get(res, 'ruleName');
                this.dataTree(tree);
                if (nodes && nodes.length > 0 && text) {
                    $('#policyTree').jstree('rename_node', nodes[0], text);
                }
            }
            this.unsubscribe(dataTree$);
        });
    }
    // cli collecton policy edit
    public cPEdit() {
        /**
        * @brief show cli collection policy edit popup
        * @author Dan Lv
        * @date 2018/03/14
        */
        let cPId = this.cPId;
        this.modalRef = this.modalService.show(CLICPEditPopComponent, this.modalConfig);
        this.modalRef.content.cPId = cPId;
        let cpName$ = this.modalService.onHidden.subscribe(res => {
            if (res) {
                this.cPName = res;
            }
            this.unsubscribe(cpName$);
        });
    }
    ngOnDestroy() {
        if (this.modalRef) {
            this.modalRef.hide();
        }
    }
    public unsubscribe(res: any) {
        res.unsubscribe();
    }
}
