import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;


@Component({
    selector: 'test-telnet',
    templateUrl: 'testTelnet.component.html',
    styleUrls: []
})
export class TestTelnetComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';
    cliParameter1: string;
    cliParameter2: string;
    cliParameter3: string;
    cliParameter4: string;
    cliParameter5: string;
    cliParameter6: string;
    cliParameter7: string;
    cliParameter8: string;
    cliParameter9: string;
    cliParameter10: string;
    resultList: any = [];
    log: string;

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit(){
        this.httpClient.setUrl(this.apiPrefix);
    }

    ngAfterViewInit() {

    }

    tips(){
        alert("Help:\nFor multiple commands or error words, please use ',' to divide them.");
    }
    submitCli(){
        let _this = this;
        let url_cli = '/api_cli_collection_test/';
        console.log(url_cli);
        // let url_cli = 'http://10.79.148.107:1111/v1/api_cli_collection_test/';
        let data: any = {};
        data["commands"] = this.cliParameter1;
        data["start_default_commands"] = this.cliParameter2;
        data["end_default_commands"] = this.cliParameter3;
        data["prompt"] = this.cliParameter4;
        data["port"] = this.cliParameter5;
        data["fail_judges"] = this.cliParameter6;
        data["ip"] = this.cliParameter7;
        data["hostname"] = this.cliParameter8;
        data["expect"] = this.cliParameter9;
        data["timeout"] = this.cliParameter10;
        this.httpClient
            .toJson(this.httpClient.post(url_cli, data))
            .subscribe(res => {
                if (res['status']['status'].toString().toLowerCase() === 'true') {
                    _this.resultList = res['data']["data"];
                    _this.log = res["data"]["log"];
                } else {
                    alert(res['status']['message']);
                }
        });
    }
}