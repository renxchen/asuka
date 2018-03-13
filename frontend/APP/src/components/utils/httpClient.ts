import { Component, Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import * as _ from 'lodash';
import { Router } from '@angular/router';
@Injectable()

export class HttpClientComponent {
  token: string;
  http: Http;
  apiPrefix: String = '';
  headers: Headers;
  constructor(
    http: Http,
    public router: Router
  ) {
    this.http = http;
    this.token = localStorage.getItem('token');
  }

  private checkAuthorization(url: string): Boolean {
    if (!localStorage.getItem('token') ||
      localStorage.getItem('token') === '' ||
      typeof (localStorage.getItem('token')) === 'undefined') {
      if (url.indexOf('login') !== -1) {
        return true;
      } else {
        return false;
      }
    }
    return true;
  }
  private createAuthorizationHeader(headers: Headers, headerData: any = {}, method?: any) {
    if (method !== 0) {
      headers.append('Content-Type', 'application/json');
    }
    headers.append('dataType', 'json');
    headers.append('token', localStorage.getItem('token'));
    // tslint:disable-next-line:forin
    for (let k in headerData) {
      headers.append(k, encodeURI(headerData[k]));
    }
  }

  public setUrl(url: String) {
    this.apiPrefix = url;
  }

  private getApiUrl(search: string): string {
    return `${this.apiPrefix}${search}`;
  }

  public getSearchParams(): any {
    let href = window.location.href;
    let href_search: any = href.split('?');
    if (href_search.length > 1) {
      href_search = href_search.pop();
    } else {
      return {};
    }
    let search_params: any[] = href_search.split('&');
    let params: any = {};
    _.each(search_params, (sp: any) => {
      let key_val = sp.split('=');
      if (key_val.length > 1) {
        params[key_val[0]] = key_val[1];
      }
    });
    return params;
  }

  public toJson(resObs: Observable<any>, obj?: any): Observable<any> {
    if (resObs) {
      return resObs.flatMap((res: any) => {
        let content = res['_body'];
        let ret: any = {};
        ret = !obj ? JSON.parse(content) : _.extend(JSON.parse(content), obj);
        if (ret.status) {
          localStorage.setItem('sessionTimeOut', '');
          return Observable.of(ret);
        } else if (ret.new_toke || ret.token) {
          let token = ret.new_toke || ret.token;
          localStorage.setItem('sessionTimeOut', '');
          if (token) {
            if (token.code === 102) {
              localStorage.setItem('sessionTimeOut', token.message);
              this.router.navigate(['/login'], { queryParams: this.getSearchParams()});
            }
          } else if (token.code === 103) {
            localStorage.setItem('sessionTimeOut', token.message);
            this.router.navigate(['/login'], { queryParams: this.getSearchParams()});
          }
          localStorage.setItem('requestFailed', '');
          return Observable.of(ret);
        }
      })
        .map(v => v)
        .catch((res: any) => {
          if (localStorage.getItem('requestFailed') !== 'failed') {
            alert('Request failed! Please contact the administrator.');
          }
          localStorage.setItem('requestFailed', 'failed');
          return Observable.of({
            'meta': {
              'status': true,
              'message': '网络状况异常。'
            },
            'data': null
          });
        });
    } else {
      let ret: any = { 'meta': { 'status': true } };
      localStorage.setItem('sessionTimeOut', '无权访问或用户过期，请重新登录.');
      this.router.navigate(['/login'], { queryParams: this.getSearchParams() });
      return Observable.of(ret);
    }
  }

  public get(url: string, headerData: any = {}) {
    let headers = new Headers();
    if (this.checkAuthorization(url)) {
      this.createAuthorizationHeader(headers, headerData, 0);
      return this.http.get(
        this.getApiUrl(url),
        {
           headers: headers
        }
      );
    } else {
      let ret: any = { 'meta': { 'status': true } };
      localStorage.setItem('sessionTimeOut', '无权访问或用户过期，请重新登录.');
      this.router.navigate(['login'], { queryParams: this.getSearchParams() });
    }
  }

  public post(url: string, data: any, headerData: any = {}) {
    let headers = new Headers();
    if (this.checkAuthorization(url)) {
      this.createAuthorizationHeader(headers, headerData);
      return this.http.post(
        this.getApiUrl(url),
        data,
        { headers: headers }
      );
    }

  }

  public put(url: string, data: any, headerData: any = {}) {
    let headers = new Headers();

    if (this.checkAuthorization(url)) {
      this.createAuthorizationHeader(headers, headerData);
      return this.http.put(
        this.getApiUrl(url),
        data,
        {
          headers: headers
        });
    }
  }

  public delete(url: string, headerData: any = {}, data: any = {}) {
    let headers = new Headers();
    if (this.checkAuthorization(url)) {
      this.createAuthorizationHeader(headers, headerData);
      return this.http.delete(
        this.getApiUrl(url),
        {
          headers: headers
        });
    }
  }

  public patch(url: string, data: any, headerData: any = {}) {
    let headers = new Headers();
    if (this.checkAuthorization(url)) {
      this.createAuthorizationHeader(headers, headerData);
      return this.http.patch(
        this.getApiUrl(url),
        data,
        {
          headers: headers
        });
    }
  }
}
