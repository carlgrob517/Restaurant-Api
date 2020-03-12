import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { User } from '../_models/index';
import { UserService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['edit.component.scss'],
    templateUrl: 'edit.component.html'
})

export class EditComponent implements OnInit {
    id: number;
    model: any = {};

    constructor(
        private userService: UserService,
        private route: ActivatedRoute,
        private router: Router) {
    }

    ngOnInit() {
        this.route.params.subscribe((params: Params) => {
            this.id = params.id;
            this.userService.getById(this.id)
                .subscribe(
                    data => {
                        this.model = data;
                        this.model.password = '';
                    },
                    err => {
    
                    });
          });
    }

    updateUser(id: number) {
        this.userService.update(this.model)
            .subscribe(
                data => {
                    this.router.navigate(['home']);
                },
                error => {
                });
    }
}