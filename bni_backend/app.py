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
    # response = requests.get(baseUrl.format("business/" + str(23)), headers=headers)
    # response = requests.get(baseUrl.format("enhanced-search/en-GB/^/^/ALPHA/1/807/1/10"), headers=headers)
    # city_list = ['Enniskillen', 'Omagh', 'Strabane', 'Dungannon', 'Cookstown', 'Londonderry', 'Coleraine',
    #              'Armagh City', 'Newry', 'Portadown', 'Lurgan', 'Craigavon', 'Belfast', 'Ballymena', 'Larne', 'Antrim',
    #              'Ballycastle', 'Bangor', 'Newtownards', 'Lisburn']
    #
    # restaurants = mongo.db.restaurant
    # restaurants.remove({})
    # for x in city_list:
    #     offset_value = 0
    #     totalUrl = baseUrl + '&location=' + x + '&limit=50' + '&offset=' + str(offset_value)
    #     response = requests.get(totalUrl, auth=BearerAuth(
    #         'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
    #     data = response.json()
    #     x_total = data['businesses']
    #     x_number = data['total']
    #     print(x_number, ', ', x_total)
    #     if x_number > 50:
    #         while True:
    #             totalUrl = baseUrl + '&location=' + x + '&limit=50' + '&offset=' + str(offset_value)
    #             response = requests.get(totalUrl, auth=BearerAuth(
    #                 'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
    #             data = response.json()
    #             x_sub_total = data['businesses']
    #
    #             offset_value += len(x_sub_total)
    #             # print('sub_total_count = ', offset_value)
    #             if offset_value > 950 or len(x_sub_total) < 1:
    #                 break
    #             else:
    #                 print('sub_total: ', x_sub_total)
    #                 for sub_restaurant in x_sub_total:
    #                     print('sub_restaurant : ', sub_restaurant['id'])
    #                     sub_url = 'https://api.yelp.com/v3/businesses/' + sub_restaurant['id']
    #                     response = requests.get(sub_url, auth=BearerAuth(
    #                         'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
    #                     data = response.json()
    #                     sub_restaurant.update({'id_info': data})
    #
    #                     review_url = 'https://api.yelp.com/v3/businesses/' + sub_restaurant['id'] + '/reviews'
    #                     response = requests.get(review_url, auth=BearerAuth(
    #                         'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
    #                     review_data = response.json()
    #                     sub_restaurant.update({'id_review': review_data})
    #                     sub_restaurant.update({'rating': str(sub_restaurant['rating'])})
    #
    #                     restaurants.insert(sub_restaurant)
    #
    #     else:
    #         for restaurant in x_total:
    #             print('restaurant : ', restaurant['id'])
    #             url = 'https://api.yelp.com/v3/businesses/' + restaurant['id']
    #             response = requests.get(url, auth=BearerAuth(
    #                 'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
    #             data = response.json()
    #             restaurant.update({'id_info': data})
    #
    #             review_url = 'https://api.yelp.com/v3/businesses/' + restaurant['id'] + '/reviews'
    #             response = requests.get(review_url, auth=BearerAuth(
    #                 'HuZbDEx4aEBAK1Hd7KkaR6b3CcwxYDX--hbITb58_7hhXeVTTvPF1ouSRZei27k1hhacmicLFLmdjMyV3DgHR6_YzpbR6FUtl3YeyhnN15osPcwj9F5nKUqm87BaXnYx'))
    #             review_data = response.json()
    #             restaurant.update({'id_review': review_data})
    #             restaurant.update({'rating': str(restaurant['rating'])})
    #
    #             restaurants.insert(restaurant)
    #
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
@app.route('/api/google_sync', methods=["POST"])
def google_sync():
    _json = request.json
    _id = _json['_id']
    old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )    
    if(old.google != '1'):        
        gInstance = google("key")    
        query = request.get_json()['query']
        res = json.loads(gInstance.getSearchLocationId(query)) 
        status = res["status"]
        if(status == "OK"):
            if( len(res["results"]) > 0  and  "United Kingdom" in res["results"][0]["formatted_address"] ):
                placeId = res["results"][0]["place_id"]
                rating =  res["results"][0]["rating"]
                res = json.loads(gInstance.getDetails(placeId)) 
                if( res["status"] == "OK"):
                    reviews = res["results"]["reviews"]
                    
                    mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                            {'$set': {'rating': (old.rating + rating)/2 ,'reviews': old.review + reviews, 'google' : '1'}})
                else:
                    return "Fail"    
        else:
            return "Fail"
    return  "Ok"

