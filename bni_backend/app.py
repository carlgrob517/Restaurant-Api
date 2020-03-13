from flask import Flask, jsonify, request, json
from bson import ObjectId  # For ObjectId to work
from bson.json_util import dumps
from flask_pymongo import PyMongo
import os
import jwt
import json
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from functools import wraps
import sys
import requests
from urllib.parse import urljoin
from .classes.user_controller import user_controller
from .classes.google import google
from .classes.tripadvisor import tripadvisor
from .classes.review_controller import review_controller
import math


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

# baseUrl = 'https://ratings.food.gov.uk/{0}/json'
# baseUrl = 'https://api.yelp.com/v3/businesses/search?term=restaurants&location=Belfast&limit=50&offset=0'
baseUrl = 'https://api.yelp.com/v3/businesses/search?term=restaurants'
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'BNI'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/BNI'
app.config['JWT_SECRET_KEY'] = 'secret'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)
CORS(app)

user_controller = user_controller(app, mongo, bcrypt, request);    
review_controller = review_controller(app, mongo, bcrypt, request);    

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY']), 403
        except:
            return jsonify({'message': 'token is missing or invalid!'})

        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    
    #response = requests.get(baseUrl.format("business/" + str(23)), headers=headers)
    #response = requests.get(baseUrl.format("enhanced-search/en-GB/^/^/ALPHA/1/807/1/10"), headers=headers)
    # city_list = ['Enniskillen', 'Omagh', 'Strabane', 'Dungannon', 'Cookstown', 'Londonderry', 'Coleraine',
    #              'Armagh City', 'Newry', 'Portadown', 'Lurgan', 'Craigavon', 'Belfast', 'Ballymena', 'Larne', 'Antrim',
    #              'Ballycastle', 'Bangor', 'Newtownards', 'Lisburn']

    city_list = ['Ballymena', 'Larne', 'Antrim',
                 'Ballycastle', 'Bangor', 'Newtownards', 'Lisburn']
    
    restaurants = mongo.db.restaurant
    #restaurants.remove({})
    mongo.db.restaurant.delete_many({"location.city":'Portadown'})

    for x in city_list:
        offset_value = 0
        totalUrl = baseUrl + '&location=' + x + '&limit=50' + '&offset=' + str(offset_value)
        response = requests.get(totalUrl, auth=BearerAuth(
            'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
        data = response.json()
        x_total = data['businesses']
        x_number = data['total']
        print(x_number, ', ', x_total)
        print(x)

        if x_number > 50:
            while True:
                totalUrl = baseUrl + '&location=' + x + '&limit=50' + '&offset=' + str(offset_value)
                response = requests.get(totalUrl, auth=BearerAuth(
                    'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
                data = response.json()
                x_sub_total = data['businesses']
    
                offset_value += len(x_sub_total)
                # print('sub_total_count = ', offset_value)
                if offset_value > 950 or len(x_sub_total) < 1:
                    break
                else:
                    print('sub_total: ', x_sub_total)
                    for sub_restaurant in x_sub_total:
                        print('sub_restaurant : ', sub_restaurant['id'])
                        sub_url = 'https://api.yelp.com/v3/businesses/' + sub_restaurant['id']
                        response = requests.get(sub_url, auth=BearerAuth(
                            'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
                        data = response.json()
                        sub_restaurant.update({'id_info': data})
    
                        review_url = 'https://api.yelp.com/v3/businesses/' + sub_restaurant['id'] + '/reviews'
                        response = requests.get(review_url, auth=BearerAuth(
                            'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
                        review_data = response.json()
                        sub_restaurant.update({'id_review': review_data})
                        

                        gInstance = google("")
                        res = gInstance.getSearchLocationId(sub_restaurant["alias"])
                        sub_restaurant.update({'google_location_id':gInstance.getLocation(res)})

                        trip = tripadvisor("")
                        tres = trip.getSearchLocationId(sub_restaurant["coordinates"]["latitude"], sub_restaurant["coordinates"]["longitude"], 0)                
                        if trip.getPhone(tres).replace(" ", "") == sub_restaurant["phone"].replace(" ","")  :                    
                            sub_restaurant.update({'tripadvisor_location_id':trip.getLocation(tres)})                    
                            sub_restaurant.update({'review_count': str( len(review_data['reviews'])  + 5 +  int(trip.getRating(tres)) )  })
                            sub_restaurant.update({'rating': str(  round(( float(sub_restaurant['rating'])  +  gInstance.getRatingValue(res) + trip.getRatingValue(tres) ) / 3, 0) ) })
                            sub_restaurant.update({'rating_score': str(  round(( float(sub_restaurant['rating'])  +  gInstance.getRatingValue(res) + trip.getRatingValue(tres) ) / 3, 1) ) })
                        else:
                            sub_restaurant.update({'tripadvisor_location_id':''})                                    
                            sub_restaurant.update({'review_count': str( len(review_data['reviews'])  + 5  )  })
                            sub_restaurant.update({'rating': str(  round(( float(sub_restaurant['rating'])  +  gInstance.getRatingValue(res)  ) / 2, 0) ) })
                            sub_restaurant.update({'rating_score': str(  round(( float(sub_restaurant['rating'])  +  gInstance.getRatingValue(res)  ) / 2, 1) ) })


                        #str(sub_restaurant['rating'])
                        restaurants.insert(sub_restaurant)

        else:
            for restaurant in x_total:
                print('restaurant : ', restaurant['id'])
                url = 'https://api.yelp.com/v3/businesses/' + restaurant['id']
                response = requests.get(url, auth=BearerAuth(
                    'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
                data = response.json()
                restaurant.update({'id_info': data})
    
                review_url = 'https://api.yelp.com/v3/businesses/' + restaurant['id'] + '/reviews'
                response = requests.get(review_url, auth=BearerAuth(
                    'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
                review_data = response.json()
                restaurant.update({'id_review': review_data})
                #restaurant.update({'rating':  str(len(review_data['reviews']))  })    
    
                gInstance = google("")
                res = gInstance.getSearchLocationId(restaurant["alias"])
                restaurant.update({'google_location_id':gInstance.getLocation(res)})
                gReview = 5
                if gInstance.getLocation(res) == "":
                    gReview  = 0

                trip = tripadvisor("")
                tres = trip.getSearchLocationId(restaurant["coordinates"]["latitude"], restaurant["coordinates"]["longitude"], 0)                
                if trip.getPhone(tres).replace(" ", "") == restaurant["phone"].replace(" ","")  :                    
                    restaurant.update({'tripadvisor_location_id':trip.getLocation(tres)})                    
                    restaurant.update({'review_count': str( len(review_data['reviews'])  + gReview +  int(trip.getRating(tres)) )  })
                    restaurant.update({'rating': str(  round(( float(restaurant['rating'])  +  gInstance.getRatingValue(res) + trip.getRatingValue(tres) ) / 3, 0) ) })
                    restaurant.update({'rating_score': str(  round(( float(restaurant['rating'])  +  gInstance.getRatingValue(res) + trip.getRatingValue(tres) ) / 3, 1) ) })
                else:
                    restaurant.update({'tripadvisor_location_id':''})                                    
                    restaurant.update({'review_count': str( len(review_data['reviews'])  + gReview )  })
                    restaurant.update({'rating': str(  round(( float(restaurant['rating'])  +  gInstance.getRatingValue(res)  ) / 2, 0) ) })
                    restaurant.update({'rating_score': str(  round(( float(restaurant['rating'])  +  gInstance.getRatingValue(res)  ) / 2, 1) ) })
                
                
                restaurants.insert(restaurant)
    
    return jsonify({'msg': 'Updated successfully!'})

    # restaurants.remove({})
    # for restaurant in data:
    #     addr = []
    #     addrKeys = ["addressLine1", "addressLine2", "addressLine3"]
    #     for ak in addrKeys:
    #         if ak in restaurant and not restaurant[ak] is None:
    #             addr.append(str(restaurant[ak]).strip())
    #     scores = restaurant['Scores']
    #     restaurants.insert({
    #         'name': restaurant['BusinessName'],
    #         'postcode': restaurant['PostCode'],
    #         'location': ', '.join(addr),
    #         'rating_details': {'rating': restaurant['RatingValue'], 'hygiene': scores['Hygiene'],
    #                            'structural': scores['Structural'],
    #                            'confidenceInManagement': scores['ConfidenceInManagement']},
    #         'created': datetime.utcnow()
    #     })
    # return jsonify({'msg': 'Restaurants updated successfully!'})

# ============== Add Google Res =========================


# ==============Authentication===========================

@app.route('/api/login', methods=["POST"])
def login():
    return  user_controller.login()
    
@app.route('/logout', methods=["POST"])
@token_required
def logout():
    return user_controller.logout()


# ==============User manage========================
@app.route('/api/users/add', methods=["POST"])
def add_user():
    return user_controller.add_user();    

@app.route('/api/users')
# @token_required
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp

@app.route('/api/users/<id>')
# @token_required
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/api/users/delete/<id>', methods=['DELETE'])
# @token_required
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp


@app.route('/api/users/update', methods=['PUT'])
@token_required
def update_user():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    # validate the received values
    if _name and _email and _password and _id and request.method == 'PUT':
        # do not save password as a plain text
        _hashed_password = bcrypt.generate_password_hash(_password)
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
        resp = jsonify('User updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


# ==============Reviews================

@app.route('/api/reviews/add', methods=["POST"])
# @token_required
def add_review():
    reviews = mongo.db.review
    user_id = request.get_json()['user_id']
    restaurant_id = request.get_json()['restaurant_id']
    review = request.get_json()['review']
    user_rating = request.get_json()['user_rating']
    created = datetime.utcnow()

    review_id = reviews.insert({
        'author_name': user_id,
        'author_url': '',                
        'rating': user_rating,        
        'text': review,
        'time': str(created),        
        'restaurant_id':restaurant_id,        
        'type':'custom'
    })

    new_review = reviews.find_one({'_id': review_id})

    result = {'message': 'Saved successfully'}

    return jsonify({'result': result})
       

@app.route('/api/reviews')
# @token_required
def reviews():
    res_id = request.args['restaurant_id']
    print(res_id)
    if res_id:
        reviews = mongo.db.review.find({'restaurant_id': res_id, 'type':'custom'})
    else:
        reviews = mongo.db.review.find()
    resp = dumps(reviews)
    return resp


@app.route('/api/reviews/getByUserId')
# @token_required
def getByUserId():
    user_id = request.args['user_id']
    print(user_id)
    if user_id:
        reviews = mongo.db.review.find({'user_id': user_id,'type':'custom'})
    else:
        reviews = mongo.db.review.find()
    # for review in reviews:
    # review['user'] = mongo.db.user.find_one({'_id': ObjectId(review['user_id'])})
    # review['restaurant'] = mongo.db.restaurant.find_one({'_id': ObjectId(review['restaurant_id'])})
    #  print (review)
    print(reviews)
    resp = dumps(reviews)
    return resp

@app.route('/api/reviews/<id>')
@token_required
def review(id):
    review = mongo.db.review.find_one({'_id': ObjectId(id)})    
    resp = dumps(review)
    return resp


@app.route('/api/viewMore', methods=["POST"])
def viewMore():
    _id = request.get_json()['id']
    query = request.get_json()['query']
    offset = request.get_json()['offset']    
    location_id = request.get_json()['location_id']
    type = request.get_json()['type']    
    if type == "google":       
        print(location_id) 
        res =  review_controller.get_view_more_google(_id, query, location_id)
        print(res)
    else:
        res =  review_controller.get_view_more(_id, query, offset, location_id)
    resp = dumps(res)
    return resp

    




@app.route('/api/reviews/delete/<id>', methods=['DELETE'])
# @token_required
def delete_review(id):
    mongo.db.review.delete_one({'_id': ObjectId(id)})
    resp = jsonify('Review deleted successfully!')
    resp.status_code = 200
    return resp


@app.route('/api/reviews/update', methods=['PUT'])
@token_required
def update_review():
    _json = request.json
    _id = _json['_id']
    _user_id = _json['user_id']
    _restaurant_id = _json['restaurant_id']
    _review = _json['review']
    # validate the received values
    if _user_id and _restaurant_id and _review and _id and request.method == 'PUT':
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'user_id': _user_id, 'restaurant_id': _restaurant_id, 'review': _review}})
        resp = jsonify('Review updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


# ==============restaurants========================

@app.route('/api/restaurants/add', methods=["POST"])
# @token_required
def add_restaurant():
    restaurants = mongo.db.restaurant
    name = request.get_json()['name']
    location = request.get_json()['location']
    info = request.get_json()['comment']
    created = datetime.utcnow()

    res_id = restaurants.insert({
        'name': name,
        'location': location,
        'comment': info,
        'created': created
    })

    new_res = restaurants.find_one({'_id': res_id})

    result = {'message': 'Saved successfully'}

    return jsonify({'result': result})


@app.route('/api/restaurants')
# @token_required
def restaurants():
    search = request.args['search']
    name = request.args['name']
    location = request.args['location']
    rating = request.args['rating']
    alias = request.args['alias']
    city = request.args['city']
    # page = int(request.args['page']) - 1

    if search == '' and name == '' and location == '' and rating == '' and alias == '' and city == '':
        count = mongo.db.restaurant.count()
        restaurants = mongo.db.restaurant.find()
        print('all')
    elif search == '' and name == '' and location == '' and rating == '' and alias != '' and city == '':
        query = dict()
        query['categories.0.alias'] = {'$regex': alias, '$options': 'i'}
        count = mongo.db.restaurant.count(query)
        restaurants = mongo.db.restaurant.find(query)

    elif search == '' and name == '' and location == '' and rating == '' and alias == '' and city != '':
        query = dict()
        query['id_info.location.city'] = {'$regex': city, '$options': 'i'}
        query['rating'] = {'$regex': '5.0', '$options': 'i'}
        count = mongo.db.restaurant.count(query)
        restaurants = mongo.db.restaurant.find(query).sort([('review_count', -1)])

    elif search == '':
        query = dict()
        if name != '':
            query['name'] = {'$regex': name, '$options': 'i'}
        if location != '':
            query['location.city'] = {'$regex': location, '$options': 'i'}
        if rating != '':
            query['rating'] = {'$regex': rating, '$options': 'i'}
        if alias != '':
            query['categories.0.alias'] = {'$regex': alias, '$options': 'i'}
        if city != '':
            query['id_info.location.city'] = {'$regex': city, '$options': 'i'}
        count = mongo.db.restaurant.count(query)
        restaurants = mongo.db.restaurant.find(query)
        print('detail search')
    else:
        count = mongo.db.restaurant.count({"name": {'$regex': search, '$options': 'i'}})
        restaurants = mongo.db.restaurant.find({"name": {'$regex': search, '$options': 'i'}})
        print('key search')
    print(count)
    resp = dumps(restaurants)
    return resp


@app.route('/api/restaurants/<id>')
# @token_required
def restaurant(id):
    restaurant = mongo.db.restaurant.find_one({'_id': ObjectId(id)})
    if 'google_location_id' in restaurant:
        print('exist google location id')
    else:
        print('start')
        res = review_controller.google_call(id , restaurant["alias"])
        print(res)
        if res == "Fail" or res == "Retry":
            if res == "Fail":       
                mongo.db.restaurant.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},
                                    {'$set': { 'google_location_id' : "0" }})
            rt = review_controller.tripadvisor_call(id, restaurant["alias"])
            if rt == "Fail":
                mongo.db.restaurant.update_one({'_id': ObjectId(id['$oid']) if '$oid' in id else ObjectId(id)},
                                    {'$set': { 'tripadvisor_location_id' : "0" }})
        else:
            print("google ok")

    restaurant = mongo.db.restaurant.find_one({'_id': ObjectId(id)})
    resp = dumps(restaurant)
    return resp


@app.route('/api/restaurants/delete/<id>', methods=['DELETE'])
# @token_required
def delete_restaurant(id):
    mongo.db.restaurant.delete_one({'_id': ObjectId(id)})
    resp = jsonify('Restaurant deleted successfully!')
    resp.status_code = 200
    return resp


@app.route('/api/restaurants/update/', methods=['PUT'])
# @token_required
def update_restaurant():
    _json = request.json
    _id = _json['_id']
    _name = _json['name']
    _location = _json['location']
    _info = _json['comment']
    # validate the received values
    if _name and _location and _info and _id and request.method == 'PUT':
        # save edits
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                 {'$set': {'_id': _id, 'name': _name, 'location': _location, 'info': _info}})
        resp = jsonify('Review updated successfully!')
        resp.status_code = 200
        return resp
    else:
        return not_found()


# ================================================

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    app.run(debug=True)
