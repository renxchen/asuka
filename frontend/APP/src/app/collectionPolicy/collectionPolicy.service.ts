import { Injectable, ViewContainerRef } from '@angular/core';
import { Observable } from 'rxjs/Rx';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
@Injectable()
export class CollectionPolicyService {
    private blockTree = new BehaviorSubject<any>('');
    blockTree$ = this.blockTree.asObservable();

    private dataTree = new BehaviorSubject<any>('');
    dataTree$ = this.blockTree.asObservable();

    private cPName = new BehaviorSubject<any>('');
    cPName$ = this.cPName.asObservable();

    public refreshBlockTree(blockInfo: any) {
        console.log('block', blockInfo);
        this.blockTree.next(blockInfo);
    }
    public refreshDataTree(dataInfo: any) {
        console.log('data', this.dataTree$);
        this.dataTree.next(dataInfo);
        console.log('zoumeizoua');
    }

    public refreshcPName(cPName: any) {
        console.log('cPName', cPName);
        this.blockTree.next(cPName);
    }
}
