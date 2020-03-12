# from flask import Flask, jsonify, request, json
# from bson import ObjectId  # For ObjectId to work
# from bson.json_util import dumps
# from flask_pymongo import PyMongo
# import os
# from datetime import datetime
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS
# from flask_jwt_extended import JWTManager
# from flask_jwt_extended import create_access_token

# app = Flask(__name__)

# app.config['MONGO_DBNAME'] = 'BNI'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/BNI'
# app.config['JWT_SECRET_KEY'] = 'secret'

# mongo = PyMongo(app)
# bcrypt = Bcrypt(app)
# jwt = JWTManager(app)

# CORS(app)


# @app.route('/')
# def index():
#     return jsonify({'message': 'success'})


# # ==============Authentication================

# @app.route('/login', methods=["POST"])
# def login():
#     users = mongo.db.user
#     email = request.get_json()['email']
#     password = request.get_json()['password']
#     result = ''

#     response = users.find_one({'email': email})
#     if response:
#         if bcrypt.check_password_hash(response['password'], password):
#             access_token = create_access_token(identify={
#                 'first_name': response['first_name'],
#                 'last_name': response['last_name'],
#                 'email': response['email']
#             })
#             result = jsonify({'token': access_token})
#         else:
#             result = jsonify({'error': 'Invalid username or password.'})
#     else:
#         result = jsonify({"result": 'Not registered'})

#     return jsonify({'result': result})


# @app.route('/logout', methods=["POST"])
# def logout():
#     users = mongo.db.user
#     email = request.get_json()['email']
#     password = request.get_json()['password']
#     result = ''

#     response = users.find_one({'email': email})

#     if response:
#         if bcrypt.check_password_hash(response['password'], password):
#             access_token = create_access_token(identify={
#                 'first_name': response['first_name'],
#                 'last_name': response['last_name'],
#                 'email': response['email']
#             })
#             result = jsonify({'token': access_token})
#         else:
#             result = jsonify({'error': 'Invalid username or password.'})
#     else:
#         result = jsonify({"result": 'Not registered'})

#     return jsonify({'result': result})


# # ==============User manage================

# @app.route('/users/add', methods=["POST"])
# def add_user():
#     users = mongo.db.user
#     first_name = request.get_json()['first_name']
#     last_name = request.get_json()['last_name']
#     email = request.get_json()['email']
#     password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
#     created = datetime.utcnow()

#     user_id = users.insert({
#         'first_name': first_name,
#         'last_name': last_name,
#         'email': email,
#         'password': password,
#         'created': created
#     })

#     new_user = users.find_one({'_id': user_id})

#     result = {'email': new_user['email'] + 'registered'}

#     return jsonify({'result': result})


# @app.route('/users')
# def users():
#     users = mongo.db.user.find()
#     resp = dumps(users)
#     return resp


# @app.route('/users/<id>')
# def user(id):
#     user = mongo.db.user.find_one({'_id': ObjectId(id)})
#     resp = dumps(user)
#     return resp


# @app.route('/users/delete/<id>', methods=['DELETE'])
# def delete_user(id):
#     mongo.db.user.delete_one({'_id': ObjectId(id)})
#     resp = jsonify('User deleted successfully!')
#     resp.status_code = 200
#     return resp


# @app.route('/users/update', methods=['PUT'])
# def update_user():
#     _json = request.json
#     _id = _json['_id']
#     _name = _json['name']
#     _email = _json['email']
#     _password = _json['pwd']
#     # validate the received values
#     if _name and _email and _password and _id and request.method == 'PUT':
#         # do not save password as a plain text
#         _hashed_password = bcrypt.generate_password_hash(_password)
#         # save edits
#         mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
#                                  {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})
#         resp = jsonify('User updated successfully!')
#         resp.status_code = 200
#         return resp
#     else:
#         return not_found()


# # ==============Reviews================

# @app.route('/reviews/add', methods=["POST"])
# def add_review():
#     reviews = mongo.db.review
#     user_id = request.get_json()['user_id']
#     restaurant_id = request.get_json()['restaurant_id']
#     review = request.get_json()['review']
#     created = datetime.utcnow()

#     review_id = reviews.insert({
#         'user_id': user_id,
#         'restaurant_id': restaurant_id,
#         'review': review,
#         'created': created
#     })

#     new_review = reviews.find_one({'_id': review_id})

#     result = {'message': 'Saved successfully'}

#     return jsonify({'result': result})


# @app.route('/reviews')
# def reviews():
#     reviews = mongo.db.review.find()
#     resp = dumps(reviews)
#     return resp


# @app.route('/reviews/<id>')
# def review(id):
#     review = mongo.db.review.find_one({'_id': ObjectId(id)})
#     resp = dumps(review)
#     return resp


# @app.route('/reviews/delete/<id>', methods=['DELETE'])
# def delete_review(id):
#     mongo.db.review.delete_one({'_id': ObjectId(id)})
#     resp = jsonify('Review deleted successfully!')
#     resp.status_code = 200
#     return resp


# @app.route('/reviews/update', methods=['PUT'])
# def update_review():
#     _json = request.json
#     _id = _json['_id']
#     _user_id = _json['user_id']
#     _restaurant_id = _json['restaurant_id']
#     _review = _json['review']
#     # validate the received values
#     if _user_id and _restaurant_id and _review and _id and request.method == 'PUT':
#         # save edits
#         mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
#                                  {'$set': {'user_id': _user_id, 'restaurant_id': _restaurant_id, 'review': _review}})
#         resp = jsonify('Review updated successfully!')
#         resp.status_code = 200
#         return resp
#     else:
#         return not_found()


# # ==============Restaurants================

# @app.route('/restuarants/add', methods=["POST"])
# def add_restaurant():
#     restaurants = mongo.db.restaurant
#     name = request.get_json()['name']
#     location = request.get_json()['location']
#     info = request.get_json()['info']
#     created = datetime.utcnow()

#     res_id = restaurants.insert({
#         'name': name,
#         'location': location,
#         'info': info,
#         'created': created
#     })

#     new_res = reviews.find_one({'_id': res_id})

#     result = {'message': 'Saved successfully'}

#     return jsonify({'result': result})


# @app.route('/restaurants')
# def restaurants():
#     restaurants = mongo.db.restaurant.find()
#     resp = dumps(restaurants)
#     return resp


# @app.route('/restaurants/<id>')
# def restaurant(id):
#     restaurant = mongo.db.restaurant.find_one({'_id': ObjectId(id)})
#     resp = dumps(restaurant)
#     return resp


# @app.route('/restaurants/delete/<id>', methods=['DELETE'])
# def delete_restaurant(id):
#     mongo.db.restaurant.delete_one({'_id': ObjectId(id)})
#     resp = jsonify('Restaurant deleted successfully!')
#     resp.status_code = 200
#     return resp


# @app.route('/restaurants/update', methods=['PUT'])
# def update_restaurant():
#     _json = request.json
#     _id = _json['_id']
#     _name = _json['name']
#     _location = _json['location']
#     _info = _json['info']
#     # validate the received values
#     if _name and _location and _info and _id and request.method == 'PUT':
#         # save edits
#         mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
#                                  {'$set': {'_id': _id, 'name': _name, 'location': _location, 'info': _info}})
#         resp = jsonify('Review updated successfully!')
#         resp.status_code = 200
#         return resp
#     else:
#         return not_found()


# # =================================================

# @app.errorhandler(404)
# def not_found(error=None):
#     message = {
#         'status': 404,
#         'message': 'Not Found: ' + request.url,
#     }
#     resp = jsonify(message)
#     resp.status_code = 404

#     return resp
