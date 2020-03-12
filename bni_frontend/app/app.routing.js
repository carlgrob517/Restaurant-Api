"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var router_1 = require("@angular/router");
var index_1 = require("./home/index");
var index_2 = require("./login/index");
var index_3 = require("./register/index");
var index_4 = require("./review/index");
var index_5 = require("./restaurant/index");
var index_6 = require("./dashboard/index");
var index_7 = require("./welcome/index");
var index_8 = require("./profile/index");
var index_9 = require("./_guards/index");
var appRoutes = [
    { path: '', component: index_7.WelcomeComponent },
    {
        path: 'home',
        component: index_1.HomeComponent,
        canActivate: [index_9.AuthGuard],
    },
    { path: 'dashboard', component: index_6.DashboardComponent },
    { path: 'login', component: index_2.LoginComponent },
    { path: 'register', component: index_3.RegisterComponent },
    { path: 'home/edit/:id', component: index_1.EditComponent },
    { path: 'restaurant', component: index_5.RestaurantComponent },
    { path: 'restaurant/edit/:id', component: index_5.EditResComponent },
    { path: 'restaurant/add', component: index_5.AddResComponent },
    { path: 'review', component: index_4.ReviewComponent, canActivate: [index_9.AuthGuard] },
    { path: 'profile', component: index_8.ProfileComponent, canActivate: [index_9.AuthGuard] },
    { path: 'review/add', component: index_4.ReviewAddComponent, canActivate: [index_9.AuthGuard] },
    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];
exports.routing = router_1.RouterModule.forRoot(appRoutes);
//# sourceMappingURL=app.routing.js.map