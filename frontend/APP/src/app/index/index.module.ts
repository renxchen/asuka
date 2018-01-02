import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { BreadCrumbModule } from '../../components/breadCrumb/bread-crumb.module';
import { IndexComponent} from './index.component';
import { IndexService } from './index.service';

@NgModule({
    declarations: [IndexComponent],
    imports: [ RouterModule, CommonModule, BreadCrumbModule ],
    exports: [],
    providers: [IndexService],
})
export class IndexComponentModule {}
