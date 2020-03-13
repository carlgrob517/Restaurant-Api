import requests
import json
from flask import Flask, jsonify, json
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.json_util import dumps
from datetime import datetime, timedelta
import jwt

class user_controller:

    def __init__(self,  app, mongo , bcrypt, req):
        self.mongo = mongo
        self.app = app
        self.bcrypt = bcrypt
        self.req = req
          
    def login(self):

        print("entered");
        users = self.mongo.db.user        
        email = self.req.get_json()['email']
        password = self.req.get_json()['password']
        result = ''        
        print(email);
        response = users.find_one({'email': email})        

        if response:
            if self.bcrypt.check_password_hash(response['password'], password):
                access_token = jwt.encode({'user': email, 'exp': datetime.utcnow() + timedelta(minutes=30)},
                                        self.app.config['JWT_SECRET_KEY'])
                result = dumps({
                    'token': 'loggedin',
                    'user_id': response['_id'],
                    'role': response['role'],
                })
            else:
                result = jsonify({'error': 'Invalid username or password.'}), 500
        else:
            result = jsonify({"result": 'Not registered'}), 500

        return result
    def logout(self):
        users = self.mongo.db.user
        email = self.req.uest.get_json()['email']
        password = self.req.get_json()['password']
        result = ''

        response = users.find_one({'email': email})

        if response:
            if self.bcrypt.check_password_hash(response['password'], password):
                result = jsonify({'token': ''})
            else:
                result = jsonify({'error': 'Invalid username or password.'})
        else:
            result = jsonify({"result": 'Not registered'})

        return jsonify({'result': result})
    
    def add_user(self):
        users = self.mongo.db.user
        first_name = self.req.get_json()['firstName']
        last_name = self.req.get_json()['lastName']
        email = self.req.get_json()['email']
        password = self.req.get_json()['password']
        hash_password = self.bcrypt.generate_password_hash(password).decode('utf-8')
        role = 'user'
        if email == 'admin':
            role = 'admin'
        created = datetime.utcnow()

        user_id = users.insert({
            'firstName': first_name,
            'lastName': last_name,
            'email': email,
            'password': hash_password,
            'role': role,
            'created': created
        })

        new_user = users.find_one({'_id': user_id})

        result = {'email': new_user['email'] + 'registered'}

        return jsonify({'result': result})
        

