import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProcessbarComponent } from './processbar.component';

@NgModule({
    declarations: [ProcessbarComponent],
    imports: [ CommonModule ],
    exports: [ProcessbarComponent],
    providers: []
})
export class ProcessbarModule {}
