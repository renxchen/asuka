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
    }

    ngAfterViewInit() {

    }

    submitSnmp(){
        let url_snmp = "http://10.71.244.134:1111/v1/api_snmp_collection_test/";
        $.ajax({
            url: url_snmp,
            type: 'post',
            dataType: 'json',
            data: {
                "oids": this.snmpParameter7,
                "port": this.snmpParameter4,
                "snmp_version": this.snmpParameter6,
                "ip": this.snmpParameter1,
                "hostname": this.snmpParameter2,
                "community": this.snmpParameter5,
                "timeout": this.snmpParameter3

            }
          }).done(function (res) {
              console.log(res);
              $('#result1').html(res["data"]["data"][0]["output"][0]["value"]);
          });
    }


}