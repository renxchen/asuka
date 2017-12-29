import { Injectable, ElementRef } from '@angular/core';
import * as $ from 'jquery';
import { Observable } from 'rxjs/Rx';
import { HttpClientComponent } from '../../components/utils/httpClient';
@Injectable()
export class IndexService {
    http: HttpClientComponent;
    apiPrefix: String = '/v1';
    constructor(httpClient: HttpClientComponent) {
        this.http = httpClient;
    }
    public get(url: string, header: any = {}) {
        this.http.setUrl(this.apiPrefix);
        return this.http.toJson(this.http.get(url, header));
    }
    public logout(headerData?: any) {
        this.http.setUrl(this.apiPrefix);
        return this.http.toJson(this.http.delete('/logout/'));
    }
}
