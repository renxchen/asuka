import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataCollectionViewComponent } from './dataCollectionView.component';
import { DataCollectionLoginComponent } from './dataCollectionLogin.component';

@NgModule({
    declarations: [
        DataCollectionViewComponent,
        DataCollectionLoginComponent,
    ],
    imports: [ CommonModule ],
    exports: [],
    providers: [],
})
export class DataCollectionComponentModule {}
