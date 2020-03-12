import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { User, Restaurant } from '../_models/index';
import { RestaurantService, PagerService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['restaurant.component.scss'],
    templateUrl: 'restaurant.component.html'
})

export class RestaurantComponent implements OnInit {
    currentUser: User;
    restaurants: Restaurant[] = [];
    // pager object
    pager: any = {};
    // paged items
    pagedItems: any[];

    constructor(
            private service: RestaurantService,
            private router: Router,
            private pagerService: PagerService,
        ) {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }

    ngOnInit() {
        this.loadAllRestaurants();
    }

    delete(id: number) {
        this.service.delete(id).subscribe(() => { this.loadAllRestaurants() });
    }

    edit(id: number) {
        this.router.navigate(['restaurant/edit', id]);
    }

    add() {
        this.router.navigate(['restaurant/add']);
    }

    private loadAllRestaurants() {
        this.service.getAll({page: 1, search: '', name: '', location: '', rating: ''})  
            .subscribe(data => { 
                this.restaurants = data; 
                console.log(data);
                this.setPage(1);
            });
    }

    setPage(page: number) {
        // get pager object from service
        this.pager = this.pagerService.getPager(this.restaurants.length, page);

        // get current page of items
        this.pagedItems = this.restaurants.slice(this.pager.startIndex, this.pager.endIndex + 1);
    }
}