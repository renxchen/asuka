import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { LoginComponent } from './login.component';
import { HClientModule } from '../../components/utils/httpClient.module';

@NgModule({
  imports: [FormsModule, HClientModule],
  exports: [],
  declarations: [LoginComponent],
  entryComponents: []
})
export class LoginComponentModule { }
