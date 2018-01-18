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
    name: any;
    osType: any;
    cliCommand: any;
    desc: any;
    policyTree: any;
    modalRef: BsModalRef;
    closeMsg: any;
    modalMsg: any;
    treeData: any = [
        {
            'text': 'test_1',
            'icon': 'fa fa-cubes fa-lg',
            'data': {
                'rule_id': '1',
                'rule_type': 'policy_rule',
            }
        },
        {
            'text': 'test_2',
            'icon': 'fa fa-cubes fa-lg',
            'data': {
                'rule_id': '2',
                'rule_type': 'policy_rule',
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
                        'rule_id': '6'
                    }
                }
            ]
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
                        this.name = _.get(data, 'name');
                        this.osType = _.get(data, 'ostype_name');
                        this.cliCommand = _.get(data, 'cli_command');
                        this.desc = _.get(data, 'desc');
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
        $('#policyTree').jstree({
            core: {
                check_callback: false,
                data: data
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
        this.router.navigate(['/index/cliCPEdit'], { queryParams: { 'id': this.cPId } });
        //         } else {
        //             // check this cp occupation, add 'occupation' feedback
        //             if (res['status']['message'] && ['status']['message'] === 'occupation') {
        //                 this.modalMsg = 'This collection policy is being occupied';
        //                 this.closeMsg = 'close';
        //                 this.showAlertModal(this.modalMsg, this.closeMsg);
        //             } else {
        //                 if (res['status'] && res['status']['message']) {
        //                     alert(res['status']['message']);
        //                 }
        //             }
        //         }
        //     });
    }
    public showAlertModal(modalMsg: any, closeMsg: any) {
        this.modalRef = this.modalService.show(ModalComponent);
        this.modalRef.content.modalMsg = modalMsg;
        this.modalRef.content.closeMsg = closeMsg;
    }
}
