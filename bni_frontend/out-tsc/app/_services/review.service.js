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
var ReviewService = /** @class */ (function () {
    function ReviewService(http) {
        this.http = http;
        this.url = 'http://localhost:5000';
    }
    ReviewService.prototype.getAll = function (id) {
        return this.http.get(this.url + '/api/reviews?restaurant_id=' + id);
    };
    ReviewService.prototype.getByUserId = function (id) {
        return this.http.get(this.url + '/api/reviews/getByUserId?user_id=' + id);
    };
    ReviewService.prototype.getById = function (id) {
        return this.http.get(this.url + '/api/reviews/' + id);
    };
    ReviewService.prototype.create = function (review) {
        return this.http.post(this.url + '/api/reviews/add', review);
    };
    ReviewService.prototype.update = function (review) {
        return this.http.put(this.url + '/api/reviews/update' + review._id, review);
    };
    ReviewService.prototype.delete = function (id) {
        return this.http.delete(this.url + '/api/reviews/delete/' + id);
    };
    ReviewService = __decorate([
        core_1.Injectable(),
        __metadata("design:paramtypes", [http_1.HttpClient])
    ], ReviewService);
    return ReviewService;
}());
exports.ReviewService = ReviewService;
//# sourceMappingURL=review.service.js.map