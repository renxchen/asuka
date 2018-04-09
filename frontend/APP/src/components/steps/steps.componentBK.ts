import {
    Component,
    OnInit,
    Input,
    ComponentFactory,
    AfterViewInit,
    ViewChild,
    ViewContainerRef,
    ReflectiveInjector,
    ComponentFactoryResolver,
    ElementRef,
    Injector
} from '@angular/core';
import * as _ from 'lodash';
import { TimelineLite, Linear } from 'gsap';

interface StepsSetting {
    step: Component;
    /**
     * ['inactive step icon', 'active step icon']
     */
    icons?: string[];
    title: string;
    buttons?: string[];
    desc?: string;
}

@Component({
    selector: 'cpu-steps',
    templateUrl: './steps.component.template.html',
    styleUrls: ['./steps.component.style.less']
})

export class StepsComponent implements OnInit, AfterViewInit {

    @Input() stepsSettings: StepsSetting[];

    @Input() direction: 'vertical' | 'parallel';

    @Input() currentStep: number;

    @Input() title: string;

    @Input() parentScope: any;

    @ViewChild('stepsContainer', { read: ViewContainerRef })
    stepsContainerRef: ViewContainerRef;

    componentsInstance: any[] = [];

    constructor(private injector: Injector,
        private resolver: ComponentFactoryResolver,
        private viewRef: ViewContainerRef,
        private elementRef: ElementRef) { }

    ngOnInit() {
        const modalDialog: HTMLElement[] =
            this.elementRef.nativeElement.querySelectorAll('div.modal-dialog');
        const tl = new TimelineLite();
        tl.
        to(modalDialog, 0.3, {rotationY: 30, ease: Linear.easeIn}).
        to(modalDialog, 0.3, {rotationY: -60, ease: Linear.easeIn}).
        to(modalDialog, 0.3, {rotationY: 0, ease: Linear.easeIn});
        this.initSteps();
    }

    private initSteps() {
        _.each(this.stepsSettings, (stepSetting: StepsSetting) => {
            const component: any = this.createComponent(stepSetting.step);
            this.componentsInstance.push(component.instance);
            component.instance.hide();
            this.stepsContainerRef.insert(component.hostView);
        });
        this.showStep(this.currentStep);
    }

    public showStep(step?: number) {
        step = _.isInteger(step) ? step : 0;
        if (_.isInteger(step)) {
            this.componentsInstance.slice(step, step + 1).pop().show();
        }
    }

    private createComponent(componentFactory: any) {
        const resolvedInputs = ReflectiveInjector.resolve([{ provide: 'parentScope', useValue: this.parentScope }]);

        const injector = ReflectiveInjector.fromResolvedProviders(resolvedInputs, this.injector);

        const component = this.resolver.resolveComponentFactory(componentFactory).create(injector);

        return component;
    }

    ngAfterViewInit() { }

    public hideAllSteps() {
        _.each(this.componentsInstance, (stepInstance: any) => {
            stepInstance.hide();
        });
    }

    public previous() {
        if (this.currentStep - 1 >= 0) {
            this.currentStep--;
        } else {
            return false;
        }
        this.hideAllSteps();
        this.showStep(this.currentStep);
    }

    public next() {
        if (this.currentStep + 1 <= this.componentsInstance.length - 1) {
            this.currentStep++;
        } else {
            return false;
        }
        this.hideAllSteps();
        this.showStep(this.currentStep);
    }

    public close() {
        this.viewRef.
            element.
            nativeElement.
            parentElement.
            removeChild(this.elementRef.nativeElement);
    }

}
