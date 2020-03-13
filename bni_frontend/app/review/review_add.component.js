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
var ReviewAddComponent = /** @class */ (function () {
    function ReviewAddComponent(router, route, reviewService, restaurantService, alertService) {
        this.router = router;
        this.route = route;
        this.reviewService = reviewService;
        this.restaurantService = restaurantService;
        this.alertService = alertService;
        this.model = {
            'user_id': 'user',
            'restaurant_id': 'res',
            'vote': '',
        };
        this.reviewModel = {};
        this.info = {};
        this.loading = false;
        this.showSpinner = false;
        this.status = [false, false, false, false, false];
        this.offset = 0;
        this.isGoogle = true;
        this.isViewMore = true;
    }
    ReviewAddComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.model.user_id = JSON.parse(localStorage.getItem('currentUser'));
        // console.log(this.model.user_id);
        this.route.queryParams.subscribe(function (params) {
            var id = params['id'];
            _this.restaurantService.getById(id).subscribe(function (data) {
                _this.info = data;
                _this.model['restaurant_id'] = _this.info._id['$oid'];
                console.log(_this.viewMoreModel);
                if (_this.info.google_location_id == "" && _this.info.tripadvisor_location_id == "") {
                    _this.isViewMore = false;
                }
                else if (_this.info.google_location_id == "") {
                    _this.isGoogle = false;
                }
                setTimeout(function () {
                    _this.map = new google.maps.Map(_this.mapRef.nativeElement, {
                        zoom: 10,
                        center: { lat: _this.info.coordinates.latitude, lng: _this.info.coordinates.longitude }
                    });
                    _this.marker = new google.maps.Marker({
                        position: { lat: _this.info.coordinates.latitude, lng: _this.info.coordinates.longitude },
                        map: _this.map
                    });
                }, 2000);
            });
        });
    };
    ReviewAddComponent.prototype.set_rating = function (e) {
        // @ts-ignore
        var result = parseInt(e.target.value);
        for (var i = 0; i < this.status.length; i++) {
            this.status[i] = false;
        }
        // @ts-ignore
        this.status[result - 1] = true;
    };
    ReviewAddComponent.prototype.viewMore = function () {
        var _this = this;
        if (this.isGoogle && this.model.google_location_id == "") {
            this.isViewMore = false;
            return;
        }
        if (!this.isGoogle && this.model.tripadvisor_location_id == "") {
            this.isViewMore = false;
            return;
        }
        if (this.isGoogle) {
            this.viewMoreModel = {
                query: this.info.alias,
                offset: this.offset,
                id: this.info._id['$oid'],
                location_id: this.info.google_location_id ? this.info.google_location_id : '',
                type: 'google'
            };
        }
        else {
            this.viewMoreModel = {
                query: this.info.alias,
                offset: this.offset,
                id: this.info._id['$oid'],
                location_id: this.info.tripadvisor_location_id ? this.info.tripadvisor_location_id : '',
                type: 'tripadvisor'
            };
        }
        if (!this.isGoogle && this.info.tripadvisor_location_id == '') {
            this.isViewMore = false;
            return;
        }
        this.showSpinner = true;
        this.reviewService.viewMore(this.viewMoreModel)
            .subscribe(function (data) {
            var reviews = _this.info.id_review.reviews;
            console.log(data);
            for (var i = 0; i < data.length; i++) {
                reviews.push(data[i]);
            }
            if (data.length < 5 || _this.info.tripadvisor_location_id == "") {
                _this.isViewMore = false;
            }
            reviews.sort(function (a, b) { return (a.rating > b.rating) ? -1 : 1; });
            _this.info.id_review.reviews = reviews;
            _this.offset = _this.offset + 1;
            _this.showSpinner = false;
            //window.scroll(0,window.innerHeight);
            _this.isGoogle = false;
        }, function (error) {
            _this.showSpinner = false;
            console.log("aaah");
        });
    };
    ReviewAddComponent.prototype.addReview = function () {
        var _this = this;
        this.loading = true;
        this.reviewService.create(this.model)
            .subscribe(function (data) {
            _this.router.navigate(['review']);
        }, function (error) {
            _this.loading = false;
        });
    };
    __decorate([
        core_1.ViewChild('map'),
        __metadata("design:type", core_1.ElementRef)
    ], ReviewAddComponent.prototype, "mapRef", void 0);
    ReviewAddComponent = __decorate([
        core_1.Component({
            moduleId: module.id,
            styleUrls: ['review_add.component.scss'],
            templateUrl: 'review_add.component.html'
        }),
        __metadata("design:paramtypes", [router_1.Router,
            router_1.ActivatedRoute,
            index_1.ReviewService,
            index_1.RestaurantService,
            index_1.AlertService])
    ], ReviewAddComponent);
    return ReviewAddComponent;
}());
exports.ReviewAddComponent = ReviewAddComponent;
//# sourceMappingURL=review_add.component.js.map