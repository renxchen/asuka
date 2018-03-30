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
        let url_snmp = 'http://10.79.148.107:1111/v1/api_snmp_collection_test/';
        $.ajax({
            url: url_snmp,
            type: 'post',
            dataType: 'json',
            data: {'device_info': eval("("+this.snmpParameter1+")")}
          }).done(function (res) {
              console.log(res);
              $('#result3').html(res["data"]["data"]);
              $('#result4').html(res["data"]["log"]);

          });
    }


}