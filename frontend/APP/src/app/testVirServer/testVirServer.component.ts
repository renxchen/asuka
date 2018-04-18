import { Component, OnInit } from '@angular/core';
import { Http } from '@angular/http';
import { HttpClientComponent } from '../../components/utils/httpClient';
import { ProgressbarComponent } from '../../components/processbar/processbar.component';
import { Validator } from '../../components/validation/validation';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { BsModalService } from 'ngx-bootstrap/modal';
import { Observable } from 'rxjs/Rx';
import * as _ from 'lodash';
declare var $: any;

@Component({
    selector: 'test-virServer',
    templateUrl: './testVirServer.component.html',
    styleUrls: ['./testVirServer.component.less']
})
export class TestVirServerComponent implements OnInit {
    commands: any;
    port: any;
    expect: any;
    apiPrefix: any = '/api/v1';
    startTrashBinFlg: Boolean = true;
    startRegFlg: Boolean = true;
    startCmds: any = [];
    countStart: number;
    formData: FormData;
    filename: any;
    uploadFlg: string;
    loginFlg: Boolean = true;
    processbar: BsModalRef;
    portNotNull: Boolean = true;
    portFlg: Boolean = true;
    expectNotNull: Boolean = true;
    expectFlg: Boolean = true;
    outputs: any;
    loadingStart: Boolean = false;
    loadingStop: Boolean = false;
    loadingRestart: Boolean = false;
    loadingUpload: Boolean = false;
    loadingQuery: Boolean = false;
    modalConfig = {
        animated: true,
        keyboard: false,
        backdrop: true,
        ignoreBackdropClick: true,
        class: 'modal-md'
    };
    constructor(
        private httpClient: HttpClientComponent,
        private http: Http,
        private modalService: BsModalService,
    ) { }

