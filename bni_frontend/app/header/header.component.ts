import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';

import { User } from '../_models/index';
import { AuthenticationService } from '../_services/index';

@Component({
    moduleId: module.id,
    'selector': 'menu',
    styleUrls: ['header.component.scss'],
    templateUrl: 'header.component.html'
})

export class HeaderComponent implements OnInit {
    currentUser: User;
    users: User[] = [];
    timerId: any;
    isLogin: boolean = false;
    role: any = '';

    constructor(
        private authService: AuthenticationService,
        private router: Router) {
    }
    
    ngOnInit() {
        this.check();
        this.timerId = setInterval(() => {
          this.check(); 
        }, 500);
    }
    ngOnDestroy() {
        if (this.timerId) {
            clearInterval(this.timerId);
        }
    }

    private logout() {
        this.authService.logout();
        this.router.navigate(['login']);
    }
    private login() {
        this.authService.logout();
        this.router.navigate(['login']);
    }
    private register() {
        this.authService.logout();
        this.router.navigate(['register']);
    }
    private check() {
        if(localStorage.getItem('currentUser')) {
            this.isLogin = true;
            this.role = JSON.parse(localStorage.getItem('role'));
            if(this.role === 'admin')
                console.log(this.isLogin, this.role);
        } else
            this.isLogin = false;
    }
}