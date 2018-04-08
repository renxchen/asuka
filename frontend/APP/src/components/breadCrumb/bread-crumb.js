"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
var core_1 = require("@angular/core");
var router_1 = require("@angular/router");
var _ = require("lodash");
var BreadCrumb = (function () {
    function BreadCrumb(_router, route) {
        var _this = this;
        this._router = _router;
        this.route = route;
        this.breadcrumbs = [];
        this._router.events.filter(function (o) {
            return o instanceof router_1.NavigationEnd;
        }).subscribe(function (eventData) {
            var currentRoute = _this.route.root, url = '';
            do {
                var childrenRoutes = currentRoute.children;
                currentRoute = null;
                childrenRoutes.forEach(function (_route) {
                    if (route.outlet === 'primary') {
                        var routeSnapshot = _route.snapshot;
                        url += '/' + routeSnapshot.url.map(function (segment) { return segment.path; }).join('/');
                        if (_.get(routeSnapshot.data || {}, 'title')) {
                            _this.breadcrumbs.push({
                                label: _.get(routeSnapshot.data || {}, 'title'),
                                url: url
                            });
                        }
                        currentRoute = _route;
                    }
                });
            } while (currentRoute);
            var len = _this.breadcrumbs.length;
            _this.breadcrumbs = _.uniqWith(_.reverse(_this.breadcrumbs), function (o, n) {
                return o.url === n.url;
            });
            _this.breadcrumbs = _.reverse(_this.breadcrumbs);
            _this.breadcrumbs = _.slice(_this.breadcrumbs, len - 10, 8);
            _this.title = _.get(_.last(_this.breadcrumbs), 'label');
        });
    }
    BreadCrumb = __decorate([
        core_1.Component({
            selector: 'bread-crumb',
            templateUrl: 'app/assets/BreadCrumb/bread-crumb.html',
            styleUrls: ['app/assets/BreadCrumb/bread-crumb.css']
        }),
        __metadata("design:paramtypes", [router_1.Router, router_1.ActivatedRoute])
    ], BreadCrumb);
    return BreadCrumb;
}());
exports.BreadCrumb = BreadCrumb;

//# sourceMappingURL=bread-crumb.js.map
