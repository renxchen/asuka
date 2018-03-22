
import {
    Component,
    OnInit,
    ComponentFactoryResolver,
    Injector,
    ReflectiveInjector,
    ElementRef,
    AfterViewInit,
    ViewChild
} from '@angular/core';
import { StepComponent } from '../../components/steps/step.component';
import { StepMainComponent } from '../../components/steps/main.component';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { DataTableLoginComponent } from './dataTableLogin.component';
import { DataTableDetailComponent } from './dataTableDetail.component';
import { Validator } from '../../components/validation/validation';
declare var $: any;
import * as _ from 'lodash';
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Rx';
@Component({
    templateUrl: './firstStep.component.html'
})
export class FirstStepComponent extends StepComponent implements OnInit, AfterViewInit {
    public keyUp = new Subject<any>();
    tableName: any;
    tableNameNotNull: Boolean = true;
    tableNameFlg: Boolean = true;
    tableNameUnq: Boolean = true;
    parentScope: any;
    nextStepFlg: Boolean;
    apiPrefix: any;
    constructor(
        injector: Injector,
        element: ElementRef,
        public httpClient: HttpClientComponent) {
        super(injector, element);
        const subscription = this.keyUp
            .map(event => event.target.value)
            .debounceTime(1000)
            .distinctUntilChanged()
            .flatMap(search => Observable.of(search).delay(500))
            .subscribe((data) => {
                console.log('validation', data);
                console.log('parentScope', this.parentScope);
                if (data) {
                    // this.doCheck(data);
                    this.tableNameNotNull = true;
                    // this.tableNameFlg = Validator.

                } else {
                    this.tableNameNotNull = false;
                }
            });
    }
    ngOnInit() {
        // this.tableName = 123;
        console.log(1110);
    }
    ngAfterViewInit() { console.log(1111); }
    doCheck(data: any) {
        let tableInfo: any;
            tableInfo['name'] = data;
            this.apiPrefix = '/v1';
            let url = '/';
            this.httpClient.setUrl(this.apiPrefix);
            this
                .httpClient
                .toJson(this.httpClient.post(tableInfo, url))
                .subscribe(res => {
                    if (res['status']['status'] === 'True') {
                        this.parentScope.nextStepFlg = true;
                    } else {
                        this.nextStepFlg = false;
                    }
                });
        }
    }

@Component({
    template: `
        <div style="min-height: 225px;">
            Step2
        </div>
    `
})
export class SecondComponent extends StepComponent implements OnInit, AfterViewInit {
    secondStepFlg: Boolean;
    constructor(injector: Injector, element: ElementRef) {
        super(injector, element);
    }
    ngOnInit() {
        console.log(2220);
        // this.nextStep(false);
        // this.secondStepFlg = false;
    }
    ngAfterViewInit() { console.log(2221); }
}
@Component({
    template: `
        <div style="min-height: 225px;">
            Step3
        </div>
    `
})
export class ThirdStepComponent extends StepComponent implements OnInit, AfterViewInit {
    constructor(injector: Injector, element: ElementRef) {
        super(injector, element);
    }
    ngOnInit() {
        console.log(3330);
    }
    ngAfterViewInit() {
        console.log(3331);
    }
}

@Component({
    template: `
        <div style="min-height: 225px;">
            Step4
        </div>
    `
})
export class FourthStepComponent extends StepComponent implements OnInit, AfterViewInit {
    constructor(injector: Injector, element: ElementRef) {
        super(injector, element);
        this.parentScope.save = (() => {
            this.parentScope.savedCallMsg = 'Save buttons clicked.';
        });
    }
    ngOnInit() {
        console.log(4440);
    }
    ngAfterViewInit() {
        console.log(4441);
    }
}

