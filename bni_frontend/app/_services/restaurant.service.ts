import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Restaurant } from '../_models/index';
import {ConstantsService} from './common/constants.service';

@Injectable()
export class RestaurantService {
    
    private url:string;
    constructor(private http: HttpClient, private _constants:ConstantsService) {
        this.url = this._constants.baseAppUrl;
    }

    getAll(query: any) {
        return this.http.get<Restaurant[]>(this.url + `/api/restaurants?page=${query.page}&search=${query.search}&name=${query.name}&location=${query.location}&rating=${query.rating}&alias=${query.alias}&city=${query.city}`);
    }

    getById(id: number) {
        return this.http.get(this.url + '/api/restaurants/' + id);
    }

    create(data: Restaurant) {
        return this.http.post(this.url + '/api/restaurants/add', data);
    }

    update(data: Restaurant) {
        return this.http.put(this.url + '/api/restaurants/update', data);
    }

    delete(id: number) {
        return this.http.delete(this.url + '/api/restaurants/delete/' + id);
    }

}
