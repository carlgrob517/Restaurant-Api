"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
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
        this.info = {};
        this.loading = false;
    }
    ReviewAddComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.model.user_id = JSON.parse(localStorage.getItem('currentUser'));
        console.log(this.model.user_id);
        this.route.queryParams.subscribe(function (params) {
            var id = params['id'];
            _this.restaurantService.getById(id).subscribe(function (data) {
                _this.info = data;
                _this.model['restaurant_id'] = _this.info._id['$oid'];
            });
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
    return ReviewAddComponent;
}());
exports.ReviewAddComponent = ReviewAddComponent;
//# sourceMappingURL=review_add.component.js.map