import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { User } from '../_models/index';
import {ConstantsService} from './common/constants.service';
@Injectable()
export class UserService {
    private url:string;
    constructor(private http: HttpClient, private _constants:ConstantsService) {
        this.url = this._constants.baseAppUrl;
    }
    

    getAll() {
        return this.http.get<User[]>(this.url + '/api/users');
    }

    getById(id: number) {
        return this.http.get(this.url + '/api/users/' + id);
    }

    create(user: User) {
        return this.http.post(this.url + '/api/users/add', user);
    }

    update(user: User) {
        return this.http.put(this.url + '/api/users/update/' + user._id['$oid'], user);
    }

    delete(id: number) {
        return this.http.delete(this.url + '/api/users/delete/' + id);
    }
}