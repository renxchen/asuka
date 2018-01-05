import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { HttpModule, Http } from '@angular/http';
import { FormsModule } from '@angular/forms';
import { appRouting } from './app.router';
import { TranslateModule, TranslateLoader} from '@ngx-translate/core';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { SharedModule } from './sharedModule/shared.module';
import { ModalModule } from 'ngx-bootstrap';

import { AppComponent } from './app.component';
import { HClientModule } from '../components/utils/httpClient.module';
import { BreadCrumbModule } from '../components/breadCrumb/bread-crumb.module';
import { LoginComponentModule } from './login/login.module';
import { IndexComponentModule } from './index/index.module';
import { CPViewComponentModule } from './collectionPolicy/collectionPolicy.module';
import { DataCollectionComponentModule } from './dataCollection/dataCollection.module';
import { DataCollectionLoginComponent } from './dataCollection/dataCollectionLogin.component';


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
    TranslateModule.forRoot({
      loader: {
          provide: TranslateLoader,
          useFactory: (HttpLoaderFactory),
          deps: [HttpClient]
      }
    }),
    HttpModule,
    FormsModule,
    appRouting,
    SharedModule,
    HClientModule,
    BreadCrumbModule,
    LoginComponentModule,
    IndexComponentModule,
    CPViewComponentModule,
    LoginComponentModule,
    IndexComponentModule,
    CPViewComponentModule,
    DataCollectionComponentModule,
    BreadCrumbModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [DataCollectionLoginComponent]
})

export class AppModule { }
