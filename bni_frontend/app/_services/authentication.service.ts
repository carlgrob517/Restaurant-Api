import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map'
import {ConstantsService} from './common/constants.service';

@Injectable()
export class AuthenticationService {
    
    private url:string;
    constructor(private http: HttpClient, private _constants: ConstantsService) {
        this.url = this._constants.baseAppUrl;
     }

    login(username: string, password: string) {
        return this.http.post<any>(this.url + '/api/login', { email: username, password: password })
            .map(user => {
                // login successful if there's a jwt token in the response
                console.log(user);
                if (user && user.user_id) {
                    // store user details and jwt token in local storage to keep user logged in between page refreshes
                    localStorage.setItem('currentUser', JSON.stringify(user.user_id['$oid']));
                    localStorage.setItem('role', JSON.stringify(user.role));
                }
                return user;
            });
    }

    logout() {
        // remove user from local storage to log user out
        localStorage.removeItem('currentUser');
    }

    isLoggedIn() {
        if(localStorage.getItem('currentUser'))
            return true;
        return false;
    }
}
