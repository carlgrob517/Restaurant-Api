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
var HeaderComponent = /** @class */ (function () {
    function HeaderComponent(authService, router) {
        this.authService = authService;
        this.router = router;
        this.users = [];
        this.isLogin = false;
        this.role = '';
    }
    HeaderComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.check();
        this.timerId = setInterval(function () {
            _this.check();
        }, 500);
    };
    HeaderComponent.prototype.ngOnDestroy = function () {
        if (this.timerId) {
            clearInterval(this.timerId);
        }
    };
    HeaderComponent.prototype.logout = function () {
        this.authService.logout();
        this.router.navigate(['login']);
    };
    HeaderComponent.prototype.login = function () {
        this.authService.logout();
        this.router.navigate(['login']);
    };
    HeaderComponent.prototype.register = function () {
        this.authService.logout();
        this.router.navigate(['register']);
    };
    HeaderComponent.prototype.check = function () {
        if (localStorage.getItem('currentUser')) {
            this.isLogin = true;
            this.role = JSON.parse(localStorage.getItem('role'));
            if (this.role === 'admin')
                console.log(this.isLogin, this.role);
        }
        else
            this.isLogin = false;
    };
    HeaderComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            'selector': 'menu',
            styleUrls: ['header.component.scss'],
            templateUrl: 'header.component.html'
        }),
        __metadata("design:paramtypes", [index_1.AuthenticationService,
            router_1.Router])
    ], HeaderComponent);
    return HeaderComponent;
}());
exports.HeaderComponent = HeaderComponent;
//# sourceMappingURL=header.component.js.map