import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
@Component({
    selector: 'msg-modal',
    templateUrl: 'modal.html',

})
export class ModalComponent implements OnInit, AfterViewInit {
    modalMsg: any;
    closeMsg: any;
    constructor(
        private bsModalRef: BsModalRef
    ) { }
    ngOnInit() {

    }
    ngAfterViewInit() {
        setTimeout(() => {
        }, 0);
    }
}
