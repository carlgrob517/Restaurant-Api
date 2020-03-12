import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { User } from '../_models/index';
import { RestaurantService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['editRestaurant.component.scss'],
    templateUrl: 'editRestaurant.component.html'
})

export class EditResComponent implements OnInit {
    id: number;
    model: any = {};

    constructor(
        private service: RestaurantService,
        private route: ActivatedRoute,
        private router: Router) {
    }

    ngOnInit() {
        this.route.params.subscribe((params: Params) => {
            this.id = params.id;
            this.service.getById(this.id)
                .subscribe(
                    data => {
                        this.model = data;
                        this.model.password = '';
                    },
                    err => {
    
                    });
          });
    }

    update() {
        this.service.update(this.model)
            .subscribe(
                data => {
                    this.router.navigate(['home']);
                },
                error => {
                });
    }
}