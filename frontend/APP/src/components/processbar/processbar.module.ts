import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProgressbarComponent } from './processbar.component';
import { ProgressbarModule } from 'ngx-bootstrap';
@NgModule({
    declarations: [ProgressbarComponent],
    imports: [CommonModule, ProgressbarModule.forRoot()],
    exports: [ProgressbarComponent],
    providers: []
})
export class ProgressbarModuleCustom { }
