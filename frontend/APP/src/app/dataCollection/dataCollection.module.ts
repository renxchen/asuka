import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DataCollectionViewComponent } from './dataCollectionView.component';
import { DataCollectionLoginComponent } from './dataCollectionLogin.component';

@NgModule({
    declarations: [
        DataCollectionViewComponent,
        DataCollectionLoginComponent,
    ],
    imports: [ CommonModule, FormsModule ],
    exports: [],
    providers: [],
})
export class DataCollectionComponentModule {}
