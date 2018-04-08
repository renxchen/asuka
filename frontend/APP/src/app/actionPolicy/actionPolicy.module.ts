import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BsDatepickerModule, TimepickerModule } from 'ngx-bootstrap';
import { ActionPolicyViewComponent } from './actionPolicyView.component';
import { ActionPolicyLoginComponent } from './actionPolicyLogin.component';
import { DataTableViewComponent} from './dataTableView.component';
import { DataTableLoginComponent } from './dataTableLogin.component';
import { DataTableDetailComponent } from './dataTableDetail.component';
import { ActionPolicyHistoryComponent } from './actionPolicyHistory.component';
import { StepsModule } from '../../components/steps/steps.module';

@NgModule({
    declarations: [
        ActionPolicyViewComponent,
        ActionPolicyLoginComponent,
        DataTableViewComponent,
        DataTableLoginComponent,
        DataTableDetailComponent,
        ActionPolicyHistoryComponent,
    ],
    imports: [
        CommonModule,
        FormsModule,
        StepsModule,
        BsDatepickerModule.forRoot(),
        TimepickerModule.forRoot(),
    ],
    exports: [],
    providers: [],
})
export class ActionPolicyComponentModule { }
