import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
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
    testData: any = [
        {
            'text': 'b1',
            'children': [
                {
                    'text': 'rule 1rule 1',
                    'children': [],
                    'id': 1
                },
                {
                    'text': 'testc',
                    'children': [],
                    'id': 6
                }
            ],
            'id': 0,
        },
        {
            'text': 'b2',
            'children': [
                {
                    'text': 'block rule 2',
                    'children': [],
                    'id': 2
                }
            ],
            'id': 0
        },
        {
            'text': 'b3',
            'children': [
                {
                    'text': 'block rule 3',
                    'children': [],
                    'rule_id': 3
                }
            ],
            'id': 0
        }
    ];
    testData2: any = [
        // 'Simple root node',
        {
            'text': 'Root node 2 <button type="button" class="btn btn-xs btn-primary add"><i class="fa fa-plus-square"></i> 追加</button>',
            'children': [
                { 'text': 'Child 1' },
                'Child 2'
            ]
        },
        {
            'text': 'Root node 2 <button type="button" class="btn btn-xs btn-primary add"><i class="fa fa-plus-square"></i> 追加</button>',
            'children': [
                { 'text': 'Child 1' },
                'Child 2'
            ]
        },
        {
            'text': 'Root node  <button type="button" class="btn btn-xs btn-primary add"><i class="fa fa-plus-square"></i> 追加</button>',
            'children': [
                { 'text': 'Child 1' },
                'Child 2',
            ],
        }
    ];
    testData3: any = [
        {
            'text': 'test',
            'rule_id': 0,
            // 'children': [
            //     {
            //         'text': 'block rule 1',
            //         'rule_id': 1,
            //         'children': [
            //             {
            //                 'text': 'block rule 2',
            //                 'rule_id': 2,
            //                 'children': [],
            //                 'id': 'j1-2',
            //             },
            //             {
            //                 'text': 'data rule 1',
            //                 'rule_id': 4,
            //                 'children': [],
            //                 'id': 'j1-3',
            //             },
            //             {
            //                 'text': 'data rule 1',
            //                 'rule_id': 4,
            //                 'children': [],
            //                 'id': 'j1-4',
            //             }
            //         ],
            //         'id': 'j1-1',
            //     }
            // ],
            'id': 'j1',
        },

    ];
    constructor(
        private router: Router,
        private activedRoute: ActivatedRoute,
        private httpClient: HttpClientComponent,
    ) {
        let cPIdeTmp: any = this.activedRoute.snapshot.queryParams['id'];
        if (cPIdeTmp && typeof (cPIdeTmp) !== 'undefined') {
            console.log(cPIdeTmp);
            this.cPId = cPIdeTmp;
            // this.getCPInfo(this.cPId);
        }
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
        this.blockTree(this.testData);
        this.dataTree(this.testData2);
        this.policyTree(this.testData3);
        this.getSelectedNode();
        // this.moveNode();
    }
    public getCPInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = '/api_policy_tree/?coll_policy_id=' + id;
        this.httpClient.setUrl(this.apiPrefix);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                console.log('res', res);
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data']) {
                        console.log('in');
                        let data = res['data'];
                        this.cPName = data['coll_policy_name'];
                        this.blockTreeData = data['block_rule_tree_json'];
                        this.dataTreeData = data['data_rule_tree_json'];
                        this.ruleTreeData = data['policy_tree_json'];
                        this.blockTree(this.blockTreeData);
                        this.dataTree(this.dataTreeData);
                        this.policyTree(this.ruleTreeData);
                    }
                }
            });
    }
    public blockTree(data: any) {
        console.log('tree');
        $('#blockTree').jstree({
            'core': {
                'check_callback': true,
                'data': data,
                'li_attr': '<button>追加</button>'
            },
            'plugins': ['dnd', 'types'],
            'types' : {
                '#' : {
                      'ax_children' : 5
                    }
            }
        });
    }
    public dataTree(data: any) {
        $('#dataTree').jstree({
            'core': {
                'check_callback': true,
                'data': data,
            },
            'plugins': ['dnd'],
            'types' : {
                '#' : {
                      'ax_children' : 3
                    }
            }
        });
    }
    public policyTree(data: any) {
        $('#policyTree').jstree({
            'core': {
                'check_callback': true,
                'data': data,
            },
            'plugins': ['dnd', 'contextmenu']
        });
    }
    public getSelectedNode() {
        let wholedata = $('#dataTree').jstree(true);
        let tree = wholedata.get_container_ul ();
        console.log('whole tree', tree);
        $('#dataTree').on('changed.jstree', function (e, data) {
            console.log('data', data);
            if (data.selected.length) {
                $(data.selected).each(function (idx) {
                    let node = data.instance.get_node(data.selected[idx]);
                    console.log('selected', node.id);
                });
            }
        });
    }
    public moveNode() {
        $('#dataTree').on ('move_node.jstree', function (e, data) {
            console.log('ddd', data);
            if (data.rslt.ot !== data.rslt.rt) {
               console.log('Node was moved to a different tree-instance');
            } else {
               console.log('Node was moved inside the same tree-instance');
            }
         });
    }
    public deleteNode() {
        // $('#PolicyTree').jstree(true).delete_node([node.id]);
    }
}
