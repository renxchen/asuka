import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { NavigationStart } from '@angular/router';
import { Http } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import * as _ from 'lodash';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.less']
})
export class AppComponent {
  title = 'app';
  constructor(
    private router: Router,
    private http: Http) {
    let href: String = window.location.href;
    router.events.subscribe(event => {
        if (event instanceof NavigationStart) {
            if (href.indexOf('/login') < 0) {
                this.http.get('/v1/api_permission_auth/')
                    .map(res => res.json())
                    .catch(error => Observable.throw(error))
                    .subscribe(res => {
                        let status = _.get(res, 'status');
                        if (status && status['status'].toString().toLowerCase() === 'false') {
                            router.navigate(['/login']);
                        }
                    });
                }
            }
        });
    }
}
