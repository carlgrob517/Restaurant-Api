import { Component, OnInit } from '@angular/core';
import { Params, ActivatedRoute } from '@angular/router';

import { Review } from '../_models/index';
import { ReviewService } from '../_services/index';

@Component({
    moduleId: module.id,
    styleUrls: ['review.component.scss'],
    templateUrl: 'review.component.html'
})

export class ReviewComponent implements OnInit {
    reviews: Review[] = [];

    constructor(private reviewService: ReviewService,
        private route: ActivatedRoute) {
    }

    ngOnInit() {
        this.route.queryParams.subscribe(params => {
            let id = params['id'];
            let name = params['name'];
            if(id === undefined)
                this.loadAllReviews();
            else    
                this.loadAllReviews(id, name);
        });
    }

    deleteReview(id: string) {
        console.log('clicked');
        this.reviewService.delete(id).subscribe(() => { this.loadAllReviews() });
    }

    private loadAllReviews(id = '', name='') {
        this.reviewService.getAll(id, name).subscribe(reviews => { this.reviews = reviews; console.log(reviews)});
    }
}