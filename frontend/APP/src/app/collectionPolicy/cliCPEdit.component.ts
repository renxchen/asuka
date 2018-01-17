import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { CLICPLoginComponent } from './cliCPLogin.component';
import { CLIBlockComponent } from './cliBlock.component';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
declare var $: any;

@Component({
    selector: 'cli-edit',
    templateUrl: 'cliCPEdit.component.html',
    styleUrls: ['collectionPolicy.component.less']
})

export class CLICPEditComponent implements OnInit, AfterViewInit {
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
    testData: any = [
        {
            'text': 'block_1',
            'icon': 'fa fa-folder-o',
            'data': {
                'is_root': true, // root_node can not be moved;
                'rule_type': 'block_rule_1', // for editing and deleting
            },
            'state': {
                'opened': true,
            },
            'children': [
                {
                    'text': 'br_1_1',
                    'icon': 'fa fa-cubes',
                    'children': [],
                    'data': {
                        'rule_id': 1,
                        'rule_type': 'block_rule_1'
                    },
                },
                {
                    'text': 'br_1_2',
                    'icon': 'fa fa-cubes',
                    'children': [],
                    'data': {
                        'rule_id': 2,
                        'rule_type': 'block_rule_1'
                    }
                }
            ],
        },
        {
            'text': 'b2',
            'icon': 'fa fa-folder-o',
            'data': {
                'rule_type': 'block_rule_2',
                'is_root': true,
            },
            'state': {
                'opened': true,
            },
            'children': [
                {
                    'text': 'br_2_1',
                    'icon': 'fa fa-cubes',
                    'children': [],
                    'data': {
                        'rule_type': 'block_rule_2',
                        'rule_id': 3
                    }
                }
            ],
        },
        {
            'text': 'b3',
            'icon': 'fa fa-folder-o',
            'data': {
                'rule_type': 'block_rule_3',
                'is_root': true
            },
            // root can't be moved
            'state': {
                'opened': true, // is the node open
            },
            'children': [
                {
                    'text': 'br_3_1',
                    'icon': 'fa fa-cubes',
                    'children': [],
                    'data': {
                        'rule_type': 'block_rule_3',
                        'rule_id': 4
                    }
                }
            ],
        },
        {
            'text': 'b4',
            'icon': 'fa fa-folder-o',
            'data': {
                'rule_type': 'block_rule_4',
                'is_root': true
            },
            // root can't be moved
            'state': {
                'opened': true, // is the node open
            },
            'children': [
                {
                    'text': 'br_4_1',
                    'icon': 'fa fa-cubes',
                    'children': [],
                    'data': {
                        'rule_type': 'block_rule_4',
                        'rule_id': 5
                    }
                }
            ],
        }
    ];
    testData2: any = [
        // 'Simple root node',
        {
            'text': 'd1',
            // used for create rule
            'icon': 'fa fa-folder-o',
            'data': {
                'rule_type': 'data_rule_1',
                'is_root': true,
            },
            'children': [
                {
                    'text': 'd_1_1',
                    'icon': 'fa fa-text-height',
                    'data': {
                        'rule_type': 'data_rule_1',
                        'rule_id': 5
                    }
                },
                {
                    'text': 'd_1_2',
                    'icon': 'fa fa-text-height',
                    'data': {
                        'rule_type': 'data_rule_1',
                    }
                }
            ]
        },
        {
            'text': 'd2',
            'icon': 'fa fa-folder-o',
            'data': {
                'rule_type': 'data_rule_2',
                'is_root': true,
            },
            'children': [
                {
                    'text': 'd_2_1',
                    // used for editing and delete
                    'icon': 'fa fa-text-height',
                    'data': {
                        'rule_type': 'data_rule_2',
                        'rule_id': 6
                    }
                },
                {
                    'text': 'd_2_2',
                    'icon': 'fa fa-text-height',
                    'data': {
                        'rule_type': 'data_rule_2',
                        'rule_id': 7
                    }
                }
            ]
        },
        {
            'text': 'd3',
            'icon': 'fa fa-folder-o',
            'data': {
                'type': 'data_rule_3',
                'is_root': true,
            },
            'type': 'data_rule_3',
            'children': [
                {
                    'text': 'd_3_1',
                    'icon': 'fa fa-text-height',
                    'data': {
                        'rule_type': 'data_rule_3',
                        'rule_id': 8
                    }
                },
                {
                    'text': 'd_3_2',
                    'icon': 'fa fa-text-height',
                    'data': {
                        'rule_type': 'data_rule_3',
                        'rule_id': 9,
                    }
                }
            ],
        }
    ];
    testData3: any = [
        {
            'text': 'test',
            'icon': 'fa fa-tags fa-lg',
            'data': {
                'rule_type': 'policy_rule',
                'is_root': true,
            }
        },

    ];
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
        private modalService: BsModalService
    ) {
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            this.cPId = cPIdeTmp;
            this.getCPInfo(this.cPId);
        }
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
        this.nodeCustomizeAndRoot();
        // this.blockTree(this.testData);
        // this.dataTree(this.testData2);
        // this.policyTree(this.testData3);
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
        if (node_parent.parent === null) {
            return false;
        }
        // block_rule can't be dragged to data_rule;
        if (node['data']['rule_type'].indexOf('block_rule') !== -1
            && node_parent['data']['rule_type']
            && node_parent['data']['rule_type'].indexOf('data_rule') !== -1) {
            return false;
        }
        // data_rule be dragged to data
        if (node['data']['rule_type'].indexOf('data_rule') !== -1
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
        return $('#policyTree')
            .jstree(true)
            .get_json('#', {
                flat: false, no_state: true,
                no_li_attr: true, no_a_attr: true,
                no_data: false,
            });
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
        // let param = {
        //     'coll_policy_id': this.cPId,
        //     'tree': this.getPlyTreeInfo()[0],
        //     'raw_data': $('#input-wrap').val()
        // };
        // this.apiPrefix = '/v1';
        // let savePlytUrl = '/api_policy_tree/';
        // this.httpClient.setUrl(this.apiPrefix);
        // this.httpClient
            // .toJson(this.httpClient.post(savePlytUrl, param)).subscribe(res => {
            //     if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
            //         alert('保存しました');
            //         this.router.navigate(['/index/cliCPDetail'], { queryParams: { 'id': this.cPId } });
            //     } else {
            //         if (res['status'] && res['status']['message']) {
            //             alert(res['status']['message']);
            //         }
            //     }
            // });
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
                        style="margin-left:20px" type="button" >
                            <i class="fa fa-plus-square"></i>&nbsp追加
                        </button>`,
                'click': function (event) {
                    let addBlockParam: any;
                    let blockRuleType = event.data.node['data']['rule_type'];
                    let actionType = 'create';
                    addBlockParam = {
                        'ruleType': blockRuleType,
                        'actionType': actionType,
                        'cPId': _t.cPId
                    };
                    _t.blockRuleAction(addBlockParam);
                    // console.log('block_add', addBlockParam);
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
                    let blockRuleType = event.data.node['data']['rule_type'];
                    let blockRuleId = event.data.node['data']['rule_id'];
                    let actionType = 'edit';
                    let editBlockParam: any;
                    editBlockParam = {
                        'ruleType': blockRuleType,
                        'actionType': actionType,
                        'blockRuleId': blockRuleId,
                        'cPId': _t.cPId
                    };
                    _t.blockRuleAction(editBlockParam);
                }
            }]
        }).bind('move_node.jstree', function (e, data) {
        }).bind('activate_node.jstree', function (e, node) {
            // console.log(node);
            // show_detail(node);
        });
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
                        style="margin-left:20px" type="button" >
                            <i class="fa fa-plus-square"></i>&nbsp追加
                        </button>`,
                'click': function (event) {
                    let addDataParam: any;
                    let dataRuleType = event.data.node['data']['rule_type'];
                    let actionType = 'create';
                    addDataParam = {
                        'ruleType': dataRuleType,
                        'actionType': actionType,
                        'cPId': _t.cPId
                    };
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
                    let dataRuleType = event.data.node['data']['rule_type'];
                    let dataRuleId = event.data.node['data']['rule_id'];
                    let actionType = 'edit';
                    let editDataParam: any;
                    editDataParam = {
                        'ruleType': dataRuleType,
                        'actionType': actionType,
                        'dataRuleId': dataRuleId,
                        'cPId': _t.cPId
                    };
                    _t.dataRuleAction(editDataParam);
                }
            }]
        }).bind('move_node.jstree', function (e, data) {})
        .bind('activate_node.jstree', function (e, node) {});
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
                    'html': `<button class="btn btn-outline btn-danger  btn-xs"
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
                            'tree': _t.getPlyTreeInfo()[0],
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
            .bind('move_node.jstree', function (e, data) {})
            .on('copy_node.jstree', function (e, data) {
                data.node.original = $.extend(true, data.node.original, data.original.original);
                data.node.data = $.extend(true, data.node.data, data.original.data);
            })
            .bind('activate_node.jstree', function (e, node) {});
    }
    public blockRuleAction(sendInfo: any) {
        this.modalRef = this.modalService.show(CLIBlockComponent, this.modalConfig);
        this.modalRef.content.info = sendInfo;
    }
    public dataRuleAction(sendInfo: any) {
        // this.bsModalRef = this.modalService.show(CLIdataComponent, this.modalConfig);
        // this.bsModalRef.content.info = sendInfo;
     }
     // detail haven't been completed
}
