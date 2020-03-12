import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Restaurant } from '../_models/index';
import { RestaurantService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['addRestaurant.component.scss'],
    templateUrl: 'addRestaurant.component.html'
})

export class AddResComponent implements OnInit {
    id: number;
    model: any = {};

    constructor(
        private service: RestaurantService,
        private router: Router) {
    }

    ngOnInit() {
        
    }

    save() {
        this.service.create(this.model)
            .subscribe(
                data => {
                    this.router.navigate(['restaurant']);
                },
                error => {
                });
    }
}