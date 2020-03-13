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
var AddResComponent = /** @class */ (function () {
    function AddResComponent(service, router) {
        this.service = service;
        this.router = router;
        this.model = {};
    }
    AddResComponent.prototype.ngOnInit = function () {
    };
    AddResComponent.prototype.save = function () {
        var _this = this;
        this.service.create(this.model)
            .subscribe(function (data) {
            _this.router.navigate(['restaurant']);
        }, function (error) {
        });
    };
    AddResComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['addRestaurant.component.scss'],
            templateUrl: 'addRestaurant.component.html'
        }),
        __metadata("design:paramtypes", [index_1.RestaurantService,
            router_1.Router])
    ], AddResComponent);
    return AddResComponent;
}());
exports.AddResComponent = AddResComponent;
//# sourceMappingURL=addRestaurant.component.js.map