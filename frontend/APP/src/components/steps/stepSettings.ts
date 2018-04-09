import {Component} from '@angular/core';


export interface StepsSetting {
  step: Component;
  /**
   * ['inactive step icon', 'active step icon']
   */
  icons?: string[];
  title: string;
  buttons?: string[];
  desc?: string;
}
