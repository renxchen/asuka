import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { appRouting,  } from './app.router';
import { HttpModule, Http } from '@angular/http';

import { AppComponent } from './app.component';
import { HttpClientModule } from '../components/utils/httpClient.module';
import { BreadCrumbModule } from '../components/breadCrumb/bread-crumb.module';
import { HttpClientComponent } from '../components/utils/httpClient';
import { LoginComponentModule } from './login/login.module';
import { IndexComponentModule } from './index/index.module';
import { CPViewComponentModule } from './collectionPolicy/collectionPolicy.module';
import { DataCollectionViewComponentModule } from './dataCollection/dataCollection.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    appRouting,
    HttpClientModule,
    HttpModule,
    LoginComponentModule,
    IndexComponentModule,
    CPViewComponentModule,
    DataCollectionViewComponentModule,
    BreadCrumbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
