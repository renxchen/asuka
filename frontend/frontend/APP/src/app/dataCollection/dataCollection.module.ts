import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BsDatepickerModule, TimepickerModule } from 'ngx-bootstrap';
import { DataCollectionViewComponent } from './dataCollectionView.component';
import { DataCollectionLoginComponent } from './dataCollectionLogin.component';
import { PoliciesPerDeviceComponent } from './policiesPerDevice.component';
import { DevicesPerPolicyComponent } from './devicesPerPolicy.component';
import { EmergencyStopComponent } from './emergencyStop.component';

@NgModule({
    declarations: [
        DataCollectionViewComponent,
        DataCollectionLoginComponent,
        PoliciesPerDeviceComponent,
        DevicesPerPolicyComponent,
        EmergencyStopComponent
    ],
    imports: [
        CommonModule,
        FormsModule,
        BsDatepickerModule.forRoot(),
        TimepickerModule.forRoot(),
    ],
    exports: [],
    providers: [],
})
export class DataCollectionComponentModule {}
