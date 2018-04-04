import { Component, OnInit, AfterViewInit } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
// import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';

@Component({
  selector: 'data-table-login',
  templateUrl: 'dataTableLogin.component.html',
  styleUrls: ['actionPolicy.component.less']
})
export class DataTableLoginComponent implements OnInit, AfterViewInit {
  apiPrefix: any = '/v1';
  title: string;

  currentStep = 1;
  maxStep = 1;
  timeOut: any;
  sendData: any = {};
  btnFlgs = {
    btnPrev: false,
    btnNext: true,
    btnFinished: false
  };
  validFlgs = {
    tableNameExsit: false
  };

  tableName: string;
  description: any;
  selectedDeviceGroup;


  constructor(
    public httpClient: HttpClientComponent,
    public bsModalRef: BsModalRef
  ) { }

  ngOnInit() {
    this.httpClient.setUrl(this.apiPrefix);


  }

  ngAfterViewInit() {
    this.setBottomBtns();
    setTimeout(() => {

      // $('#validPeriod').hide();
      // $('#dataSchedule').hide();
      // if(this.id == -1){
      //     this.getOsTypes();
      //     this.setInitSelect();
      //     $('button.btn-danger').hide();
      // } else {
      //     this.getDetailById(this.id);
      // }
    }, 0);
  }

  public next() {
    /*
      when click next icon btn ,step ++
    */
    this.currentStep++;
    this.maxStep === 4 ? this.maxStep = 4 : this.maxStep++;
    this.setBottomBtns();
  }

  public previous() {
    /*
      when click prev icon btn ,step --
    */
    this.currentStep--;
    this.setBottomBtns();
  }

  public setBottomBtns() {
    /*
      set bottom (prev next finished) btn status,disabled or not ,
      call : afterviewinit and next 、previous
    */
    this.vaild();
    if (this.currentStep === 1) {
      this.btnFlgs.btnNext = this.validFlgs.tableNameExsit;
      console.log('this.btnFlgs.btnNext', this.btnFlgs.btnNext);
      this.btnFlgs.btnPrev = false;
    } else {
      this.btnFlgs.btnPrev = true;
    }
    if (this.currentStep === 4) {
      this.btnFlgs.btnNext = false;
      this.btnFlgs.btnFinished = true;
    }

  }

  public checkTableNameValidation() {
    /*
      check this.tableName vilidaty(repeat,exit)
    */
    let _t = this;
    if (this.tableName) {
      this.validFlgs.tableNameExsit = true;
      this.setBottomBtns();
      clearTimeout(this.timeOut);
      this.timeOut = setTimeout(function () {
        let url = '/api_data_table_name_verify/?name=' + _t.tableName + '/';
        _t.get(url).subscribe((res: any) => {
          console.log('res', res);
        });

      }, 2000);
    }

  }

  public vaild() {
    /*
      vaild function
      {valid value: tableName,
      call： finish click},
      {vaild:tableName exsit,
      call:afterViewInit}

      }
      */
    if (this.tableName) {
      this.validFlgs.tableNameExsit = true;
    } else {
      this.validFlgs.tableNameExsit = false;
    }
  }

  public setSteps(step: number) {
    this.currentStep = step;
  }

  // common function of http

  private get(url: string) {
    return this.httpClient.toJson(this.httpClient.get(url));
  }

  private post(url: string, bodyData: any) {
    return this.httpClient.toJson(this.httpClient.post(url, bodyData));
  }
  private put(url: string, bodyData: any) {
    return this.httpClient.toJson(this.httpClient.put(url, bodyData));
  }

  private delete(url: string) {
    return this.httpClient.toJson(this.httpClient.delete(url));
  }
}
