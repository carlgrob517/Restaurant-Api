import {Injectable} from '@angular/core';

@Injectable()
export class ConstantsService{
    readonly baseAppUrl: string = 'http://127.0.0.1:5000';
    readonly location: string = 'api/';
}
