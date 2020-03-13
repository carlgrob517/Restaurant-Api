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
var http_1 = require("@angular/common/http");
var RestaurantService = /** @class */ (function () {
    function RestaurantService(http) {
        this.http = http;
        this.url = 'http://localhost:5000';
    }
    RestaurantService.prototype.getAll = function (query) {
        return this.http.get(this.url + ("/api/restaurants?page=" + query.page + "&search=" + query.search + "&name=" + query.name + "&location=" + query.location + "&rating=" + query.rating));
    };
    RestaurantService.prototype.getById = function (id) {
        return this.http.get(this.url + '/api/restaurants/' + id);
    };
    RestaurantService.prototype.create = function (data) {
        return this.http.post(this.url + '/api/restaurants/add', data);
    };
    RestaurantService.prototype.update = function (data) {
        return this.http.put(this.url + '/api/restaurants/update', data);
    };
    RestaurantService.prototype.delete = function (id) {
        return this.http.delete(this.url + '/api/restaurants/delete/' + id);
    };
    RestaurantService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [http_1.HttpClient])
    ], RestaurantService);
    return RestaurantService;
}());
exports.RestaurantService = RestaurantService;
//# sourceMappingURL=restaurant.service.js.map