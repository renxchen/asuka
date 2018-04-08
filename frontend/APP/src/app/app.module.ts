import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpModule, Http } from '@angular/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { appRouting, entryComponentList } from './app.router';
import { ModalModule, BsDatepickerModule, TimepickerModule } from 'ngx-bootstrap';
import { AppComponent } from './app.component';
import { HClientModule } from '../components/utils/httpClient.module';
import { StepsModule } from '../components/steps/steps.module';
import { ValidationModule } from '../components/validation/validation.module';
import { BreadCrumbModule } from '../components/breadCrumb/bread-crumb.module';
import { ModModule } from '../components/modal/modal.module';
import { LoginComponentModule } from './login/login.module';
import { NotFoundModule } from '../components/404/notFound.module';
import { IndexComponentModule } from './index/index.module';
import { DeviceModule } from './device/device.module';
import { CPViewComponentModule } from './collectionPolicy/collectionPolicy.module';
import { DataCollectionComponentModule } from './dataCollection/dataCollection.module';
import { ActionPolicyComponentModule } from './actionPolicy/actionPolicy.module';
import { TestComponentModule } from './testModule/test.module';

@NgModule({
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        HttpClientModule,
        ModalModule.forRoot(),
        BsDatepickerModule.forRoot(),
        TimepickerModule.forRoot(),
        HttpModule,
        FormsModule,
        ReactiveFormsModule,
        appRouting,
        HClientModule,
        StepsModule,
        BreadCrumbModule,
        DeviceModule,
        CPViewComponentModule,
        LoginComponentModule,
        NotFoundModule,
        IndexComponentModule,
        DataCollectionComponentModule,
        ActionPolicyComponentModule,
        BreadCrumbModule,
        ModModule,
        TestComponentModule,
    ],
    providers: [],
    bootstrap: [AppComponent],
    entryComponents: [entryComponentList]
})

export class AppModule { }
