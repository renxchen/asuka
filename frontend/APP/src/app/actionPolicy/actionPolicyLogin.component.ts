import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
    selector: 'action-policy-login',
    templateUrl: 'actionPolicyLogin.component.html',
    styleUrls: ['actionPolicy.component.less']
})
export class ActionPolicyLoginComponent implements OnInit, AfterViewInit {

    apiPrefix: any = '/v1';
    title: string;

    modalRef: BsModalRef;
    modalConfig = {
        animated: true,
        keyboard: true,
        backdrop: true,
        ignoreBackdropClick: true
    };

    isNew: boolean = true;

    selectingColumn:string;
    columnModel: any = [
        {label: 'table_id', hidden: true, name: 'table_id'},
        {label: 'policy_id', hidden: true, name: 'policy_id'},
        {label: 'コレクションポリシー名',  name: 'policy_name', width: 30, align: 'center', sortable:false},
        {label: 'テーブル名',  name: 'name', width: 30, align: 'center', sortable:false},
        {label: '概要', name: 'desc', width: 30, align: 'center', sortable:false},

    ];
    columnSelected: number;

    historyDataModel: any = [
        {label: 'デバイス名',  name: 'hostname', width: 30, align: 'center', sortable:false},
        {label: 'Time Stamp',  name: 'date', width: 30, align: 'center', sortable:false},
        {label: 'Path',  name: 'path', width: 30, align: 'center', sortable:false},
        {label: 'value', name: 'value', width: 30, align: 'center', sortable:false},

    ];

    editingAction: string;
    actionSelectTitle: string;
    actionSelectedType: number = 0;
    snmpVersion: number = 1;
    snmpCommunity: string;
    snmpAgent: string;
    snmpIp: string;
    snmpOid: string;
    snmpMessage: string;
    script: string;
    rundeckIp: string;
    rundeckUser: string;
    rundeckPassword: string;
    rundeckCommand: string;

    actionPolicyName: string;
    actionPolicyDescription: string;

    triggerType: number = 2;
    triggerTypes: any = [{id: 2, value: '文字列比較'}, {id: 1, value: '数値比較'}, {id: 0, value: '演算比較'}, {id: 3, value: '取得失敗'}];
    conditionList: any = [{id: 4, value: '未満'}, {id: 0, value: '以下'}, {id: 1, value: '等しい'}, {id: 2, value: '以上'}, {id: 5, value: 'より大きい'}, {id: 3, value: '異なる'}];
    continuousOverList: any = [{id: 1, value: '1回'}, {id: 2, value: '2回'}, {id: 3, value: '3回'}, {id: 4, value: '4回'}, {id: 5, value: '5回'}];
    actionTypes: any = [{id: 0, value: 'SNMP Trap送信'}, {id: 1, value: 'スクリプト実行'}, {id: 2, value: '自動化シナリオ実行'}];

    columnOne: string;
    columnA: string;
    columnB: string;

    critical_value: string = "";
    major_value: string = "";
    minor_value: string = "";

    critical_string_condition: number = 1;
    major_string_condition: number = 1;
    minor_string_condition: number = 1;

    critical_number_condition: number = 4;
    major_number_condition: number = 4;
    minor_number_condition: number = 4;

    critical_function: string = "";
    major_function: string = "";
    minor_function: string = "";

    critical_continuous_condition: number = 1;
    major_continuous_condition: number = 1;
    minor_continuous_condition: number = 1;

    criticalActionA: string = "Please select action 1";
    criticalActionB: string = "Please select action 2";
    majorActionA: string = "Please select action 1";
    majorActionB: string = "Please select action 2";
    minorActionA: string = "Please select action 1";
    minorActionB: string = "Please select action 2";

    criticalActionSelectedType1: number = 0;
    criticalSnmpVersion1: number = 1;
    criticalCommunity1: string = "";
    criticalAgentAddress1: string = "";
    criticalIp1: string = "";
    criticalOid1: string = "";
    criticalMessage1: string = "";
    criticalScript1: string = "";
    criticalRundeckIp1: string = "";
    criticalUser1: string = "";
    criticalPassword1: string = "";
    criticalCommand1: string = "";

    criticalActionSelectedType2: number = 0;
    criticalSnmpVersion2: number = 1;
    criticalCommunity2: string = "";
    criticalAgentAddress2: string = "";
    criticalIp2: string = "";
    criticalOid2: string = "";
    criticalMessage2: string = "";
    criticalScript2: string = "";
    criticalRundeckIp2: string = "";
    criticalUser2: string = "";
    criticalPassword2: string = "";
    criticalCommand2: string = "";

    majorActionSelectedType1: number = 0;
    majorSnmpVersion1: number = 1;
    majorCommunity1: string = "";
    majorAgentAddress1: string = "";
    majorIp1: string = "";
    majorOid1: string = "";
    majorMessage1: string = "";
    majorScript1: string = "";
    majorRundeckIp1: string = "";
    majorUser1: string = "";
    majorPassword1: string = "";
    majorCommand1: string = "";

