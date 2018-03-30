import { Component, OnInit, AfterViewInit } from '@angular/core';
import { HttpClientComponent } from '../utils/httpClient';
import { Router } from '@angular/router';

@Component({
    selector: 'not-found',
    templateUrl: './notFount.component.html'
})
export class NotFoundComponent implements OnInit, AfterViewInit {
    constructor(public router: Router,
        public httpClient: HttpClientComponent) { }

    public ngOnInit() { }

    public ngAfterViewInit(): void { }

    logout() {
        this.httpClient.setUrl('/v1');
        this.
            httpClient
            .toJson(this.httpClient.delete('/logout/'))
            .subscribe(res => {
                if (res['status'] && res['status']['status'].toLowerCase() === 'true') {
                    localStorage.removeItem('token');
                    localStorage.removeItem('sessionTimeOut');
                    this.router.navigate(['/login/']);
                }

            });
    }

}
