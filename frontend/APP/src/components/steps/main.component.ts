import {
  Component,
  ElementRef,
  OnInit,
  AfterViewInit,
  ComponentFactoryResolver,
  Input,
  ComponentFactory,
  ComponentRef,
  ViewContainerRef,
  ReflectiveInjector,
  Injector,
  ViewChild,
  ApplicationRef,
  EmbeddedViewRef,
  OnDestroy
} from '@angular/core';
import { Observable } from 'rxjs/Rx';
import { StepsComponent } from './steps.component';
import { StepsSetting } from './stepSettings';


@Component({
  selector: '[cpu-wizzard]',
  template: ` <ng-content></ng-content>
    `
})

export class StepMainComponent implements OnInit, AfterViewInit, OnDestroy {

  @Input()
  componentRef: any;

  @Input() stepsSettings: StepsSetting[];

  @Input() direction?: 'vertical' | 'parallel';

  @Input() currentStep: number;

  @Input() title: string;

  @Input() parentScope: any;

  options: any = {};

  constructor(
    public element?: ElementRef,
    public componentFactoryResolver?: ComponentFactoryResolver,
    private injector?: Injector,
    private appRef?: ApplicationRef
  ) {
  }

  public ngOnInit() { }

  public ngAfterViewInit() {
    this.element.nativeElement.href = 'javaScript:void(0)';
  }


  public getOptions() {
    this.options['stepsSettings'] = this.stepsSettings;
    this.options['direction'] = 'parallel';
    this.options['currentStep'] = this.currentStep;
    this.options['title'] = this.title;
    this.options['parentScope'] = this.parentScope;

  }

  public showWizzard() {
    this.getOptions();
    console.log('this.opyions', this.options);
    const resolvedInputs = ReflectiveInjector.resolve([{ provide: 'option', useValue: this.options },
    { provide: 'mainIns', useValue: this }]);
    const injector = ReflectiveInjector.fromResolvedProviders(resolvedInputs, this.injector);
    let component: any;
    component = this.componentFactoryResolver.resolveComponentFactory(StepsComponent).create(injector);
    this.appRef.attachView(component.hostView);
    const domElem = (component.hostView as EmbeddedViewRef<any>)
      .rootNodes[0] as HTMLElement;
    document.body.appendChild(domElem);
    this.componentRef = component;
    return component;
  }


  public ngOnDestroy(): void { }

  public close() {
    this.componentRef.destroy();
  }

}
