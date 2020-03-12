import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {FormsModule} from '@angular/forms';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';

// used to create fake backend
import {fakeBackendProvider} from './_helpers/index';

import {AppComponent} from './app.component';
import {routing} from './app.routing';

import {AlertComponent} from './_directives/index';
import {AuthGuard} from './_guards/index';
import {JwtInterceptor} from './_helpers/index';

import {
    AlertService,
    AuthenticationService,
    UserService,
    ReviewService,
    RestaurantService,
    PagerService
} from './_services/index';
import {HomeComponent, EditComponent} from './home/index';
import {LoginComponent} from './login/index';
import {RegisterComponent} from './register/index';
import {HeaderComponent} from './header/index';
import {ReviewComponent, ReviewAddComponent} from './review/index';
import {DashboardComponent} from './dashboard/index';
import {WelcomeComponent} from './welcome/index';
import {RestaurantComponent, EditResComponent, AddResComponent} from './restaurant/index';
import {ProfileComponent} from './profile/index';
import {ConstantsService} from './_services/common/constants.service';
@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        HttpClientModule,
        routing,
    ],
    declarations: [
        AppComponent,
        AlertComponent,
        HomeComponent,
        LoginComponent,
        RegisterComponent,
        HeaderComponent,
        ReviewComponent,
        ReviewAddComponent,
        DashboardComponent,
        EditComponent,
        RestaurantComponent,
        EditResComponent,
        AddResComponent,
        WelcomeComponent,
        ProfileComponent,

    ],
    providers: [
        AuthGuard,
        AlertService,
        AuthenticationService,
        UserService,
        ReviewService,
        PagerService,
        RestaurantService,
        {
            provide: HTTP_INTERCEPTORS,
            useClass: JwtInterceptor,
            multi: true
        },
        ConstantsService,
    ],
    bootstrap: [AppComponent]
})

export class AppModule {
}
