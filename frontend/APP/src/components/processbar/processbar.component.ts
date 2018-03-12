import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
@Component({
    selector: 'msg-modal',
    templateUrl: 'processbar.component.html',

})
export class ProcessbarComponent implements OnInit, AfterViewInit {
    message: any;
    constructor(
        private bsModalRef: BsModalRef
    ) { }
    ngOnInit() {
    }
    ngAfterViewInit() {

    }
    public closeAlertModal() {
        this.bsModalRef.hide();
    }
}
