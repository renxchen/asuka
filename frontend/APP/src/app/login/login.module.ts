import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login.component';
import { HttpClientModule } from '../../components/utils/httpClient.module';

@NgModule({
  imports: [FormsModule, HttpClientModule],
  exports: [LoginComponent],
  declarations: [LoginComponent],
  entryComponents: []
})
export class LoginComponentModule { }
