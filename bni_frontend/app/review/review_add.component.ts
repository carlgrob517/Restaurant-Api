import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { AlertService, ReviewService, RestaurantService } from '../_services/index';
import { ViewMore } from '../_models';
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

    reviewModel: any = {

    }

    viewMoreModel : ViewMore;
    info: any = {};
    loading = false;
    showSpinner = false;

    map: Object;
    marker: Object;
    zoom: number;
    status = [false, false, false, false, false];
    offset = 0;
    isGoogle = true;
    isViewMore = true;
    

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
                console.log(this.viewMoreModel);
                
                if (this.info.google_location_id == "" && this.info.tripadvisor_location_id == ""){
                    this.isViewMore = false;                    
                }else if(this.info.google_location_id == ""){
                    this.isGoogle = false;
                }

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

    viewMore(){

        if(this.isGoogle && this.model.google_location_id == ""){
            this.isViewMore = false;
            return;
        }
        if(!this.isGoogle && this.model.tripadvisor_location_id == ""){
            this.isViewMore = false;
            return;
        }

        if (this.isGoogle){
            this.viewMoreModel = {
                query:this.info.alias,
                offset:this.offset,
                id:this.info._id['$oid'],
                location_id:this.info.google_location_id?this.info.google_location_id:'',
                type:'google'
            }            
        }else{
            this.viewMoreModel = {
                query:this.info.alias,
                offset:this.offset,
                id:this.info._id['$oid'],
                location_id:this.info.tripadvisor_location_id?this.info.tripadvisor_location_id:'',
                type:'tripadvisor'
            }  
        }

        if(!this.isGoogle && this.info.tripadvisor_location_id == ''){
            this.isViewMore = false;
            return;
        }

        this.showSpinner = true;
        this.reviewService.viewMore(this.viewMoreModel)
            .subscribe(
                data => {

                    let reviews = this.info.id_review.reviews;
                    console.log(data);
                    for( let i = 0 ; i < data.length ; i++){
                        reviews.push(data[i]);
                    }


                    
                    if(data.length < 5 || this.info.tripadvisor_location_id == ""){
                        this.isViewMore = false;
                    }
                    reviews.sort((a, b) => (a.rating > b.rating) ? -1 : 1)

                    this.info.id_review.reviews = reviews;
                    this.offset = this.offset + 1;
                    
                    this.showSpinner = false;
                    //window.scroll(0,window.innerHeight);
                    this.isGoogle = false;


                },
                error => {
                    this.showSpinner = false;
                    console.log("aaah");
                });

       
        
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
