import { RouterModule, Routes } from '@angular/router';
import { ModalComponent } from '../components/modal/modal.component';

// login
import { LoginComponent } from './login/login.component';
// index
import { IndexComponent } from './index/index.component';
// collection policy
import { CPViewComponent } from './collectionPolicy/cPView.component';
import { CLICPLoginComponent } from './collectionPolicy/cliCPLogin.component';
import { CLICPEditComponent } from './collectionPolicy/cliCPEdit.component';
import { CLICPEditPopComponent } from './collectionPolicy/cliCPEditPop.component';
import { CLICPDetailComponent } from './collectionPolicy/cliCPDetail.component';
import { CLIBlockComponent } from './collectionPolicy/cliBlock.component';
import { CLIDataComponent } from './collectionPolicy/cliData.component';
import { SNMPCPLoginComponent } from './collectionPolicy/snmpCPLogin.component';
import { SNMPCPDetailComponent } from './collectionPolicy/snmpCPDetail.component';
import { SNMPCPEditComponent } from './collectionPolicy/snmpCPEdit.component';
import { CPGViewComponent } from './collectionPolicy/cPGView.component';
import { CPGLoginComponent } from './collectionPolicy/cPGLogin.component';
import { CPGDetailComponent } from './collectionPolicy/cPGDetail.component';
import { CPGEditComponent } from './collectionPolicy/cPGEdit.component';
import { CPGActionComponent } from './collectionPolicy/cPGAction.component';

// data collection
import { DataCollectionViewComponent } from './dataCollection/dataCollectionView.component';
import { PoliciesPerDeviceComponent } from './dataCollection/policiesPerDevice.component';
import { DevicesPerPolicyComponent } from './dataCollection/devicesPerPolicy.component';
import { DataCollectionLoginComponent } from './dataCollection/dataCollectionLogin.component';

import { ActionPolicyViewComponent } from './actionPolicy/actionPolicyView.component';
import { ActionPolicyLoginComponent } from './actionPolicy/actionPolicyLogin.component';
import { DataTableViewComponent } from './actionPolicy/dataTableView.component';
import { ActionPolicyHistoryComponent } from './actionPolicy/actionPolicyHistory.component';
import { DataTableLoginComponent } from './actionPolicy/dataTableLogin.component';

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
          // collection policy
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
            path: 'cliCPEdit',
            component: CLICPEditComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'CLIコレクションポリシー：ツリー構成'
            }
          },
          {
            path: 'cliCPDetail',
            component: CLICPDetailComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'CLIコレクションポリシー確認'
            }
          },
          {
            path: 'snmpCPLogin',
            component: SNMPCPLoginComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'SNMPコレクションポリシー登録'
            }
          },
          {
            path: 'snmpCPDetail',
            component: SNMPCPDetailComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'SNMPコレクションポリシー：確認'
            }
          },
          {
            path: 'snmpCPEdit',
            component: SNMPCPEditComponent,
            data: {
              parentTitle: 'コレクションポリシー',
              title: 'SNMPコレクションポリシー：編集'
            }
          },
          // data collection
          {
            path: 'dataCollectionView',
            component: DataCollectionViewComponent,
            data: {
              parentTitle: 'データ取得',
              title: 'データ取得一覧'
            }
          },
          {
            path: 'policiesPerDevice',
            component: PoliciesPerDeviceComponent,
            data: {
              parentTitle: 'データ取得',
              title: 'デバイス毎のデータ収集中の項目出力機能'
            }
          },
          {
            path: 'devicesPerPolicy',
            component: DevicesPerPolicyComponent,
            data: {
              parentTitle: 'データ取得',
              title: 'コレクションポリシー毎のデバイス一覧出力機能'
            }
          },
          {
            path: 'dataTableView',
            component: DataTableViewComponent,
            data: {
              parentTitle: 'アクションポリシー',
              title: 'テーブル一覧'
            }
          },
          {
            path: 'actionPolicyView',
            component: ActionPolicyViewComponent,
            data: {
              parentTitle: 'アクションポリシー',
              title: 'アクションポリシー一覧'
            }
          },
          {
            path: 'actionPolicyHistory',
            component: ActionPolicyHistoryComponent,
            data: {
              parentTitle: 'アクションポリシー',
              title: 'アクション実行履歴'
            }
          }
        ]
    }
];
export const appRouting = RouterModule.forRoot(routes);
export const entryComponentList: any[] = [
ModalComponent,
    // collection policy
    CLIBlockComponent,
    CLIDataComponent,
    CLICPEditPopComponent,
    CPGLoginComponent,
    CPGDetailComponent,
    CPGEditComponent,
    CPGActionComponent,
    // data
    DataCollectionLoginComponent,
    DataTableLoginComponent,
    ActionPolicyLoginComponent
];
