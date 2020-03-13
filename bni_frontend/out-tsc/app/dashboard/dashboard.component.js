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
var index_1 = require("../_services/index");
var DashboardComponent = /** @class */ (function () {
    function DashboardComponent(service, pagerService, router) {
        this.service = service;
        this.pagerService = pagerService;
        this.router = router;
        this.restaurants = [];
        this.model = {
            searchStr: '',
            name: '',
            location: '',
            rating: '',
        };
        this.page = 1;
        this.pageSize = 10;
        this.total = 0;
        this.showDetailsSearch = false;
        this.loading = false;
        // pager object
        this.pager = {};
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }
    DashboardComponent.prototype.ngOnInit = function () {
        this.search();
    };
    DashboardComponent.prototype.search = function () {
        var _this = this;
        this.loading = true;
        this.service.getAll({ page: this.page, search: this.model.searchStr, name: '', location: '', rating: '' })
            .subscribe(function (data) {
            _this.total = data.length;
            _this.restaurants = data;
            _this.loading = false;
            console.log(data);
            _this.setPage(1);
        }, function (error) {
        });
    };
    DashboardComponent.prototype.each_search = function (info) {
        console.log(this.restaurants);
        this.router.navigate(['review/add'], { queryParams: { 'id': info._id['$oid'] } });
    };
    DashboardComponent.prototype.searchByDetails = function () {
        var _this = this;
        this.loading = true;
        this.service.getAll({ page: this.page, search: '', name: this.model.name, location: this.model.location, rating: this.model.rating })
            .subscribe(function (data) {
            _this.total = data.length;
            _this.restaurants = data;
            _this.loading = false;
            console.log(_this.restaurants);
            _this.setPage(1);
        }, function (error) {
        });
    };
    DashboardComponent.prototype.write = function (info) {
        console.log();
        this.router.navigate(['review/add'], { queryParams: { 'id': info._id['$oid'] } });
    };
    DashboardComponent.prototype.viewAll = function (id) {
        this.router.navigate(['/review'], { queryParams: { 'id': id } });
    };
    DashboardComponent.prototype.toggleDetailSearch = function () {
        this.showDetailsSearch = !this.showDetailsSearch;
    };
    DashboardComponent.prototype.setPage = function (page) {
        // get pager object from service
        this.pager = this.pagerService.getPager(this.restaurants.length, page);
        // get current page of items
        this.pagedItems = this.restaurants.slice(this.pager.startIndex, this.pager.endIndex + 1);
    };
    DashboardComponent.prototype.getRepeatArray = function (count) {
        var arr = [];
        for (var i = 0; i < count; i++)
            arr.push(i);
        return arr;
    };
    DashboardComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['dashboard.component.scss'],
            templateUrl: 'dashboard.component.html'
        }),
        __metadata("design:paramtypes", [index_1.RestaurantService,
            index_1.PagerService,
            router_1.Router])
    ], DashboardComponent);
    return DashboardComponent;
}());
exports.DashboardComponent = DashboardComponent;
//# sourceMappingURL=dashboard.component.js.map