    ngOnInit(): void {
        this.startCmdsInit();
        this.uploadFlg = 'null';
    }
    public startCmdsInit() {
        this.startTrashBinFlg = true;
        this.startCmds = [];
        this.countStart = 1;
        let firstStartCmd = {
            'id': this.countStart,
            'name': '',
            'startCmdFlg': false,
            'startRegFlg': true,
        };
        this.startCmds.push(firstStartCmd);
        return firstStartCmd;
    }
    public addStartCmd() {
        this.startTrashBinFlg = false;
        let addStartTmp: any = [];
        addStartTmp = _.cloneDeep(this.startCmds);
        let startCmdInfo = {
            'id': addStartTmp.length + 1,
            'name': '',
            'startCmdFlg': false,
            'startRegFlg': true,
        };
        let id: any = startCmdInfo['id'];
        let penult = id - 1;
        if (addStartTmp[penult - 1]['id'] === penult) {
            addStartTmp[penult - 1]['startCmdFlg'] = true;
        }
        addStartTmp.push(startCmdInfo);
        this.startCmds = addStartTmp;
    }
    public delStartCmd(startCmd: any) {
        let delStartTmp: any = [];
        delStartTmp = _.cloneDeep(this.startCmds);
        for (let i = 0; i < delStartTmp.length; i++) {
            if (delStartTmp.length > 1 && delStartTmp[i]['id'] === startCmd['id']) {
                delStartTmp.splice(i, 1);
            }
        }
        for (let i = 0; i < delStartTmp.length; i++) {
            let num: number = i + 1;
            delStartTmp[i]['id'] = num;
            if (i === delStartTmp.length - 1) {
                delStartTmp[i]['startCmdFlg'] = false;
                if (delStartTmp.length === 1) {
                    this.startTrashBinFlg = true;
                } else {
                    this.startTrashBinFlg = false;
                }
            }
        }
        this.startCmds = delStartTmp;
    }
    startServer() {
        this.loadingStart = true;
        let startUrl = '/api/v1/server/?operations=start';
        this.http.get(startUrl)
            .map(res => res.json())
            .catch(error => Observable.throw(error))
            .subscribe(res => {
                this.loadingStart = false;
                if (res && res['status'].toString() === 'success') {
                    alert(res['message']);
                } else {
                    alert('Start server failed');
                }
            });
    }
    stopServer() {
        this.loadingStop = true;
        let stopUrl = '/api/v1/server/?operations=stop';
        this.http.get(stopUrl)
            .map(res => res.json())
            .catch(error => Observable.throw(error))
            .subscribe(res => {
                this.loadingStop = false;
                if (res && res['status'].toString() === 'success') {
                    alert(res['message']);
                } else {
                    alert('Stop server failed');
                }
            });
    }
    restartServer() {
        this.loadingRestart = true;
        let restartUrl = '/api/v1/server/?operations=restart';
        this.http.get(restartUrl)
            .map(res => res.json())
            .catch(error => Observable.throw(error))
            .subscribe(res => {
                this.loadingRestart = false;
                if (res && res['status'].toString() === 'success') {
                    alert(res['message']);
                } else {
                    alert('Restart server failed');
                }
            });
    }
    public changeFile(files: FileList) {
        if (files && files.length > 0) {
            let file: File = files.item(0);
            let fileType = file.type;
            this.filename = file.name;
            this.formData = new FormData();
            this.formData.append('file', file);
            if (this.filename === 'config.csv') {
                this.uploadFlg = 'csv';
                this.loginFlg = false;
            } else {
                this.uploadFlg = 'other';
                this.loginFlg = true;
            }
        } else {
            if (this.filename) {
                this.loginFlg = false;
            } else {
                this.loginFlg = true;
            }
        }
    }
    public uploadFile() {
        let uploadUrl = '/api/v1/server/';
        this.loadingUpload = true;
        this.http.post(uploadUrl, this.formData)
            .map(res => res.json())
            .catch(error => Observable.throw(error))
            .subscribe(res => {
                this.loadingUpload = false;
                if (res && res['status'].toString() === 'success') {
                    alert('Import the config.csv file succeed');
                } else {
                    alert('Import the config.csv file failed');
                }
            });
    }
    public doCheck() {
        let starts = _.cloneDeep(this.startCmds);
        this.startRegFlg = this.multiStartCmdRegFomatter(starts);
        this.portNotNull = Validator.notNullCheck(this.port);
        if (this.portNotNull) {
            this.portFlg = Validator.numRegCheck(this.port);
        }
        this.expectNotNull = Validator.notNullCheck(this.expect);
        if (this.expectNotNull) {
            this.expectFlg = Validator.halfWidthReg(this.expect);
        }
        if (this.portNotNull && this.portFlg
            && this.expectNotNull && this.expectFlg
            && this.startRegFlg) {
            return true;
        } else {
            return false;
        }
    }
    public multiStartCmdRegFomatter(multiStartCmds: any) {
        let regFlgTmp = true;
        _.each(multiStartCmds, function (value) {
            return value['name'] = value['name'].trim();
        });
        _.remove(multiStartCmds, function (value) {
            return value['name'] === '';
        });
        let uniqData: any = [];
        // uniqData = _.uniqBy(multiStartCmds, 'name');
        uniqData = _.cloneDeep(multiStartCmds);
        let len = uniqData.length;
        if (len > 0) {
            for (let i = 0; i < uniqData.length; i++) {
                if (Validator.halfWidthReg(uniqData[i].name)) {
                    uniqData[i].startRegFlg = true;
                } else {
                    uniqData[i].startRegFlg = false;
                    regFlgTmp = false;
                }
            }
            uniqData[len - 1]['startCmdFlg'] = false;
        } else {
            let startInitTmp: any = this.startCmdsInit();
            startInitTmp['startRegFlg'] = false;
            uniqData.push(startInitTmp);
            regFlgTmp = false;
        }
        if (uniqData.length === 1) {
            this.startTrashBinFlg = true;
        } else {
            this.startTrashBinFlg = false;
        }
        this.startCmds = _.cloneDeep(uniqData);
        return regFlgTmp;
    }
    queryOutput() {
        this.outputs = [];
        if (this.doCheck()) {
            this.loadingQuery = true;
            let queryInfo: any = {
                'commands': this.startCmds,
                'port': parseInt(this.port, 0),
                'expect': this.expect
            };
            this.http.post('/api/v1/collection/', queryInfo)
                .map(res => res.json())
                .catch(error => Observable.throw(error))
                .subscribe(res => {
                    this.loadingQuery = false;
                    if (res && res['status'].toString() === 'success') {
                        this.outputs = res['output'];
                    } else {
                        alert(res['message']);
                    }
                });
        }
    }
}
