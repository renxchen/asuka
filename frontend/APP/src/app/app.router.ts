import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { IndexComponent } from './index/index.component';
import { CPViewComponent } from './collectionPolicy/cPView.component';
import { CPGViewComponent } from './collectionPolicy/cPGView.component';
import { CLICPLoginComponent } from './collectionPolicy/cliCPLogin.component';
import { SNMPCPLoginComponent } from './collectionPolicy/snmpCPLogin.component';
const routes: Routes = [
    {
        path: '',
        redirectTo: localStorage.getItem('sessionTimeOut') !== '' ? 'login' : 'index',
        pathMatch: 'full'
    },
    {
        path: 'login',
        component: LoginComponent
    },
    {
        path: 'index',
        component: IndexComponent,
        children: [
          {
            path: '',
            component: CPViewComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'コレクションポリシー一覧',
            }
          },
          {
            path: 'cPView',
            component: CPViewComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'コレクションポリシー一覧',
            }
          },
          {
            path: 'cPGView',
            component: CPGViewComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'コレクションポリシーグループ一覧'
            }
          },
          {
            path: 'cliCPLogin',
            component: CLICPLoginComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'CLIコレクションポリシー登録'
            }
          },
          {
            path: 'snmpCPLogin',
            component: SNMPCPLoginComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'SNMPコレクションポリシー登録'
            }
          }
        ]
    }
];
export const appRouting = RouterModule.forRoot(routes);
