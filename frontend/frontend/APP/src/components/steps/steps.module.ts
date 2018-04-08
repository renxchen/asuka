import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { importType } from '@angular/compiler/src/output/output_ast';

import { StepsComponent } from './steps.component';
import { StepComponent } from './step.component';
import { StepMainComponent } from './main.component';

@NgModule({
  imports: [FormsModule, CommonModule],
  exports: [StepMainComponent],
  declarations: [StepsComponent, StepComponent, StepMainComponent],
  entryComponents: [StepComponent, StepsComponent],
  providers: [],
})
export class StepsModule { }