    majorActionSelectedType2: number = 0;
    majorSnmpVersion2: number = 1;
    majorCommunity2: string = "";
    majorAgentAddress2: string = "";
    majorIp2: string = "";
    majorOid2: string = "";
    majorMessage2: string = "";
    majorScript2: string = "";
    majorRundeckIp2: string = "";
    majorUser2: string = "";
    majorPassword2: string = "";
    majorCommand2: string = "";

    minorActionSelectedType1: number = 0;
    minorSnmpVersion1: number = 1;
    minorCommunity1: string = "";
    minorAgentAddress1: string = "";
    minorIp1: string = "";
    minorOid1: string = "";
    minorMessage1: string = "";
    minorScript1: string = "";
    minorRundeckIp1: string = "";
    minorUser1: string = "";
    minorPassword1: string = "";
    minorCommand1: string = "";

    minorActionSelectedType2: number = 0;
    minorSnmpVersion2: number = 1;
    minorCommunity2: string = "";
    minorAgentAddress2: string = "";
    minorIp2: string = "";
    minorOid2: string = "";
    minorMessage2: string = "";
    minorScript2: string = "";
    minorRundeckIp2: string = "";
    minorUser2: string = "";
    minorPassword2: string = "";
    minorCommand2: string = "";

    constructor(
        public httpClient: HttpClientComponent,
        public router: Router,
        private route: ActivatedRoute,
        private modalService: BsModalService
    ) {}

    ngOnInit(){
        this.httpClient.setUrl(this.apiPrefix);
        this.init();

    }

    ngAfterViewInit() {
        this.columnOne = "table sample";
    }

    init(){
        let name = this.route.snapshot.queryParams['name'];
        let column = this.route.snapshot.queryParams['column'];
        if (name != ""){
            this.actionPolicyName = name;
            this.isNew = false;
            this.initForExist(name);
        } else {

        }


    }

