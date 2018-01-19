import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SharedModule } from '../sharedModule/shared.module';
import { CPViewComponent } from './cPView.component';
import { CPGViewComponent } from './cPGView.component';
import { CLICPLoginComponent } from './cliCPLogin.component';
import { CLICPEditComponent } from './cliCPEdit.component';
import { CLICPDetailComponent } from './cliCPDetail.component';
import { CLIBlockComponent } from './cliBlock.component';
import { SNMPCPLoginComponent } from './snmpCPLogin.component';
import { SNMPCPDetailComponent } from './snmpCPDetail.component';
import { SNMPCPEditComponent } from './snmpCPEdit.component';

@NgModule({
    declarations: [CPViewComponent, CPGViewComponent,
                    CLICPLoginComponent, CLICPEditComponent,
                    CLICPDetailComponent, CLIBlockComponent,
                    SNMPCPLoginComponent, SNMPCPDetailComponent,
                    SNMPCPEditComponent],
    imports: [FormsModule, CommonModule, SharedModule],
    exports: [],
    providers: [],
})
export class CPViewComponentModule {}
