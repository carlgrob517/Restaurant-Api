import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { AlertService, ReviewService, RestaurantService } from '../_services/index';
declare var google: any;

@Component({
    moduleId: module.id,
    styleUrls: ['review_add.component.scss'],
    templateUrl: 'review_add.component.html'
})

export class ReviewAddComponent implements OnInit {
    model: any = {
        'user_id': 'user',
        'restaurant_id': 'res',
        'vote': '',
    };
    info: any = {};
    loading = false;

    map: Object;
    marker: Object;
    zoom: number;
    status = [false, false, false, false, false];

    @ViewChild('map') mapRef: ElementRef;

    constructor(
        private router: Router,
        private route: ActivatedRoute,
        private reviewService: ReviewService,
        private restaurantService : RestaurantService,
        private alertService: AlertService) { }

    ngOnInit() {
        this.model.user_id = JSON.parse(localStorage.getItem('currentUser'));
        // console.log(this.model.user_id);

        this.route.queryParams.subscribe(params => {
            let id = params['id'];
            this.restaurantService.getById(id).subscribe(data => {

                this.info = data;
                this.model['restaurant_id'] = this.info._id['$oid'];

                setTimeout(() => {
                    this.map = new google.maps.Map(this.mapRef.nativeElement, {
                        zoom: 10,
                        center: { lat: this.info.coordinates.latitude, lng: this.info.coordinates.longitude }
                    });
                    this.marker = new google.maps.Marker({
                        position: { lat: this.info.coordinates.latitude, lng: this.info.coordinates.longitude },
                        map: this.map
                    });

                }, 2000)

            });
        });
    }

    set_rating(e:any) {
        // @ts-ignore
        let result = parseInt(e.target.value);
        for(let i = 0 ; i < this.status.length; i ++ ){
            this.status[i] = false;
        }

        // @ts-ignore
        this.status[result - 1] = true;
    }
    addReview() {
        this.loading = true;
        this.reviewService.create(this.model)
            .subscribe(
                data => {
                    this.router.navigate(['review']);
                },
                error => {
                    this.loading = false;
                });
    }

}
