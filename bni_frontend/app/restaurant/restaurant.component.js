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
var RestaurantComponent = /** @class */ (function () {
    function RestaurantComponent(service, router, pagerService) {
        this.service = service;
        this.router = router;
        this.pagerService = pagerService;
        this.restaurants = [];
        // pager object
        this.pager = {};
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }
    RestaurantComponent.prototype.ngOnInit = function () {
        this.loadAllRestaurants();
    };
    RestaurantComponent.prototype.delete = function (id) {
        var _this = this;
        this.service.delete(id).subscribe(function () { _this.loadAllRestaurants(); });
    };
    RestaurantComponent.prototype.edit = function (id) {
        this.router.navigate(['restaurant/edit', id]);
    };
    RestaurantComponent.prototype.add = function () {
        this.router.navigate(['restaurant/add']);
    };
    RestaurantComponent.prototype.loadAllRestaurants = function () {
        var _this = this;
        this.service.getAll({ page: 1, search: '', name: '', location: '', rating: '' })
            .subscribe(function (data) {
            _this.restaurants = data;
            console.log(data);
            _this.setPage(1);
        });
    };
    RestaurantComponent.prototype.setPage = function (page) {
        // get pager object from service
        this.pager = this.pagerService.getPager(this.restaurants.length, page);
        // get current page of items
        this.pagedItems = this.restaurants.slice(this.pager.startIndex, this.pager.endIndex + 1);
    };
    RestaurantComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['restaurant.component.scss'],
            templateUrl: 'restaurant.component.html'
        }),
        __metadata("design:paramtypes", [index_1.RestaurantService,
            router_1.Router,
            index_1.PagerService])
    ], RestaurantComponent);
    return RestaurantComponent;
}());
exports.RestaurantComponent = RestaurantComponent;
//# sourceMappingURL=restaurant.component.js.map