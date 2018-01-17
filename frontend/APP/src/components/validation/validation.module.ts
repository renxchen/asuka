import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Validator } from './validation';

@NgModule({
    declarations: [Validator],
    imports: [ CommonModule ],
    exports: [],
    providers: [Validator],
})
export class ValidationModule {}
