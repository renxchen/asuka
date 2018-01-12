import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
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
    constructor(
        private httpClient: HttpClientComponent,
        private activatedRoute: ActivatedRoute,
        private router: Router) {
        let cPIdTmp = this.activatedRoute.snapshot.queryParams['id'];
        if (cPIdTmp) {
            this.cPId = cPIdTmp;
            this.getCPDetailInfo(this.cPId);
        }
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
    }
    public getCPDetailInfo(id: any) {
        this.apiPrefix = '/v1';
        let url = 'api_collection_policy?id=' + id;
        this.httpClient.setUrl(url);
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['data']) {
                        let data = res['data'];
                        this.name = data['name'];
                        this.osType = data['ostype_name'];
                        this.cliCommand = data['cli_command'];
                        this.desc = data['desc'];
                        this.policyTree = data['policy_tree_json'];
                        this.drawPlyTree(this.policyTree);
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
        this.router.navigate(['/index/cliCPEdit'], {queryParams: {'id' : this.cPId }});
    }
}
