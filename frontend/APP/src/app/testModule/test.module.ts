import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TestTelnetComponent } from './testTelnet.component';
import { TestSnmpComponent } from './testSnmp.component';


@NgModule({
    declarations: [
        TestTelnetComponent,
        TestSnmpComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
    ],
    exports: [],
    providers: [],
})
export class TestComponentModule { }
