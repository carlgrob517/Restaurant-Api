import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { User, Restaurant } from '../_models/index';
import { RestaurantService, PagerService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['dashboard.component.scss'],
    templateUrl: 'dashboard.component.html'
})

export class DashboardComponent implements OnInit {
    currentUser: User;
    restaurants: Restaurant[] = [];
    model: any = {
        searchStr: '',
        name: '',
        location: '',
        rating: '',
        alias: '',
        city: ''
    };
    page: Number = 1;
    pageSize: Number = 10;
    total: Number = 0;
    showDetailsSearch: Boolean = false;
    loading: Boolean = false;

    // pager object
    pager: any = {};

    // paged items
    pagedItems: any[];

    constructor(
        private service: RestaurantService,
        private pagerService: PagerService,
        private router: Router) {
        this.currentUser = JSON.parse(localStorage.getItem('currentUser'));
    }

    ngOnInit() {
        this.search();
    }


    //AIzaSyBRHZ24e9OnPUSM4J2pLfOzVGrXBkFia_g
    search() {
        this.loading = true;
        console.log("all search");
        console.log(this.page);
        this.service.getAll({page: this.page, search: this.model.searchStr, name: '', location: '', rating: '', alias: '', city: ''})
            .subscribe(
                data => {
                    console.log(data);
                    this.total = data.length;
                    this.restaurants = data;
                    this.loading = false;
                    this.setPage(1);
                    
                },
                error => {
                });
    }

    each_search(info: any) {
        this.router.navigate(['review/add'], { queryParams: { 'id': info._id['$oid']}});

    }

    top_search() {
        this.loading = true;
        console.log("top");
        console.log(this.page);
        this.service.getAll({page: this.page, name: '', search:'', location: '', rating: '', alias: '', city: this.model.city})
            .subscribe(
                data => {
                    this.total = data.length;
                    this.restaurants = data;
                    this.loading = false;
                    console.log(this.restaurants);
                    this.setPage(1);
                },
                error => {
                });
    }

    searchByDetails() {
        this.loading = true;
        console.log("by dtails");
        console.log(this.page);
        this.service.getAll({page: this.page, search:'', name: this.model.name, location: this.model.location, rating: this.model.rating, alias: this.model.alias, city: this.model.city})
            .subscribe(
                data => {
                    this.total = data.length;
                    this.restaurants = data;
                    this.loading = false;
                    console.log(this.restaurants);
                    this.setPage(1);
                },
                error => {
                });
    }

    write(info: any) {        
        this.router.navigate(['review/add'], { queryParams: { 'id': info._id['$oid']}});
    }

    viewAll(id: number, name: any) {
        this.router.navigate(['/review'], { queryParams: { 'id' : id, 'name':name}});
    }

    toggleDetailSearch() {
        this.showDetailsSearch = ! this.showDetailsSearch;
    }

    setPage(page: number) {
        // get pager object from service
        this.pager = this.pagerService.getPager(this.restaurants.length, page);
        // get current page of items
        this.pagedItems = this.restaurants.slice(this.pager.startIndex, this.pager.endIndex + 1);
        
    }

    getRepeatArray(count: number) {
        let arr = [];
        for(let i = 0; i < count ; i++)
            arr.push(i);
        return arr;
    }
}
