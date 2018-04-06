import { Component, OnInit, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;


@Component({
    selector: 'test-snmp',
    templateUrl: 'testSnmp.component.html',
    styleUrls: []
})
export class TestSnmpComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';
    snmpParameter1: string;
    snmpParameter2: string;
    snmpParameter3: string;
    snmpParameter4: string;
    snmpParameter5: string;
    snmpParameter6: string;
    snmpParameter7: string;

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

    submitSnmp(){
        let url_snmp = "/api_snmp_collection_test/";
        let data: any = {};
        data["oids"] = this.snmpParameter7;
        data["port"] = this.snmpParameter4;
        data["snmp_version"] = this.snmpParameter6;
        data["ip"] = this.snmpParameter1;
        data["hostname"] = this.snmpParameter2;
        data["community"] = this.snmpParameter5;
        data["timeout"] = this.snmpParameter3;
        this.httpClient
            .toJson(this.httpClient.post(url_snmp, data))
            .subscribe(res => {
                if (res['status']['status'].toString().toLowerCase() === 'true') {
                    if (res['status']['message'] == "Success") {
                       console.log("done");
                       console.log(res);
                       $('#result1').html(res["data"]["data"][0]["output"][0]["value"]);
                    }
                } else {
                    alert(res['status']['message']);
                }
        });
        // $.ajax({
        //     url: url_snmp,
        //     type: 'post',
        //     dataType: 'json',
        //     data: {
        //         "oids": this.snmpParameter7,
        //         "port": this.snmpParameter4,
        //         "snmp_version": this.snmpParameter6,
        //         "ip": this.snmpParameter1,
        //         "hostname": this.snmpParameter2,
        //         "community": this.snmpParameter5,
        //         "timeout": this.snmpParameter3
        //
        //     }
        //   }).done(function (res) {
        //       console.log(res);
        //       $('#result1').html(res["data"]["data"][0]["output"][0]["value"]);
        //   });
    }


}