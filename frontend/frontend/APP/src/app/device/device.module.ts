import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ProgressbarModuleCustom } from '../../components/processbar/processbar.module';
import { DeviceGroupComponent } from './deviceGroup/deviceGroup.component';
import { GroupLoginComponent } from './deviceGroup/groupLogin.component';
import { GroupEditComponent } from './deviceGroup/groupEdit.component';
import { DeviceLoginComponent } from './deviceLogin.component';
import { DeviceErrorTableComponent } from './deviceErrorTable.component';
import { DeviceViewComponent } from './deviceView.component';
import { OstypeComponent } from './ostype/ostype.component';
import { OstypeLoginComponent } from './ostype/ostypeLogin.component';
import { OstypeEditComponent } from './ostype/ostypeEdit.component';

@NgModule({
    declarations:
        [
            DeviceGroupComponent, GroupLoginComponent,
            GroupEditComponent, DeviceLoginComponent,
            DeviceViewComponent, OstypeComponent,
            OstypeLoginComponent, OstypeEditComponent,
            DeviceErrorTableComponent
        ],
    imports: [CommonModule, FormsModule, ProgressbarModuleCustom],
    exports: [],
    providers: [],
})
export class DeviceModule { }
