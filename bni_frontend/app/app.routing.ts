import { Routes, RouterModule } from '@angular/router';

import { HomeComponent, EditComponent } from './home/index';
import { LoginComponent } from './login/index';
import { RegisterComponent } from './register/index';
import { ReviewComponent, ReviewAddComponent } from './review/index';
import { RestaurantComponent, EditResComponent, AddResComponent } from './restaurant/index';
import { DashboardComponent } from './dashboard/index';
import { WelcomeComponent } from './welcome/index';
import { ProfileComponent } from './profile/index';
import { AuthGuard } from './_guards/index';

const appRoutes: Routes = [
    { path: '', component: WelcomeComponent },
    { 
        path: 'home', 
        component: HomeComponent, 
        canActivate: [AuthGuard],
    }, 
    { path: 'dashboard', component: DashboardComponent },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: 'home/edit/:id', component: EditComponent },
    { path: 'restaurant', component: RestaurantComponent},
    { path: 'restaurant/edit/:id', component: EditResComponent},
    { path: 'restaurant/add', component: AddResComponent},
    { path: 'review', component: ReviewComponent, canActivate: [AuthGuard] },
    { path: 'profile', component: ProfileComponent, canActivate: [AuthGuard] },
    { path: 'review/add', component: ReviewAddComponent, canActivate: [AuthGuard] },

    // otherwise redirect to home
    { path: '**', redirectTo: '' }
];

export const routing = RouterModule.forRoot(appRoutes);