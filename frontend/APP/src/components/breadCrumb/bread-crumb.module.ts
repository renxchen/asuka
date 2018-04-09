import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { BreadCrumbComponent } from './bread-crumb';

@NgModule({
    declarations: [BreadCrumbComponent],
    imports: [RouterModule, CommonModule ],
    exports: [BreadCrumbComponent],
    providers: [],
})
export class BreadCrumbModule {}