def google_call(_id, query):   
    
    old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )        
    gInstance = google("key")
    try:
        res = gInstance.getSearchLocationId(query)         
        status = res["status"]        
        if(status == "OK"):
            if( len(res["results"]) > 0  and  "United Kingdom" in res["results"][0]["formatted_address"] ):
                placeId = res["results"][0]["place_id"]
                rating =  res["results"][0]["rating"]
                res = gInstance.getDetails(placeId)            
                if( res["status"] == "OK"):                
                    reviews = res["result"]["reviews"]
                    for item in reviews :
                        add_review_item(item, placeId, _id)
                    # reviews = res["result"]["reviews"]
                    mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                            {'$set': {'rating':math.ceil( (float(old["rating"]) + float(rating))/2 ) , 'google' : '1', 'review_count':len(reviews)}})
                else:
                    return "Fail"    
        else:
            return "Fail"
    except ValueError:   
            #index = index + 1                     
            print("Oops!  That was no valid number.  Try again...")

        
    
    return  "Ok"

# ============== Add Tripadvisor Res ===================
@app.route('/api/tripadvisor_sync', methods=["POST"])
def tripadvisor_sync():
    _json = request.json
    _id = _json['_id']

    tripInstance = tripadvisor("api_key")    
    query = request.get_json()['query']
    res = json.loads(tripInstance.getSearchLocationId(query)) 
    status = res["status"]
    if(status == "OK"):
        placeId = res["results"][0]["place_id"]
        rating =  res["results"][0]["rating"]
        res = json.loads(tripInstance.getDetails(placeId)) 
        if( res["status"] == "OK"):
            reviews = res["results"]["reviews"]
            for item in reviews :
                add_tripadvisor_review_item(item, placeId, _id)

            # old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )                
            # mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
            #                         {'$set': {'rating': (old.rating + rating)/2 ,'reviews': old.review + reviews}})
        else:
            return "Fail"
    else:
        return "Fail"
    return "Ok"

def tripadvisor_call(_id, query):    
    tripInstance = tripadvisor("")        
    res = tripInstance.getSearchLocationId(query, 0)
    datas = res["data"]
    if(len(datas) > 0 ):
        for data in datas:            
            result_type = data["result_type"]                        
            address_obj = data["result_object"]["address_obj"]
            print(address_obj)
            country =  address_obj["country"]

            if result_type == "restaurants" and country == "United Kingdom":
                location_id = data["result_object"]["location_id"]
                rating = data["result_object"]["rating"]
                num_reviews = data["result_object"]["num_reviews"]
                print("------------")              
                print(location_id)
                index = 0

                old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )
                mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                    {'$set': {'rating': str(math.ceil(round((float(old["rating"]) + float(rating))/2,1))) , 'tripadvisor' : '1' }})

                for offset in  range(int(int(num_reviews)/20) + 1 + index):
                    try:
                        res = tripInstance.getDetails(location_id, offset - index)
                        print(str(offset - index ))
                        if len(res["data"]) > 0 :
                            reviews  = res["data"]
                            for item in reviews :
                                add_tripadvisor_review_item(item, location_id, _id)
                            
                    except ValueError:   
                        #index = index + 1                     
                        print("Oops!  That was no valid number.  Try again...")
                   
                
                old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )
                reviews = mongo.db.review.find({'restaurant_id': _id})
                mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                    {'$set': { 'review_count' : reviews.count() }})

        else:
            return "Fail"
    else:
        return "Fail"
    return "Ok"

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


def add_review_item(item, placeId, _id):
    reviews = mongo.db.review
    author_name = item['author_name']
    author_url = item['author_url']
    language = item['language']
    profile_photo_url = item['profile_photo_url']
    rating = item['rating']
    relative_time_description = item['relative_time_description']
    text = item['text']
    time = item['time']

    review_id = reviews.insert({
        'author_name': author_name,
        'author_url': author_url,
        'language': language,
        'profile_photo_url': profile_photo_url,
        'rating': rating,
        'relative_time_description': relative_time_description,
        'text': text,
        'time': time,
        'placeId':placeId,
        'restaurant_id':_id,
        'type':'service'
    })


def add_tripadvisor_review_item(item, placeId, _id):
    reviews = mongo.db.review
    author_name = item["user"]['username']
    author_url = item['url']
    language = item['lang']
    profile_photo_url = item['user']['contributions']['avatar_thumbnail_url']
    rating = item['rating']
    relative_time_description = item['travel_date']
    text = item['text']

    time = item['published_date']
    title = item['title']

    review_id = reviews.insert({
        'author_name': author_name,
        'author_url': author_url,
        'language': language,
        'profile_photo_url': profile_photo_url,
        'rating': rating,
        'relative_time_description': relative_time_description,
        'text': text,
        'title':title,
        'time': time,
        'placeId':placeId,
        'restaurant_id':_id,
    })


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

def get_reviews():
    res_id = request.args['restaurant_id']    
    restaurant = mongo.db.restaurant.find_one({'_id':ObjectId(res_id)})

    if( 'google' in restaurant  and  restaurant["google"] == '1' ):    
        print(restaurant["name"])
    else:
        google_call(res_id, restaurant["name"])
    
    if( 'tripadvisor' in restaurant  and  restaurant["tripadvisor"] == '1' ):    
        print(restaurant["name"])
    else:
        tripadvisor_call(res_id , restaurant["name"] )
        
    if res_id:
        reviews = mongo.db.review.find({'restaurant_id': res_id})
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
