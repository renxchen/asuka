import { RouterModule, Routes } from '@angular/router';
import { ModalComponent } from '../components/modal/modal.component';
import { ProgressbarComponent } from '../components/processbar/processbar.component';

// login
import { LoginComponent } from './login/login.component';
// index
import { IndexComponent } from './index/index.component';
// device
import { DeviceGroupComponent } from './device/deviceGroup/deviceGroup.component';
import { GroupLoginComponent } from './device/deviceGroup/groupLogin.component';
import { GroupEditComponent } from './device/deviceGroup/groupEdit.component';
import { DeviceLoginComponent } from './device/deviceLogin.component';
import { DeviceErrorTableComponent } from './device/deviceErrorTable.component';

import { DeviceViewComponent } from './device/deviceView.component';
import { OstypeComponent } from './device/./ostype/ostype.component';
import { OstypeLoginComponent } from './device/./ostype/ostypeLogin.component';
import { OstypeEditComponent } from './device/./ostype/ostypeEdit.component';
// collection policy
import { CPViewComponent } from './collectionPolicy/cPView.component';
import { CLICPLoginComponent } from './collectionPolicy/cli/cliCPLogin.component';
import { CLICPEditComponent } from './collectionPolicy/cli/cliCPEdit.component';
import { CLICPEditPopComponent } from './collectionPolicy/cli/cliCPEditPop.component';
import { CLICPDetailComponent } from './collectionPolicy/cli/cliCPDetail.component';
import { CLIBlockComponent } from './collectionPolicy/cli/cliBlock.component';
import { CLIDataComponent } from './collectionPolicy/cli/cliData.component';

import { SNMPCPLoginComponent } from './collectionPolicy/snmp/snmpCPLogin.component';
import { SNMPCPDetailComponent } from './collectionPolicy/snmp/snmpCPDetail.component';
import { SNMPCPEditComponent } from './collectionPolicy/snmp/snmpCPEdit.component';

import { CPGViewComponent } from './collectionPolicy/cpg/cPGView.component';
import { CPGLoginComponent } from './collectionPolicy/cpg/cPGLogin.component';
import { CPGDetailComponent } from './collectionPolicy/cpg/cPGDetail.component';
import { CPGEditComponent } from './collectionPolicy/cpg/cPGEdit.component';

// data collection
import { DataCollectionViewComponent } from './dataCollection/dataCollectionView.component';
import { PoliciesPerDeviceComponent } from './dataCollection/policiesPerDevice.component';
import { DevicesPerPolicyComponent } from './dataCollection/devicesPerPolicy.component';
import { DataCollectionLoginComponent } from './dataCollection/dataCollectionLogin.component';

