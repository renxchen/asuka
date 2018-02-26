import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { DeviceGroupComponent } from './deviceGroup/deviceGroup.component';
import { GroupLoginComponent } from './deviceGroup/groupLogin.component';
import { GroupEditComponent } from './deviceGroup/groupEdit.component';

@NgModule({
    declarations: [DeviceGroupComponent, GroupLoginComponent, GroupEditComponent],
    imports: [CommonModule, FormsModule],
    exports: [],
    providers: [],
})
export class DeviceModule { }
