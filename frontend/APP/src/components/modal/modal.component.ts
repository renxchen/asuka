import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
declare var $: any;
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
        // setTimeout(() => {
        // }, 0);
    }
    public closeAlertModal() {
        this.bsModalRef.hide();
        $('body').removeClass('modal-open');
        $('body').css('padding-right', '0px');
    }
}
