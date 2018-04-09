import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login.component';
import { HClientModule } from '../../components/utils/httpClient.module';
import { SharedModule } from '../sharedModule/shared.module';

@NgModule({
  imports: [FormsModule, HClientModule, SharedModule],
  exports: [],
  declarations: [LoginComponent],
  entryComponents: []
})
export class LoginComponentModule { }
