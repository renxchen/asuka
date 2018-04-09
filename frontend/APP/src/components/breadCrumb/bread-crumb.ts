import { Component } from '@angular/core';
import { Router, NavigationEnd, ActivatedRoute } from '@angular/router';
import * as _ from 'lodash';

@Component({
    selector: 'bread-crumb',
    templateUrl: 'bread-crumb.html',
    styleUrls: ['bread-crumb.less']
})

export class BreadCrumbComponent {
    title: string | Object;
    breadcrumbs: any[] = [];
    pathObj: any;
    constructor(private _router: Router, private route: ActivatedRoute) {
        this._router.events.filter(o => {
            return o instanceof NavigationEnd;
        }).subscribe(eventData => {
            let currentRoute = this.route.root,
                url = '';
            do {
                let childrenRoutes = currentRoute.children;
                currentRoute = null;
                childrenRoutes.forEach(_route => {
                    if (route.outlet === 'primary') {
                        let routeSnapshot = _route.snapshot;
                        url += '/' + routeSnapshot.url.map(segment => segment.path).join('/');
                        let labelTitle = '';
                        let labelParent = '';
                        // let label = '';
                        if (_.get(routeSnapshot.data || {}, 'title') && _.get(routeSnapshot.data || {}, 'parentTitle')) {
                            labelParent = _.get(routeSnapshot.data || {}, 'parentTitle');
                            labelTitle = _.get(routeSnapshot.data || {}, 'title');
                            // label = labelParent + '/' + labelTitle;
                        }
                        if (_.get(routeSnapshot.data || {}, 'title')) {
                            this.breadcrumbs.push({
                                label: _.get(routeSnapshot.data || {}, 'title'),
                                url: url,
                                labelParent : _.get(routeSnapshot.data || {}, 'parentTitle'),
                                labelTitle : _.get(routeSnapshot.data || {}, 'title')
                                // pathLabel: label
                            });
                        }
                        currentRoute = _route;
                    }
                });
            } while (currentRoute);
            let len = this.breadcrumbs.length;
            this.breadcrumbs = _.uniqWith(_.reverse(this.breadcrumbs), (o: any, n: any) => {
                return o.url === n.url;
            });
            this.breadcrumbs = _.reverse(this.breadcrumbs);
            this.breadcrumbs = _.slice(this.breadcrumbs, len - 10, 8);
            if (this.breadcrumbs && this.breadcrumbs.length > 0) {
                this.pathObj = _.last(this.breadcrumbs);
                this.title = _.get(this.pathObj, 'labelTitle');
            }
        });
    }
}
