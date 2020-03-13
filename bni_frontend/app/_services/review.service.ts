import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Review, ViewMore } from '../_models/index';

import {ConstantsService} from './common/constants.service';

@Injectable()
export class ReviewService {
    private url:string;
    constructor(private http: HttpClient, private _constants:ConstantsService) {
        this.url = this._constants.baseAppUrl;
    }
    
    getAll(id: string, name:string) {
        return this.http.get<Review[]>(this.url + '/api/reviews?restaurant_id=' + id);
    }

    getByUserId(id: string) {
        return this.http.get<Review[]>(this.url + '/api/reviews/getByUserId?user_id=' + id)
    }

    getById(id: number) {
        return this.http.get(this.url + '/api/reviews/' + id);
    }

    create(review: Review) {
        return this.http.post(this.url + '/api/reviews/add', review);
    }

    update(review: Review) {
        return this.http.put(this.url + '/api/reviews/update' + review._id, review);
    }

    delete(id: string) {
        return this.http.delete(this.url + '/api/reviews/delete/' + id);
    }

    viewMore(viewMore:ViewMore){        
        return this.http.post(this.url + '/api/viewMore', viewMore);
    }

    viewMoreGoogle(viewMore:ViewMore){
        return this.http.post(this.url + '/api/viewMoreGoogle', viewMore);
    }

}