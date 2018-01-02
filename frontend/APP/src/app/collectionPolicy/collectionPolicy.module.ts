import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CPViewComponent } from './cPView.component';
import { CPGViewComponent } from './cPGView.component';
import { CLICPLoginComponent } from './cliCPLogin.component';
import { CLICPEditComponent } from './cliCPEdit.component';
import { SNMPCPLoginComponent } from './snmpCPLogin.component';
import { SNMPCPEditComponent } from './snmpCPEdit.component';

@NgModule({
    declarations: [CPViewComponent, CPGViewComponent,
                    CLICPLoginComponent, CLICPEditComponent,
                    SNMPCPLoginComponent, SNMPCPEditComponent],
    imports: [FormsModule, CommonModule ],
    exports: [],
    providers: [],
})
export class CPViewComponentModule {}