@Component({
    selector: 'data-table-view',
    templateUrl: 'dataTableView.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class DataTableViewComponent implements OnInit, AfterViewInit {
    stepsSettings: any;
    stepTitle: String;
    direction: Number;
    currentStep: Number;
    parentScope: any;
    @ViewChild(StepMainComponent) stepIns: StepMainComponent;
    tableModel: any = [
        { label: 'No', hidden: true, name: 'table_id', index: 'table_id' },
        { label: 'テーブル名', name: 'name', width: 30, align: 'center' },
        { label: '概要', name: 'description', width: 45, align: 'center' },
        {
            label: 'アクション', name: 'action', width: 30, align: 'center', search: false,
            formatter: this.formatterButtons
        },
    ];

    testData: any = [
        { table_id: 10, name: 'data table 1', description: 'description of data table 1' },
        { table_id: 11, name: 'data table 2', description: 'description of data table 2' },
        { table_id: 12, name: 'data table 3', description: 'description of data table 3' },
    ];

    modalRef: BsModalRef;
    modalConfig = {
        animated: true,
        keyboard: true,
        backdrop: true,
        ignoreBackdropClick: true
    };

    constructor(
        private modalService: BsModalService,
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        private resolver: ComponentFactoryResolver,
        private injector: Injector
        // public bsModalRef: BsModalRef
    ) { }

    ngOnInit() {
        this.initStepSettings();
    }

    ngAfterViewInit() {
        this.drawDataTableTable();

    }

    formatterButtons(cellvalue, options, rowObject) {
        // let buttons = '';
        let buttons = '<button class="btn btn-xs btn-default showInfo" id="show_' + rowObject["table_id"] + '"><i class="fa fa-info-circle"></i> 表示</button>&nbsp;';
        buttons += '<button class="btn btn-xs btn-warning delete" id="delete_' + rowObject["table_id"] + '"><i class="fa fa-minus-square"></i> 削除</button>&nbsp;';
        buttons += '<button class="btn btn-xs btn-primary addAction" id="add_' + rowObject["table_id"] + '"><i class="fa fa-plus-square"></i> アクションポリシー追加</button>';
        return buttons
    }

    public drawDataTableTable() {
        let _this = this;
        $('#tableTable').jqGrid({
            // url: '/v1/api_data_collection/',
            // datatype: 'JSON',
            datatype: 'local',
            // mtype: 'get',
            colModel: _this.tableModel,
            // postData: { '': '' },
            data: _this.testData,
            // viewrecords: true,
            loadComplete: function () {
                _this.showDataTable();
                // _this.renderColor();
            },
            rowNum: 10,
            rowList: [10, 20, 30],
            autowidth: true,
            beforeSelectRow: function (rowid, e) { return false; },
            height: 230,
            pager: '#tablePager',
            // jsonReader: {
            //     root: 'data',
            //     page: 'current_page_num',
            //     total: 'num_page',
            //     records: 'total_num',
            //     userData: 'status',
            //     repeatitems: false,
            // },
        });
        $('#tableTable').jqGrid('filterToolbar', { defaultSearch: 'cn' });
    }
    // wizard test begin
    initStepSettings() {
        this.stepsSettings = [{
            'step': FirstStepComponent,
            'icons': ['./assets/image/success.png', './assets/image/success_active.png'],
            'title': 'step 1',
            // 'desc': '基本設定を入力してください.'
        }, {
            'step': SecondComponent,
            'icons': ['./assets/image/success.png', './assets/image/success_active.png'],
            'title': 'step 2',
            // 'desc': 'デバイスグループを選択してください.',
            'buttons': []
        },
        {
            'step': ThirdStepComponent,
            'icons': ['./assets/image/success.png', './assets/image/success_active.png'],
            'title': 'step 3',
            // 'desc': 'カラムを選択してください.',
            'buttons': []
        },
        {
            'step': FourthStepComponent,
            'icons': ['./assets/image/success.png', './assets/image/success_active.png'],
            'title': 'step 4',
            // 'desc': 'コレクションポリシーを選択してください.',
            'buttons': [
                { 'label': 'Save', 'callFunc': 'save' }
            ]
        }];
        this.stepTitle = 'テーブル登録';
        this.direction = 1;
        this.currentStep = 0;
        this.parentScope = this;
    }
    showDialog() {
        this.stepIns.showWizzard();
    }
    // wizard test end

    // newTable(){

    //     this.modalRef = this.modalService.show(DataTableLoginComponent, this.modalConfig);
    //     // init the title of modal
    //     this.modalRef.content.title = 'テーブル登録';

    // }

    public showDataTable() {
        let _this = this;
        $('.showInfo').click(function (event) {
            let id = $(event)[0].target.id;
            let tableId = id.split('_')[1];
            // open modal and init the title and id of modal
            _this.modalRef = _this.modalService.show(DataTableDetailComponent, _this.modalConfig);
            _this.modalRef.content.title = 'データ取得編集';
            _this.modalRef.content.id = tableId;
        });
    }
}
