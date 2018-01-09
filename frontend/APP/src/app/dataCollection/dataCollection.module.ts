import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BsDatepickerModule, TimepickerModule } from 'ngx-bootstrap';
import { DataCollectionViewComponent } from './dataCollectionView.component';
import { DataCollectionLoginComponent } from './dataCollectionLogin.component';

@NgModule({
    declarations: [
        DataCollectionViewComponent,
        DataCollectionLoginComponent,
    ],
    imports: [ CommonModule, FormsModule, BsDatepickerModule.forRoot(),TimepickerModule.forRoot(), ],
    exports: [],
    providers: [],
})
export class DataCollectionComponentModule {}
