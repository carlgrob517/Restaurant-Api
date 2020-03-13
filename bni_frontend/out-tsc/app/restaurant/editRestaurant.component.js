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
var EditResComponent = /** @class */ (function () {
    function EditResComponent(service, route, router) {
        this.service = service;
        this.route = route;
        this.router = router;
        this.model = {};
    }
    EditResComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.route.params.subscribe(function (params) {
            _this.id = params.id;
            _this.service.getById(_this.id)
                .subscribe(function (data) {
                _this.model = data;
                _this.model.password = '';
            }, function (err) {
            });
        });
    };
    EditResComponent.prototype.update = function () {
        var _this = this;
        this.service.update(this.model)
            .subscribe(function (data) {
            _this.router.navigate(['home']);
        }, function (error) {
        });
    };
    EditResComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['editRestaurant.component.scss'],
            templateUrl: 'editRestaurant.component.html'
        }),
        __metadata("design:paramtypes", [index_1.RestaurantService,
            router_1.ActivatedRoute,
            router_1.Router])
    ], EditResComponent);
    return EditResComponent;
}());
exports.EditResComponent = EditResComponent;
//# sourceMappingURL=editRestaurant.component.js.map