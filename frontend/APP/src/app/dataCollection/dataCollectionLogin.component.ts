import { Component, OnInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';

@Component({
    selector: 'modal-content',
    templateUrl: 'dataCollectionLogin.component.html',
    styleUrls: ['dataCollection.component.less']
})

export class DataCollectionLoginComponent implements OnInit {
    title: string;
    id: number = 0;
    // modalTitle:string;

    constructor(public bsModalRef: BsModalRef) {}

    ngOnInit() {
        // this.modalTitle = 'data';
        // this.cpType = 'cli';
        // this.modalRef = this.modalService;
        // this.drawCPTable();
    }


}
