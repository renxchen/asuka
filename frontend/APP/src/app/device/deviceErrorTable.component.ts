import { Component, OnInit, AfterViewInit, Input } from '@angular/core';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
@Component({
    selector: 'device-error-table',
    templateUrl: 'deviceErrorTable.component.html',

})
export class DeviceErrorTableComponent implements OnInit, AfterViewInit {
    data: any;
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
    }
}
