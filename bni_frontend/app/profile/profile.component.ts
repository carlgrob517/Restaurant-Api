import { Component, OnInit } from '@angular/core';
import { Params, ActivatedRoute } from '@angular/router';

import { Review } from '../_models/index';
import { ReviewService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['profile.component.scss'],
    templateUrl: 'profile.component.html'
})

export class ProfileComponent implements OnInit {
    reviews: Review[] = [];

    constructor(private reviewService: ReviewService,
        private route: ActivatedRoute) {
    }

    ngOnInit() {
        let id = JSON.parse(localStorage.getItem('currentUser'));
        console.log(id);
        this.loadAllReviews(id);
    }

    deleteReview(id: string) {
        console.log('clicked');
        this.reviewService.delete(id).subscribe(() => { this.loadAllReviews() });
    }

    private loadAllReviews(id = '') {
        this.reviewService.getByUserId(id).subscribe(reviews => { this.reviews = reviews; console.log(reviews)});
    }
}