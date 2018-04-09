import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotFoundComponent } from './notFound.component';
import { RouterModule, Routes } from '@angular/router';
@NgModule({
    declarations: [NotFoundComponent],
    imports: [CommonModule, RouterModule],
    exports: [NotFoundComponent],
    providers: [],
})
export class NotFoundModule { }
