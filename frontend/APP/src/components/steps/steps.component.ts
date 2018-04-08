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
import { StepsSetting } from './stepSettings';


@Component({
  selector: 'cpu-steps',
  templateUrl: './steps.component.template.html',
  styleUrls: ['./steps.component.style.less']
})

export class StepsComponent implements OnInit, AfterViewInit {

  stepsSettings: StepsSetting[];

  direction: 'vertical' | 'parallel';

  currentStep: number;

  title: string;

  parentScope: any;

  mainInstance: any;


  @ViewChild('stepsContainer', { read: ViewContainerRef })
  stepsContainerRef: ViewContainerRef;

  componentsInstance: any[] = [];

  constructor(private injector: Injector,
    private resolver: ComponentFactoryResolver,
    private viewRef: ViewContainerRef,
    private elementRef: ElementRef) { }

  ngOnInit() {
    this.showSteps();
  }

  public showSteps() {
    const _t: any = this;
    const option = this.injector.get('option');
    this.mainInstance = this.injector.get('mainIns');
    this.direction = option['direction'] ? option['direction'] : 'parallel';
    this.stepsSettings = option['stepsSettings'];
    this.currentStep = option['currentStep'] ? option['currentStep'] : 0;
    this.title = option['title'];
    this.parentScope = option['parentScope'];
    const modalDialog: HTMLElement[] =
      this.elementRef.nativeElement.querySelectorAll('div.modal-dialog');
    const tl = new TimelineLite();
    tl.
      to(modalDialog, 0.3, { rotationY: 30, ease: Linear.easeIn }).
      to(modalDialog, 0.3, { rotationY: -60, ease: Linear.easeIn }).
      to(modalDialog, 0.3, { rotationY: 0, ease: Linear.easeIn });
    // this.initSteps();
    _t.initSteps();
  }

  private initSteps() {

    _.each(this.stepsSettings, (stepSetting: StepsSetting) => {
      const component: any = this.createComponent(stepSetting.step);
      this.componentsInstance.push(component.instance);
      // console.log('component', component);
      this.stepsContainerRef.insert(component.hostView);
      component.instance.hide();
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
    console.log('in close');
    this.mainInstance.close();
  }
}
