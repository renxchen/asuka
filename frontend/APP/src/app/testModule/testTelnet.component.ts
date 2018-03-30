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
    snmpParameter1: string;


    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit(){
        // this.httpClient.setUrl(this.apiPrefix);
    }

    ngAfterViewInit() {

    }
    submitCli(){
        let url_cli = 'http://10.79.148.107:1111/v1/api_cli_collection_test/';


        // this.testTelnetService.sendRequest(eval("("+this.cliParameter1+")"))
        //       .subscribe(res => {
        //        console.log(res);
        //       });

        // console.log(eval(this.cliParameter1));
        // let cliInfo = [];
        // cliInfo["device_info"] = eval("("+this.cliParameter1+")");
        // console.log(this.cliParameter1);
        // console.log(eval("("+this.cliParameter1+")"));
        // this.httpClient.post(url_cli, eval("("+this.cliParameter1+")"))
        //     .subscribe(res => {
        //         if (res['status']['status'].toString().toLowerCase() === 'true') {
        //             if (res['status']['message'] == "Success") {
        //
        //
        //             }
        //         } else {
        //             alert(res['status']['message']);
        //         }
        // });
        // $('#result1').html(this.cliParameter1);
        $.ajax({
            url: url_cli,
            type: 'post',
            dataType: 'json',
            data: {'device_info': eval("("+this.cliParameter1+")")}
          }).done(function (res) {
              console.log(res);
              $('#result1').html(res["data"]["data"]);
              $('#result2').html(res["data"]["log"]);

          });



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