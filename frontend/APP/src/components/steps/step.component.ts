import { Component, OnInit, Input, Injector, ElementRef } from '@angular/core';

@Component({
    selector: 'cpu-step',
    templateUrl: 'step.component.template.html',
    styleUrls: ['./step.component.style.less']
})

export class StepComponent implements OnInit {

    parentScope: any;

    constructor(private injector: Injector, public element: ElementRef) {
        this.parentScope = this.injector.get('parentScope');
    }

    ngOnInit() {

    }

    public hide() {
        this.element.nativeElement.style.display = 'none';
    }

    public show() {
        this.element.nativeElement.style.display = 'block';
    }
}
