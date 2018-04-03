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

    cliParameter1: string;


    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
    ) {}

    ngOnInit(){
    }

    ngAfterViewInit() {

    }
    submitCli(){
        let url_cli = 'http://10.71.244.134:1111/v1/api_cli_collection_test/';
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
            data: {"device_info": this.cliParameter1}
            // data: {"device_info": eval("("+this.cliParameter1+")")}
          }).done(function (res) {
              console.log("done");
              console.log(res);
              $('#result1').html(res["data"]["data"]);
              $('#result2').html(res["data"]["log"]);

          });

        // $.ajax({
        //     "type" : 'post',
        //     "url" : url_cli,
        //     "dataType" : "json",
        //     "data" : {"device_info": this.cliParameter1},
        //     "success" : function(resp) {
        //         console.log("done");
        //         console.log(resp);
        //     },
        //     "error":function(emsg){
        //         //返回失败信息-----》emsg
        //     }
        // });

    }


}