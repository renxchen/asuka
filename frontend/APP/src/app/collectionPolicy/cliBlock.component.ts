import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';

@Component({
    selector: 'cli-block',
    templateUrl: './cliBlock.component.html',
    styleUrls: ['./collectionPolicy.component.less']
})

export class CLIBlockComponent implements OnInit, AfterViewInit {
    actionType: any;
    ruleId: any;
    ruleType: any;
    name: any;
    desc: any;
    markString: any;
    keyStr: any;

    constructor(
        private httpClient: HttpClientComponent,
        private bsModalRef: BsModalRef) {

    }
    ngOnInit() {
        this.actionType = 'create';
    }
    ngAfterViewInit() {

    }
    public doCheck() { }
    public save() { }
}
