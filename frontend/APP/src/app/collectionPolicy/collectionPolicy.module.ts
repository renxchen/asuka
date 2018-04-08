import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { CPViewComponent } from './cPView.component';
import { CLICPLoginComponent } from './cli/cliCPLogin.component';
import { CLICPEditComponent } from './cli/cliCPEdit.component';
import { CLICPEditPopComponent } from './cli/cliCPEditPop.component';
import { CLICPDetailComponent } from './cli/cliCPDetail.component';
import { CLIBlockComponent } from './cli/cliBlock.component';
import { CLIDataComponent } from './cli/cliData.component';
import { SNMPCPLoginComponent } from './snmp/snmpCPLogin.component';
import { SNMPCPDetailComponent } from './snmp/snmpCPDetail.component';
import { SNMPCPEditComponent } from './snmp/snmpCPEdit.component';
import { CPGViewComponent } from './cpg/cPGView.component';
import { CPGLoginComponent } from './cpg/cPGLogin.component';
import { CPGDetailComponent } from './cpg/cPGDetail.component';
import { CPGEditComponent } from './cpg/cPGEdit.component';

@NgModule({
    declarations: [CPViewComponent, CLICPLoginComponent,
        CLICPEditComponent, CLICPDetailComponent,
        CLIBlockComponent, CLICPEditPopComponent,
        CLIDataComponent, SNMPCPLoginComponent,
        SNMPCPDetailComponent, SNMPCPEditComponent,
        CPGViewComponent, CPGLoginComponent,
        CPGDetailComponent, CPGEditComponent
    ],
    imports: [FormsModule, CommonModule],
    exports: [],
    providers: [],
})
export class CPViewComponentModule { }
