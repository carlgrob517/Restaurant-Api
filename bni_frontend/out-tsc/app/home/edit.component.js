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
var EditComponent = /** @class */ (function () {
    function EditComponent(userService, route, router) {
        this.userService = userService;
        this.route = route;
        this.router = router;
        this.model = {};
    }
    EditComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.route.params.subscribe(function (params) {
            _this.id = params.id;
            _this.userService.getById(_this.id)
                .subscribe(function (data) {
                _this.model = data;
                _this.model.password = '';
            }, function (err) {
            });
        });
    };
    EditComponent.prototype.updateUser = function (id) {
        var _this = this;
        this.userService.update(this.model)
            .subscribe(function (data) {
            _this.router.navigate(['home']);
        }, function (error) {
        });
    };
    EditComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['edit.component.scss'],
            templateUrl: 'edit.component.html'
        }),
        __metadata("design:paramtypes", [index_1.UserService,
            router_1.ActivatedRoute,
            router_1.Router])
    ], EditComponent);
    return EditComponent;
}());
exports.EditComponent = EditComponent;
//# sourceMappingURL=edit.component.js.map