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
var ProfileComponent = /** @class */ (function () {
    function ProfileComponent(reviewService, route) {
        this.reviewService = reviewService;
        this.route = route;
        this.reviews = [];
    }
    ProfileComponent.prototype.ngOnInit = function () {
        var id = JSON.parse(localStorage.getItem('currentUser'));
        console.log(id);
        this.loadAllReviews(id);
    };
    ProfileComponent.prototype.deleteReview = function (id) {
        var _this = this;
        console.log('clicked');
        this.reviewService.delete(id).subscribe(function () { _this.loadAllReviews(); });
    };
    ProfileComponent.prototype.loadAllReviews = function (id) {
        var _this = this;
        if (id === void 0) { id = ''; }
        this.reviewService.getByUserId(id).subscribe(function (reviews) { _this.reviews = reviews; console.log(reviews); });
    };
    ProfileComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['profile.component.scss'],
            templateUrl: 'profile.component.html'
        }),
        __metadata("design:paramtypes", [index_1.ReviewService,
            router_1.ActivatedRoute])
    ], ProfileComponent);
    return ProfileComponent;
}());
exports.ProfileComponent = ProfileComponent;
//# sourceMappingURL=profile.component.js.map