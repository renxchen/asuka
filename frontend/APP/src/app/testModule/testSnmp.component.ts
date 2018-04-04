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


    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit(){
    }

    ngAfterViewInit() {

    }

    // http://10.79.148.107:1111/v1/api_snmp_collection_test/
    // ?ip=10.71.244.135&community=cisco
    // &oids=['1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.2.0','1.3.6.1.2.1.10.30.5']

    submitSnmp(){
        let url_snmp = "http://10.71.244.134:1111/v1/api_snmp_collection_test/?ip="+this.snmpParameter1+"&community="
            +this.snmpParameter2+"&oids=['"+this.snmpParameter3+"']";
        console.log(url_snmp);
        $.ajax({
            url: url_snmp,
            type: 'get',
            // dataType: 'json',
            // data: {'device_info': eval("("+this.snmpParameter1+")")}
          }).done(function (res) {
              console.log(res);
              $('#result1').html(res["data"]["data"][0]["output"][0]["value"]);
          });
    }


}