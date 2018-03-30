import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TestTelnetComponent } from './testTelnet.component';


@NgModule({
    declarations: [
        TestTelnetComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
    ],
    exports: [],
    providers: [],
})
export class TestComponentModule { }