    initForExist(name){
        let url = '/api_action_policy/?name='+name;
        this.httpClient
            .toJson(this.httpClient.get(url))
            .subscribe(res => {
                // this.initVariable(res);
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    if (res['data']) {
                        this.initVariable(res['data']);
                    }
                } else {
                    if (res['status'] && res['status']['message']) {
                        alert(res['status']['message']);
                        // jump to view
                    }
                }
        });
    }

    initVariable(data){
        console.log(data);
        let commonData = data['common_data'];
        this.actionPolicyName = commonData['name'];
        this.actionPolicyDescription = commonData['desc'];
        this.triggerType = commonData['trigger_type'];

        if (data['critical']){

        }

        if (data['major']){

        }

        if (data['minor']){

        }
    }

    resetAll(){
        this.resetColumn();
    }

    resetColumn(){
        this.columnOne = "";
        this.columnA = "";
        this.columnB = "";
    }

    resetTable(){

    }

    selectColumn(template, isWhich){
        this.selectingColumn = isWhich;
        this.modalRef = this.modalService.show(template, this.modalConfig);
        this.drawColumnTable();
    }

    drawColumnTable(){
        let _this = this;
        $('#columnTable').jqGrid({
            url: '/v1/api_column/',
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: _this.columnModel,
            // postData: { '': '' },
            // data: _this.testData,
            // viewrecords: true,
            onSelectRow: function(rowid,status,e) {
              let table_id = e.target.parentElement.cells[0].innerHTML;
              _this.columnSelected = table_id;
              let policy_id = e.target.parentElement.cells[1].innerHTML;
              _this.drawHistoryDataTable(table_id, policy_id);
            },
            loadComplete: function() {
                // _this.showDataTable();
                // _this.renderColor();
            },
            // rowNum: 10,
            // rowList: [ 10, 20, 30],
            autowidth: true,

            // beforeSelectRow: function(rowid, e) { return false; },
            // height: 230,
            // pager: '#actionPolicyPager',
            jsonReader: {
                root: 'data.data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        });

    }

    drawHistoryDataTable(table_id, policy_id){
        console.log(table_id, policy_id);
        let _this = this;
        $('#historyDataTable').jqGrid({
            url: '/v1/api_column/',
            datatype: 'JSON',
            // datatype: 'local',
            mtype: 'get',
            colModel: _this.historyDataModel,
            postData: { 'id': table_id,  'policy_id': policy_id},
            // data: _this.testData,
            // viewrecords: true,
            // onSelectRow: function(rowid,status,e) {
            // },
            loadComplete: function(res) {
                _this.drawHistoryDataTableLastTitle(res);
                _this.drawPolicyTree(res);
            },
            // rowNum: 10,
            // rowList: [ 10, 20, 30],
            autowidth: true,
            // beforeSelectRow: function(rowid, e) { return false; },
            // height: 230,
            // pager: '#actionPolicyPager',
            jsonReader: {
                root: 'data.data_history.data.data',
                page: 'current_page_num',
                total: 'num_page',
                records: 'total_num',
                userData: 'status',
                repeatitems: false,
            },
        }).setGridParam({postData: { 'id': table_id,  'policy_id': policy_id}}).trigger("reloadGrid");
    }

    drawHistoryDataTableLastTitle(res){
        let title = res.data['data_history'];
        console.log(title);
        // $('#historyDataTable').jqGrid('setLabel', 'valid_status', title);
    }

    drawPolicyTree(res){
        let _t = this;
        let data = res['data']['policy_tree'];
        $('#policyTree').jstree({
            'core': {
                'check_callback': false,
                'data': data,
            },
            // 'plugins': ['state'],
            // 'state': { 'opened': true },
            'expand_selected_onload': true,
        });


    }

    selectAction(template, isWhich){
        this.editingAction = isWhich;
        if (isWhich == "critical_1"){
            this.actionSelectedType = this.criticalActionSelectedType1;
            this.snmpVersion = this.criticalSnmpVersion1;
            this.snmpCommunity = this.criticalCommunity1;
            this.snmpAgent = this.criticalAgentAddress1;
            this.snmpIp = this.criticalIp1;
            this.snmpOid = this.criticalOid1;
            this.snmpMessage = this.criticalMessage1;
            this.script = this.criticalScript1;
            this.rundeckIp = this.criticalRundeckIp1;
            this.rundeckUser = this.criticalUser1;
            this.rundeckPassword = this.criticalPassword1;
            this.rundeckCommand = this.criticalCommand1;
            this.actionSelectTitle = "Critical Action 1";
        } else if (isWhich == "critical_2"){
            this.actionSelectedType = this.criticalActionSelectedType2;
            this.snmpVersion = this.criticalSnmpVersion2;
            this.snmpCommunity = this.criticalCommunity2;
            this.snmpAgent = this.criticalAgentAddress2;
            this.snmpIp = this.criticalIp2;
            this.snmpOid = this.criticalOid2;
            this.snmpMessage = this.criticalMessage2;
            this.script = this.criticalScript2;
            this.rundeckIp = this.criticalRundeckIp2;
            this.rundeckUser = this.criticalUser2;
            this.rundeckPassword = this.criticalPassword2;
            this.rundeckCommand = this.criticalCommand2;
            this.actionSelectTitle = "Critical Action 2";
        } else if (isWhich == "major_1"){
            this.actionSelectedType = this.majorActionSelectedType1;
            this.snmpVersion = this.majorSnmpVersion1;
            this.snmpCommunity = this.majorCommunity1;
            this.snmpAgent = this.majorAgentAddress1;
            this.snmpIp = this.majorIp1;
            this.snmpOid = this.majorOid1;
            this.snmpMessage = this.majorMessage1;
            this.script = this.majorScript1;
            this.rundeckIp = this.majorRundeckIp1;
            this.rundeckUser = this.majorUser1;
            this.rundeckPassword = this.majorPassword1;
            this.rundeckCommand = this.majorCommand1;
            this.actionSelectTitle = "Major Action 1";
        } else if (isWhich == "major_2"){
            this.actionSelectedType = this.majorActionSelectedType2;
            this.snmpVersion = this.majorSnmpVersion2;
            this.snmpCommunity = this.majorCommunity2;
            this.snmpAgent = this.majorAgentAddress2;
            this.snmpIp = this.majorIp2;
            this.snmpOid = this.majorOid2;
            this.snmpMessage = this.majorMessage2;
            this.script = this.majorScript2;
            this.rundeckIp = this.majorRundeckIp2;
            this.rundeckUser = this.majorUser2;
            this.rundeckPassword = this.majorPassword2;
            this.rundeckCommand = this.majorCommand2;
            this.actionSelectTitle = "Major Action 2";
        } else if (isWhich == "minor_1"){
            this.actionSelectedType = this.minorActionSelectedType1;
            this.snmpVersion = this.minorSnmpVersion1;
            this.snmpCommunity = this.minorCommunity1;
            this.snmpAgent = this.minorAgentAddress1;
            this.snmpIp = this.minorIp1;
            this.snmpOid = this.minorOid1;
            this.snmpMessage = this.minorMessage1;
            this.script = this.minorScript1;
            this.rundeckIp = this.minorRundeckIp1;
            this.rundeckUser = this.minorUser1;
            this.rundeckPassword = this.minorPassword1;
            this.rundeckCommand = this.minorCommand1;
            this.actionSelectTitle = "Minor Action 1";
        } else if (isWhich == "minor_2"){
            this.actionSelectedType = this.minorActionSelectedType2;
            this.snmpVersion = this.minorSnmpVersion2;
            this.snmpCommunity = this.minorCommunity2;
            this.snmpAgent = this.minorAgentAddress2;
            this.snmpIp = this.minorIp2;
            this.snmpOid = this.minorOid2;
            this.snmpMessage = this.minorMessage2;
            this.script = this.minorScript2;
            this.rundeckIp = this.minorRundeckIp2;
            this.rundeckUser = this.minorUser2;
            this.rundeckPassword = this.minorPassword2;
            this.rundeckCommand = this.minorCommand2;
            this.actionSelectTitle = "Minor Action 2";
        }

        this.modalRef = this.modalService.show(template, this.modalConfig);
    }


    confirmSelectedAction(){

        let actionName;
        for (let i=0; i<this.actionTypes.length; i++){
            if (this.actionTypes[i]['id'] == this.actionSelectedType ){
                actionName = this.actionTypes[i]['value'];
            }
        }

        if (this.editingAction == "critical_1"){
            this.criticalActionSelectedType1 = this.actionSelectedType;
            this.criticalSnmpVersion1 = this.snmpVersion;
            this.criticalCommunity1 = this.snmpCommunity;
            this.criticalAgentAddress1 = this.snmpAgent;
            this.criticalIp1 = this.snmpIp;
            this.criticalOid1 = this.snmpOid;
            this.criticalMessage1 = this.snmpMessage;
            this.criticalScript1 = this.script;
            this.criticalRundeckIp1 = this.rundeckIp;
            this.criticalUser1 = this.rundeckUser;
            this.criticalPassword1 = this.rundeckPassword;
            this.criticalCommand1 = this.rundeckCommand;
            this.criticalActionA = actionName;
        } else if (this.editingAction == "critical_2"){
            this.criticalActionSelectedType2 = this.actionSelectedType;
            this.criticalSnmpVersion2 = this.snmpVersion;
            this.criticalCommunity2 = this.snmpCommunity;
            this.criticalAgentAddress2 = this.snmpAgent;
            this.criticalIp2 = this.snmpIp;
            this.criticalOid2 = this.snmpOid;
            this.criticalMessage2 = this.snmpMessage;
            this.criticalScript2 = this.script;
            this.criticalRundeckIp2 = this.rundeckIp;
            this.criticalUser2 = this.rundeckUser;
            this.criticalPassword2 = this.rundeckPassword;
            this.criticalCommand2 = this.rundeckCommand;
            this.criticalActionB = actionName;
        } else if (this.editingAction == "major_1"){
            this.majorActionSelectedType1 = this.actionSelectedType;
            this.majorSnmpVersion1 = this.snmpVersion;
            this.majorCommunity1 = this.snmpCommunity;
            this.majorAgentAddress1 = this.snmpAgent;
            this.majorIp1 = this.snmpIp;
            this.majorOid1 = this.snmpOid;
            this.majorMessage1 = this.snmpMessage;
            this.majorScript1 = this.script;
            this.majorRundeckIp1 = this.rundeckIp;
            this.majorUser1 = this.rundeckUser;
            this.majorPassword1 = this.rundeckPassword;
            this.majorCommand1 = this.rundeckCommand;
            this.majorActionA = actionName;
        } else if (this.editingAction == "major_2"){
            this.majorActionSelectedType2 = this.actionSelectedType;
            this.majorSnmpVersion2 = this.snmpVersion;
            this.majorCommunity2 = this.snmpCommunity;
            this.majorAgentAddress2 = this.snmpAgent;
            this.majorIp2 = this.snmpIp;
            this.majorOid2 = this.snmpOid;
            this.majorMessage2 = this.snmpMessage;
            this.majorScript2 = this.script;
            this.majorRundeckIp2 = this.rundeckIp;
            this.majorUser2 = this.rundeckUser;
            this.majorPassword2 = this.rundeckPassword;
            this.majorCommand2 = this.rundeckCommand;
            this.majorActionB = actionName;
        } else if (this.editingAction == "minor_1"){
            this.minorActionSelectedType1 = this.actionSelectedType;
            this.minorSnmpVersion1 = this.snmpVersion;
            this.minorCommunity1 = this.snmpCommunity;
            this.minorAgentAddress1 = this.snmpAgent;
            this.minorIp1 = this.snmpIp;
            this.minorOid1 = this.snmpOid;
            this.minorMessage1 = this.snmpMessage;
            this.minorScript1 = this.script;
            this.minorRundeckIp1 = this.rundeckIp;
            this.minorUser1 = this.rundeckUser;
            this.minorPassword1 = this.rundeckPassword;
            this.minorCommand1 = this.rundeckCommand;
            this.minorActionA = actionName;
        } else if (this.editingAction == "minor_2"){
            this.minorActionSelectedType2 = this.actionSelectedType;
            this.minorSnmpVersion2 = this.snmpVersion;
            this.minorCommunity2 = this.snmpCommunity;
            this.minorAgentAddress2 = this.snmpAgent;
            this.minorIp2 = this.snmpIp;
            this.minorOid2 = this.snmpOid;
            this.minorMessage2 = this.snmpMessage;
            this.minorScript2 = this.script;
            this.minorRundeckIp2 = this.rundeckIp;
            this.minorUser2 = this.rundeckUser;
            this.minorPassword2 = this.rundeckPassword;
            this.minorCommand2 = this.rundeckCommand;
            this.minorActionB = actionName;
        }

        this.modalRef.hide();
    }

    save(){

        let type = this.triggerType;
        let checkResult = this.checkForSave(type);
        if (!checkResult['flag']){
            alert(checkResult['message']);
            return;
        }

        let actionPolicyInfo: any = {};
        let url = '/api_action_policy/';
        actionPolicyInfo['name'] = this.actionPolicyName;
        actionPolicyInfo['desc'] = this.actionPolicyDescription;

        if (type == 0) {
            actionPolicyInfo = this.saveCalculationType(actionPolicyInfo, checkResult['filledField']);
        } else if (type == 1) {
            actionPolicyInfo = this.saveNumberType(actionPolicyInfo, checkResult['filledField']);
        } else if (type == 2) {
            actionPolicyInfo = this.saveStringType(actionPolicyInfo, checkResult['filledField']);
        } else if (type == 3) {
            actionPolicyInfo = this.saveFailedType(actionPolicyInfo, checkResult['filledField']);
        }

        console.log(actionPolicyInfo);

        if (this.isNew){
            this.httpClient
                .toJson(this.httpClient.post(url, actionPolicyInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['status']['message'] == "Success") {
                           alert('アクションポリシー追加しました。');
                        }
                    } else {
                        alert(res['status']['message']);
                    }
            });
        } else{
            this.httpClient
                .toJson(this.httpClient.put(url, actionPolicyInfo))
                .subscribe(res => {
                    if (res['status']['status'].toString().toLowerCase() === 'true') {
                        if (res['status']['message'] == "Success") {
                           alert('アクションポリシー更新しました。');
                        }
                    } else {
                        alert(res['status']['message']);
                    }
            });
        }



    }

    checkForSave(type){
        let result: any = {};
        let flag: boolean = true;
        let message: string = "";
        let filledField = this.checkAtLeastOnePriorityFilled(type);
        if (!filledField['critical']['filled'] && !filledField['major']['filled'] && !filledField['minor']['filled']){
            flag = false;
            message = "Please filled at least one field";
        }
        // this.isColumnMachTrigger(type);

        result['flag'] = flag;
        result['message'] = message;
        result['filledField'] = filledField;
        return result

    }

    checkAtLeastOnePriorityFilled(type){
        let checkResult: any = {
            critical: {filled: false, action1: false, action2: false},
            major: {filled: false, action1: false, action2: false},
            minor: {filled: false, action1: false, action2: false}
        };

        if (type == 2 || type == 1){
            if (this.critical_value.trim() != ""){
                if (this.criticalActionA != "Please select action 1"){
                    checkResult['critical']['action1'] = true;
                    checkResult['critical']['filled'] = true;
                }
                if (this.criticalActionB != "Please select action 2"){
                    checkResult['critical']['action2'] = true;
                    checkResult['critical']['filled'] = true;
                }
            }
            if (this.major_value.trim() != ""){
                if (this.majorActionA != "Please select action 1"){
                    checkResult['major']['action1'] = true;
                    checkResult['major']['filled'] = true;
                }
                if (this.majorActionB != "Please select action 2"){
                    checkResult['major']['action2'] = true;
                    checkResult['major']['filled'] = true;
                }
            }
            if (this.minor_value.trim() != ""){
                if (this.minorActionA != "Please select action 1"){
                    checkResult['minor']['action1'] = true;
                    checkResult['minor']['filled'] = true;
                }
                if (this.minorActionB != "Please select action 2"){
                    checkResult['minor']['action2'] = true;
                    checkResult['minor']['filled'] = true;
                }
            }
        } else if (type == 3){

            if (this.criticalActionA != "Please select action 1"){
                checkResult['critical']['action1'] = true;
                checkResult['critical']['filled'] = true;
            }
            if (this.criticalActionB != "Please select action 2"){
                checkResult['critical']['action2'] = true;
                checkResult['critical']['filled'] = true;
            }


            if (this.majorActionA != "Please select action 1"){
                checkResult['major']['action1'] = true;
                checkResult['major']['filled'] = true;
            }
            if (this.majorActionB != "Please select action 2"){
                checkResult['major']['action2'] = true;
                checkResult['major']['filled'] = true;
            }


            if (this.minorActionA != "Please select action 1"){
                checkResult['minor']['action1'] = true;
                checkResult['minor']['filled'] = true;
            }
            if (this.minorActionB != "Please select action 2"){
                checkResult['minor']['action2'] = true;
                checkResult['minor']['filled'] = true;
            }

        } else if (type == 0){
            if (this.critical_function.trim() != ""){
                if (this.criticalActionA != "Please select action 1"){
                    checkResult['critical']['action1'] = true;
                    checkResult['critical']['filled'] = true;
                }
                if (this.criticalActionB != "Please select action 2"){
                    checkResult['critical']['action2'] = true;
                    checkResult['critical']['filled'] = true;
                }
            }
            if (this.major_function.trim() != ""){
                if (this.majorActionA != "Please select action 1"){
                    checkResult['major']['action1'] = true;
                    checkResult['major']['filled'] = true;
                }
                if (this.majorActionB != "Please select action 2"){
                    checkResult['major']['action2'] = true;
                    checkResult['major']['filled'] = true;
                }
            }
            if (this.minor_function.trim() != ""){
                if (this.minorActionA != "Please select action 1"){
                    checkResult['minor']['action1'] = true;
                    checkResult['minor']['filled'] = true;
                }
                if (this.minorActionB != "Please select action 2"){
                    checkResult['minor']['action2'] = true;
                    checkResult['minor']['filled'] = true;
                }
            }
        }

        return checkResult


    }

    isColumnMachTrigger(type){

    }

    checkStringType(){

    }

    saveStringType(actionPolicyInfo, filledField){

        actionPolicyInfo['trigger_type'] = 2;
        actionPolicyInfo['column_a'] = this.columnOne;
        actionPolicyInfo['column_b'] = null;

        if (filledField['critical']['filled']){
            actionPolicyInfo['critical_priority'] = "0";
            actionPolicyInfo['critical_threshold'] = this.critical_value;
            actionPolicyInfo['critical_condition'] = this.critical_string_condition;
            actionPolicyInfo['critical_limit_nums'] = this.critical_continuous_condition;
        }

        if (filledField['major']['filled']) {
            actionPolicyInfo['major_priority'] = "1";
            actionPolicyInfo['major_threshold'] = this.major_value;
            actionPolicyInfo['major_condition'] = this.major_string_condition;
            actionPolicyInfo['major_limit_nums'] = this.major_continuous_condition;
        }

        if (filledField['minor']['filled']){
            actionPolicyInfo['minor_priority'] = "2";
            actionPolicyInfo['minor_threshold'] = this.minor_value;
            actionPolicyInfo['minor_condition'] = this.minor_string_condition;
            actionPolicyInfo['minor_limit_nums'] = this.minor_continuous_condition;
        }

        actionPolicyInfo = this.saveActions(actionPolicyInfo, filledField);
        return actionPolicyInfo;

    }

    saveNumberType(actionPolicyInfo, filledField){

        actionPolicyInfo['trigger_type'] = 1;
        actionPolicyInfo['column_a'] = this.columnOne;
        actionPolicyInfo['column_b'] = null;

        if (filledField['critical']['filled']){
            actionPolicyInfo['critical_priority'] = "0";
            actionPolicyInfo['critical_threshold'] = this.critical_value;
            actionPolicyInfo['critical_condition'] = this.critical_number_condition;
            actionPolicyInfo['critical_limit_nums'] = this.critical_continuous_condition;
        }

        if (filledField['major']['filled']){
            actionPolicyInfo['major_priority'] = "1";
            actionPolicyInfo['major_threshold'] = this.major_value;
            actionPolicyInfo['major_condition'] = this.major_number_condition;
            actionPolicyInfo['major_limit_nums'] = this.major_continuous_condition;
        }

        if (filledField['minor']['filled']){
            actionPolicyInfo['minor_priority'] = "2";
            actionPolicyInfo['minor_threshold'] = this.minor_value;
            actionPolicyInfo['minor_condition'] = this.minor_number_condition;
            actionPolicyInfo['minor_limit_nums'] = this.minor_continuous_condition;
        }

        actionPolicyInfo = this.saveActions(actionPolicyInfo, filledField);
        return actionPolicyInfo

    }

    saveCalculationType(actionPolicyInfo, filledField){

        actionPolicyInfo['trigger_type'] = 0;
        actionPolicyInfo['column_a'] = this.columnA;
        actionPolicyInfo['column_b'] = this.columnB;

        if (filledField['critical']['filled']){
            actionPolicyInfo['critical_priority'] = "0";
            actionPolicyInfo['critical_threshold'] = this.critical_function;
            actionPolicyInfo['critical_limit_nums'] = this.critical_continuous_condition;
        }

        if (filledField['major']['filled']){
            actionPolicyInfo['major_priority'] = "1";
            actionPolicyInfo['major_threshold'] = this.major_function;
            actionPolicyInfo['major_limit_nums'] = this.major_continuous_condition;
        }

        if (filledField['minor']['filled']){
            actionPolicyInfo['minor_priority'] = "2";
            actionPolicyInfo['minor_threshold'] = this.minor_function;
            actionPolicyInfo['minor_limit_nums'] = this.minor_continuous_condition;
        }

        actionPolicyInfo = this.saveActions(actionPolicyInfo, filledField);
        return actionPolicyInfo

    }

    saveFailedType(actionPolicyInfo, filledField){

        actionPolicyInfo['trigger_type'] = 3;
        actionPolicyInfo['column_a'] = this.columnOne;
        actionPolicyInfo['column_b'] = null;

        if (filledField['critical']['filled']){
            actionPolicyInfo['critical_priority'] = "0";
        }

        if (filledField['major']['filled']){
            actionPolicyInfo['major_priority'] = "1";
        }

        if (filledField['minor']['filled']){
            actionPolicyInfo['minor_priority'] = "2";
        }

        actionPolicyInfo = this.saveActions(actionPolicyInfo, filledField);
        return actionPolicyInfo

    }

    saveActions(actionPolicyInfo, filledField){
        if (filledField['critical']['filled']){
            if (filledField['critical']['action1']){
                actionPolicyInfo['critical_action_type_1'] = this.criticalActionSelectedType1;
                actionPolicyInfo['critical_snmp_version_1'] = this.criticalSnmpVersion1;
                actionPolicyInfo['critical_snmp_comminute_1'] = this.criticalCommunity1;
                actionPolicyInfo['critical_agent_address_1'] = this.criticalAgentAddress1;
                actionPolicyInfo['critical_destination_address_1'] = this.criticalIp1;
                actionPolicyInfo['critical_oid_1'] = this.criticalOid1;
                actionPolicyInfo['critical_msg_1'] = this.criticalMessage1;
                actionPolicyInfo['critical_execute_script_1'] = this.criticalScript1;
                actionPolicyInfo['critical_runner_server_1'] = this.criticalRundeckIp1;
                actionPolicyInfo['critical_runner_username_1'] = this.criticalUser1;
                actionPolicyInfo['critical_runner_password_1'] = this.criticalPassword1;
                actionPolicyInfo['critical_runner_command_1'] = this.criticalCommand1;

            } else {
                actionPolicyInfo['critical_action_type_1'] = null;
                actionPolicyInfo['critical_snmp_version_1'] = null;
                actionPolicyInfo['critical_snmp_comminute_1'] = null;
                actionPolicyInfo['critical_agent_address_1'] = null;
                actionPolicyInfo['critical_destination_address_1'] = null;
                actionPolicyInfo['critical_oid_1'] = null;
                actionPolicyInfo['critical_msg_1'] = null;
                actionPolicyInfo['critical_execute_script_1'] = null;
                actionPolicyInfo['critical_runner_server_1'] = null;
                actionPolicyInfo['critical_runner_username_1'] = null;
                actionPolicyInfo['critical_runner_password_1'] = null;
                actionPolicyInfo['critical_runner_command_1'] = null;
            }
            if (filledField['critical']['action2']){
                actionPolicyInfo['critical_action_type_2'] = this.criticalActionSelectedType2;
                actionPolicyInfo['critical_snmp_version_2'] = this.criticalSnmpVersion2;
                actionPolicyInfo['critical_snmp_comminute_2'] = this.criticalCommunity2;
                actionPolicyInfo['critical_agent_address_2'] = this.criticalAgentAddress2;
                actionPolicyInfo['critical_destination_address_2'] = this.criticalIp2;
                actionPolicyInfo['critical_oid_2'] = this.criticalOid2;
                actionPolicyInfo['critical_msg_2'] = this.criticalMessage2;
                actionPolicyInfo['critical_execute_script_2'] = this.criticalScript2;
                actionPolicyInfo['critical_runner_server_2'] = this.criticalRundeckIp2;
                actionPolicyInfo['critical_runner_username_2'] = this.criticalUser2;
                actionPolicyInfo['critical_runner_password_2'] = this.criticalPassword2;
                actionPolicyInfo['critical_runner_command_2'] = this.criticalCommand2;

            } else {
                actionPolicyInfo['critical_action_type_2'] = null;
                actionPolicyInfo['critical_snmp_version_2'] = null;
                actionPolicyInfo['critical_snmp_comminute_2'] = null;
                actionPolicyInfo['critical_agent_address_2'] = null;
                actionPolicyInfo['critical_destination_address_2'] = null;
                actionPolicyInfo['critical_oid_2'] = null;
                actionPolicyInfo['critical_msg_2'] = null;
                actionPolicyInfo['critical_execute_script_2'] = null;
                actionPolicyInfo['critical_runner_server_2'] = null;
                actionPolicyInfo['critical_runner_username_2'] = null;
                actionPolicyInfo['critical_runner_password_2'] = null;
                actionPolicyInfo['critical_runner_command_2'] = null;
            }
        }

        if (filledField['major']['filled']){

            if (filledField['major']['action1']){
                actionPolicyInfo['major_action_type_1'] = this.majorActionSelectedType1;
                actionPolicyInfo['major_snmp_version_1'] = this.majorSnmpVersion1;
                actionPolicyInfo['major_snmp_comminute_1'] = this.majorCommunity1;
                actionPolicyInfo['major_agent_address_1'] = this.majorAgentAddress1;
                actionPolicyInfo['major_destination_address_1'] = this.majorIp1;
                actionPolicyInfo['major_oid_1'] = this.majorOid1;
                actionPolicyInfo['major_msg_1'] = this.majorMessage1;
                actionPolicyInfo['major_execute_script_1'] = this.majorScript1;
                actionPolicyInfo['major_runner_server_1'] = this.majorRundeckIp1;
                actionPolicyInfo['major_runner_username_1'] = this.majorUser1;
                actionPolicyInfo['major_runner_password_1'] = this.majorPassword1;
                actionPolicyInfo['major_runner_command_1'] = this.majorCommand1;

            } else {
                actionPolicyInfo['major_action_type_1'] = null;
                actionPolicyInfo['major_snmp_version_1'] = null;
                actionPolicyInfo['major_snmp_comminute_1'] = null;
                actionPolicyInfo['major_agent_address_1'] = null;
                actionPolicyInfo['major_destination_address_1'] = null;
                actionPolicyInfo['major_oid_1'] = null;
                actionPolicyInfo['major_msg_1'] = null;
                actionPolicyInfo['major_execute_script_1'] = null;
                actionPolicyInfo['major_runner_server_1'] = null;
                actionPolicyInfo['major_runner_username_1'] = null;
                actionPolicyInfo['major_runner_password_1'] = null;
                actionPolicyInfo['major_runner_command_1'] = null;
            }
            if (filledField['major']['action2']){
                actionPolicyInfo['major_action_type_2'] = this.majorActionSelectedType2;
                actionPolicyInfo['major_snmp_version_2'] = this.majorSnmpVersion2;
                actionPolicyInfo['major_snmp_comminute_2'] = this.majorCommunity2;
                actionPolicyInfo['major_agent_address_2'] = this.majorAgentAddress2;
                actionPolicyInfo['major_destination_address_2'] = this.majorIp2;
                actionPolicyInfo['major_oid_2'] = this.majorOid2;
                actionPolicyInfo['major_msg_2'] = this.majorMessage2;
                actionPolicyInfo['major_execute_script_2'] = this.majorScript2;
                actionPolicyInfo['major_runner_server_2'] = this.majorRundeckIp2;
                actionPolicyInfo['major_runner_username_2'] = this.majorUser2;
                actionPolicyInfo['major_runner_password_2'] = this.majorPassword2;
                actionPolicyInfo['major_runner_command_2'] = this.majorCommand2;

            } else {
                actionPolicyInfo['major_action_type_2'] = null;
                actionPolicyInfo['major_snmp_version_2'] = null;
                actionPolicyInfo['major_snmp_comminute_2'] = null;
                actionPolicyInfo['major_agent_address_2'] = null;
                actionPolicyInfo['major_destination_address_2'] = null;
                actionPolicyInfo['major_oid_2'] = null;
                actionPolicyInfo['major_msg_2'] = null;
                actionPolicyInfo['major_execute_script_2'] = null;
                actionPolicyInfo['major_runner_server_2'] = null;
                actionPolicyInfo['major_runner_username_2'] = null;
                actionPolicyInfo['major_runner_password_2'] = null;
                actionPolicyInfo['major_runner_command_2'] = null;
            }
        }

        if (filledField['minor']['filled']){

            if (filledField['minor']['action1']){
                actionPolicyInfo['minor_action_type_1'] = this.minorActionSelectedType1;
                actionPolicyInfo['minor_snmp_version_1'] = this.minorSnmpVersion1;
                actionPolicyInfo['minor_snmp_comminute_1'] = this.minorCommunity1;
                actionPolicyInfo['minor_agent_address_1'] = this.minorAgentAddress1;
                actionPolicyInfo['minor_destination_address_1'] = this.minorIp1;
                actionPolicyInfo['minor_oid_1'] = this.minorOid1;
                actionPolicyInfo['minor_msg_1'] = this.minorMessage1;
                actionPolicyInfo['minor_execute_script_1'] = this.minorScript1;
                actionPolicyInfo['minor_runner_server_1'] = this.minorRundeckIp1;
                actionPolicyInfo['minor_runner_username_1'] = this.minorUser1;
                actionPolicyInfo['minor_runner_password_1'] = this.minorPassword1;
                actionPolicyInfo['minor_runner_command_1'] = this.minorCommand1;

            } else {
                actionPolicyInfo['minor_action_type_1'] = null;
                actionPolicyInfo['minor_snmp_version_1'] = null;
                actionPolicyInfo['minor_snmp_comminute_1'] = null;
                actionPolicyInfo['minor_agent_address_1'] = null;
                actionPolicyInfo['minor_destination_address_1'] = null;
                actionPolicyInfo['minor_oid_1'] = null;
                actionPolicyInfo['minor_msg_1'] = null;
                actionPolicyInfo['minor_execute_script_1'] = null;
                actionPolicyInfo['minor_runner_server_1'] = null;
                actionPolicyInfo['minor_runner_username_1'] = null;
                actionPolicyInfo['minor_runner_password_1'] = null;
                actionPolicyInfo['minor_runner_command_1'] = null;
            }
            if (filledField['minor']['action2']){
                actionPolicyInfo['minor_action_type_2'] = this.minorActionSelectedType2;
                actionPolicyInfo['minor_snmp_version_2'] = this.minorSnmpVersion2;
                actionPolicyInfo['minor_snmp_comminute_2'] = this.minorCommunity2;
                actionPolicyInfo['minor_agent_address_2'] = this.minorAgentAddress2;
                actionPolicyInfo['minor_destination_address_2'] = this.minorIp2;
                actionPolicyInfo['minor_oid_2'] = this.minorOid2;
                actionPolicyInfo['minor_msg_2'] = this.minorMessage2;
                actionPolicyInfo['minor_execute_script_2'] = this.minorScript2;
                actionPolicyInfo['minor_runner_server_2'] = this.minorRundeckIp2;
                actionPolicyInfo['minor_runner_username_2'] = this.minorUser2;
                actionPolicyInfo['minor_runner_password_2'] = this.minorPassword2;
                actionPolicyInfo['minor_runner_command_2'] = this.minorCommand2;

            } else {
                actionPolicyInfo['minor_action_type_2'] = null;
                actionPolicyInfo['minor_snmp_version_2'] = null;
                actionPolicyInfo['minor_snmp_comminute_2'] = null;
                actionPolicyInfo['minor_agent_address_2'] = null;
                actionPolicyInfo['minor_destination_address_2'] = null;
                actionPolicyInfo['minor_oid_2'] = null;
                actionPolicyInfo['minor_msg_2'] = null;
                actionPolicyInfo['minor_execute_script_2'] = null;
                actionPolicyInfo['minor_runner_server_2'] = null;
                actionPolicyInfo['minor_runner_username_2'] = null;
                actionPolicyInfo['minor_runner_password_2'] = null;
                actionPolicyInfo['minor_runner_command_2'] = null;
            }
        }

        return actionPolicyInfo;
    }


}