// action policy
import { ActionPolicyViewComponent } from './actionPolicy/actionPolicyView.component';
import { ActionPolicyLoginComponent } from './actionPolicy/actionPolicyLogin.component';
import {DataTableViewComponent} from './actionPolicy/dataTableView.component';
import { ActionPolicyHistoryComponent } from './actionPolicy/actionPolicyHistory.component';
import { DataTableLoginComponent } from './actionPolicy/dataTableLogin.component';
import { DataTableDetailComponent } from './actionPolicy/dataTableDetail.component';

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
                component: DeviceViewComponent,
                data: {
                    parentTitle: 'デバイス',
                    title: 'デバイス閲覧',
                }
            },
            // device
            {
                path: 'ostype',
                component: OstypeComponent,
                data: {
                    parentTitle: 'デバイス',
                    title: 'OS Type設定',
                }
            },
            {
                path: 'devicegroup',
                component: DeviceGroupComponent,
                data: {
                    parentTitle: 'デバイス',
                    title: 'デバイスグループ閲覧',
                }
            },
            {
                path: 'deviceview',
                component: DeviceViewComponent,
                data: {
                    parentTitle: 'デバイス',
                    title: 'デバイス閲覧',
                }
            },
            {
                path: 'devicelogin',
                component: DeviceLoginComponent,
                data: {
                    parentTitle: 'デバイス',
                    title: 'デバイス登録',
                }
            },
            // collection policy
            {
                path: 'cpview',
                component: CPViewComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'コレクションポリシー一覧',
                }
            },
            {
                path: 'cpgview',
                component: CPGViewComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'コレクションポリシーグループ一覧'
                }
            },
            {
                path: 'cpgdetail',
                component: CPGDetailComponent,
                data: {
                    parentTitle: 'コレクションポリシーグループ',
                    title: 'コレクションポリシーグループ確認'
                }
            },
            {
                path: 'cpgedit',
                component: CPGEditComponent,
                data: {
                    parentTitle: 'コレクションポリシーグループ',
                    title: 'コレクションポリシーグループ編集'
                }
            },
            {
                path: 'clicplogin',
                component: CLICPLoginComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'CLIコレクションポリシー登録'
                }
            },
            {
                path: 'clicpedit',
                component: CLICPEditComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'CLIコレクションポリシー：ツリー構成'
                }
            },
            {
                path: 'clicpdetail',
                component: CLICPDetailComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'CLIコレクションポリシー確認'
                }
            },
            {
                path: 'snmpcplogin',
                component: SNMPCPLoginComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'SNMPコレクションポリシー登録'
                }
            },
            {
                path: 'snmpcpdetail',
                component: SNMPCPDetailComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'SNMPコレクションポリシー：確認'
                }
            },
            {
                path: 'snmpcpedit',
                component: SNMPCPEditComponent,
                data: {
                    parentTitle: 'コレクションポリシー',
                    title: 'SNMPコレクションポリシー：編集'
                }
            },
            // data collection
            {
                path: 'datacollectionview',
                component: DataCollectionViewComponent,
                data: {
                    parentTitle: 'データ取得',
                    title: 'データ取得一覧'
                }
            },
            {
                path: 'policiesperdevice',
                component: PoliciesPerDeviceComponent,
                data: {
                    parentTitle: 'データ取得',
                    title: 'デバイス毎のデータ収集中の項目出力機能'
                }
            },
            {
                path: 'devicesperpolicy',
                component: DevicesPerPolicyComponent,
                data: {
                    parentTitle: 'データ取得',
                    title: 'コレクションポリシー毎のデバイス一覧出力機能'
                }
            },
            {
                path: 'datatableview',
                component: DataTableViewComponent,
                data: {
                    parentTitle: 'アクションポリシー',
                    title: 'テーブル一覧'
                }
            },
            {
                path: 'actionpolicyview',
                component: ActionPolicyViewComponent,
                data: {
                    parentTitle: 'アクションポリシー',
                    title: 'アクションポリシー一覧'
                }
            },
            {
                path: 'actionpolicyhistory',
                component: ActionPolicyHistoryComponent,
                data: {
                    parentTitle: 'アクションポリシー',
                    title: 'アクション実行履歴'
                }
            },
            //
            // data collection
            {
                path: 'datacollectionview',
                component: DataCollectionViewComponent,
                data: {
                    parentTitle: 'データ取得',
                    title: 'データ取得一覧'
                }
            },
            {
                path: 'policiesperdevice',
                component: PoliciesPerDeviceComponent,
                data: {
                    parentTitle: 'データ取得',
                    title: 'デバイス毎のデータ収集中の項目出力機能'
                }
            },
            {
                path: 'devicesperpolicy',
                component: DevicesPerPolicyComponent,
                data: {
                    parentTitle: 'データ取得',
                    title: 'コレクションポリシー毎のデバイス一覧出力機能'
                }
            },
            {
                path: 'datatableview',
                component: DataTableViewComponent,
                data: {
                    parentTitle: 'アクションポリシー',
                    title: 'テーブル一覧'
                }
            },
            {
                path: 'actionpolicyview',
                component: ActionPolicyViewComponent,
                data: {
                    parentTitle: 'アクションポリシー',
                    title: 'アクションポリシー一覧'
                }
            },
            {
                path: 'actionpolicylogin',
                component: ActionPolicyLoginComponent,
                data: {
                    parentTitle: 'アクションポリシー',
                    title: 'アクションポリシー編集'
                }
            },
            {
                path: 'actionpolicyhistory',
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
    ProgressbarComponent,
    // device
    GroupLoginComponent,
    GroupEditComponent,
    OstypeLoginComponent,
    OstypeEditComponent,
    DeviceErrorTableComponent,
    // collection policy
    CLIBlockComponent,
    CLIDataComponent,
    CLICPEditPopComponent,
    CPGLoginComponent,
    // data
    DataCollectionLoginComponent,
    DataTableLoginComponent,
    DataTableDetailComponent,
    // action policy
    ActionPolicyLoginComponent,
];
