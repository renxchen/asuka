import { Component, OnInit, AfterViewInit, ElementRef } from '@angular/core';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClientComponent } from '../../components/utils/httpClient';
declare var $: any;
import * as _ from 'lodash';
import * as moment from 'moment';
import * as flatpickr from 'flatpickr';

@Component({
  selector: 'data-table-detail',
  templateUrl: 'dataTableDetail.component.html',
  styleUrls: ['actionPolicy.component.less']
})
export class DataTableDetailComponent implements OnInit, AfterViewInit {
  tableName: string;
  apiPrefix: String = '/v1';
  contentData: any;
  startTime: any;
  endTime: any;
  flatPickrStartTime: any;
  flatPickrEndTime: any;


  constructor(
    public httpClient: HttpClientComponent,
    public router: Router,
    private route: ActivatedRoute,
    public bsModalRef: BsModalRef,
    public elementRef: ElementRef
  ) { }

  public ngOnInit() {
    this.httpClient.setUrl(this.apiPrefix);
  }

  public ngAfterViewInit() {
    let _t = this;
    this.setPopUpSize();
    setTimeout(() => {
      _t.tableName = _t.contentData['name'];
      console.log('this.contentData!', _t.contentData);
    }, 0);
    this.initPickr();
  }

  protected setPopUpSize() {
    $('#detail-popup').parents('div.modal-content').css('width', '701px');

  }

  public drawDetailTable() {

    let testData = [
      {
        'date': '2018-01-16 17:24:52',
        'path': null,
        'hostname': 'test-device02',
        'checkitem': 'IF_NAME2',
        'value': 91
      },
      {
        'date': '2018-01-16 18:24:52',
        'path': null,
        'hostname': 'test-device03',
        'checkitem': 'IF_NAME3',
        'value': 92
      },
      {
        'date': '2018-01-16 19:24:52',
        'path': null,
        'hostname': 'test-device04',
        'checkitem': 'IF_NAME4',
        'value': 93
      }, {
        'date': '2018-01-16 20:24:52',
        'path': null,
        'hostname': 'test-device05',
        'checkitem': 'IF_NAME5',
        'value': 94
      },
      {
        'date': '2018-01-16 21:24:52',
        'path': null,
        'hostname': 'test-device06',
        'checkitem': 'IF_NAME6',
        'value': 95
      }

    ];
  }

  protected initPickr() {
    let option: any = {
      enableTime: true
    };
    let startEle = document.getElementById('startTimeInput');
    let endEle = document.getElementById('endTimeInput');
    let flatPickrStartTime: any = new flatpickr(startEle, option);
  }

}
