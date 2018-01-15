import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
// import { BsModalService } from 'ngx-bootstrap';
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
    name: any;
    desc: any;
    markString: any;
    keyStr: any;
    startLnNum: any;
    endLnNum: any;
    startMrkStr: any;
    endMrkStr: any;
    isInclude: any;
    isSerial: any;

    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef) {
    }
    ngOnInit() {
    }
    ngAfterViewInit() {
        setTimeout(() => {
            if (typeof (this.info) !== 'undefined') {
                console.log('infro', this.info);
                this.cpId = this.info['cpId'];
                this.ruleType = this.info['ruleType'];
                this.actionType = this.info['actionType'];
                if (this.info['actionType'] === 'edit') {
                    console.log('lslsl');
                    this.ruleId = this.info['ruleId'];
                    if (this.ruleType === 'block_rule_1') {
                        console.log('in');
                        this.name = 'test name';
                        this.desc = 'test desc';
                        this.markString = 'test mark_string';
                        this.keyStr = 'test key_str';
                        // blockRule1();
                    } else if (this.ruleType === 'block_rule_2') {
                        // blockRule2();
                    } else if (this.ruleType === 'block_rule_3') {
                        // blockRule3();
                    } else {
                        // blockRule4();
                    }
                    console.log('create', this.ruleType);
                    // call create
                }
            }
        }, 0);
    }
    public transIsSerial(serial: any) {
        return serial ? 0 : 1;
    }
    public transIsInclude(incl: any) {
        return incl ? 0 : 1;
    }
    public commInfo(ruleId: any) {
        this.apiPrefix = '/v1';
        let url = '/v1/api_policy_tree_rule/?rule_id=' + ruleId;
        this.httpClient.setUrl(this.apiPrefix);
        return this.httpClient.toJson(this.httpClient.get(url));
    }
    public getDataRule(ruleId: any) {
        this.commInfo(ruleId).subscribe(res => {
            if (res['status'] && res['status']['status'].toString().toLowerCase() === 'true') {
                if (res['data']) {
                    let data = res['data'];
                    this.name = data['name'];
                    this.desc = data['desc'];
                }
            }
        });
    }
    public doCheck() { }
    public save() { }
}
