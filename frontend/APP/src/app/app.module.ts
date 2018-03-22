import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpModule, Http } from '@angular/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { appRouting, entryComponentList } from './app.router';
import { TranslateModule, TranslateLoader } from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { SharedModule } from './sharedModule/shared.module';
import { ModalModule, BsDatepickerModule, TimepickerModule} from 'ngx-bootstrap';
import { AppComponent } from './app.component';
import { HClientModule } from '../components/utils/httpClient.module';
import { StepsModule } from '../components/steps/steps.module';
import { ValidationModule } from '../components/validation/validation.module';
import { BreadCrumbModule } from '../components/breadCrumb/bread-crumb.module';
import { ModModule } from '../components/modal/modal.module';
import { ProcessbarModule } from '../components/processbar/processbar.module';
import { LoginComponentModule } from './login/login.module';
import { IndexComponentModule } from './index/index.module';
import { DeviceModule } from './device/device.module';
import { CPViewComponentModule } from './collectionPolicy/collectionPolicy.module';
import { DataCollectionComponentModule } from './dataCollection/dataCollection.module';
import { ActionPolicyComponentModule } from './actionPolicy/actionPolicy.module';

export function HttpLoaderFactory(http: HttpClient) {
    return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}
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
        TranslateModule.forRoot({
            loader: {
                provide: TranslateLoader,
                useFactory: (HttpLoaderFactory),
                deps: [HttpClient]
            }
        }),
        HttpModule,
        FormsModule,
        ReactiveFormsModule,
        appRouting,
        SharedModule,
        HClientModule,
        StepsModule,
        BreadCrumbModule,
        DeviceModule,
        CPViewComponentModule,
        LoginComponentModule,
        IndexComponentModule,
        DataCollectionComponentModule,
        ActionPolicyComponentModule,
        BreadCrumbModule,
        ModModule,
        ProcessbarModule
    ],
    providers: [],
    bootstrap: [AppComponent],
    entryComponents: [entryComponentList]
})

export class AppModule { }
