import requests
import json
from flask import Flask, jsonify, json
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.json_util import dumps
from datetime import datetime, timedelta
import jwt
from .google import google
from .tripadvisor import tripadvisor
from bson import ObjectId  # For ObjectId to work

class review_controller:

    def __init__(self,  app, mongo , bcrypt, req):
        self.mongo = mongo
        self.app = app
        self.bcrypt = bcrypt
        self.req = req

    def get_reviews(self, res_id, name):
        
        google_call(res_id, name)
        tripadvisor_call(res_id , name )                                       
        if res_id:
            reviews = mongo.db.review.find({'restaurant_id': res_id})
        else:
            reviews = mongo.db.review.find()        
        resp = dumps(reviews)
        return resp

    def get_view_more_google(self, _id, query, location_id):
        gInstance = google("")
        res = gInstance.getDetails(location_id)        
        print(res)        
        if( res["status"] == "OK"):                
            reviews = res["result"]["reviews"]
            total_review = []
            for item in reviews :
                item = self.get_google_item(item, location_id, _id)                      
                total_review.append(item)
            return total_review                

    def get_view_more(self,_id, query, offset, location_id):
        tripInstance = tripadvisor("")   
        
        if location_id != "" and location_id != "0":
            res = tripInstance.getDetails(location_id, offset * 5 , 5)                        
            if len(res["data"]) > 0 :
                reviews  = res["data"]
                total_review = []
                for item in reviews :
                    item = self.get_trip_item(item, location_id, _id)
                    total_review.append(item)
                return total_review
        else:
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

                        index = 0

                        #old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )
                        self.mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                            {'$set': { 'tripadvisor_location_id' : location_id }})
                        #for offset in range(1): # range(int(int(num_reviews)/20) + 1 + index):
                        try:
                            print("--------------offset ------------")
                            print(offset)

                            res = tripInstance.getDetails(location_id, offset * 5 , 5)                        
                            if len(res["data"]) > 0 :
                                reviews  = res["data"]
                                total_review = []
                                for item in reviews :
                                    item = self.get_trip_item(item, location_id, _id)
                                    total_review.append(item)
                                return total_review
                        except ValueError:   
                            #index = index + 1                     
                            print("Oops!  That was no valid number.  Try again...")                           
                    else:
                        return []
            else:
                return []
        return []

    def google_call(self, _id, query):   
                
        gInstance = google("key")
        try:
            res = gInstance.getSearchLocationId(query)  
            if( res != ""):       
                status = res["status"]        
                if(status == "OK"):
                    if( len(res["results"]) > 0  and  "United Kingdom" in res["results"][0]["formatted_address"] ):
                        placeId = res["results"][0]["place_id"]
                        rating =  res["results"][0]["rating"]
                        res = gInstance.getDetails(placeId)       
                        print(placeId)     
                        self.mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                                {'$set': { 'google_location_id' : placeId}})

                        if( res["status"] == "OK"):                
                            reviews = res["result"]["reviews"]

                            for item in reviews :
                                total_review = self.add_google_review(item, placeId, _id)                                
                                self.mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                                                        {'$set': {'id_review.reviews':  total_review }})
                            # reviews = res["result"]["reviews"]
                            #mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                            #                        {'$set': {'rating':math.ceil( (float(old["rating"]) + float(rating))/2 ) , 'google' : '1', 'review_count':len(reviews)}})
                        else:
                            return "Fail"
                    else:
                        return "Fail"    
                else:
                    return "Fail"
            else:
                return "Retry"
        except ValueError:   
                #index = index + 1                     
                print("Oops!  That was no valid number.  Try again...")
                return "Fail"                    
        return  "Ok"

    # ============== Add Tripadvisor Res ===================

    def tripadvisor_call(self, _id, query, offset = '0'):    
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

                    index = 0

                    #old = mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id) } )
                    self.mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                        {'$set': { 'tripadvisor_location_id' : location_id }})

                    for offset in range(1): # range(int(int(num_reviews)/20) + 1 + index):
                        try:
                            res = tripInstance.getDetails(location_id, offset - index, 5)
                            print(str(offset - index ))
                            if len(res["data"]) > 0 :
                                reviews  = res["data"]
                                for item in reviews :
                                    total_review = self.add_tripadvisor_review(item, location_id, _id)
                                    self.mongo.db.restaurant.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)},
                                                {'$set': {'id_review.reviews':  total_review }})
                                
                        except ValueError:   
                            #index = index + 1                     
                            print("Oops!  That was no valid number.  Try again...")                           
                else:
                    return "Fail"
        else:
            return "Fail"
        return "Ok"                
        
    def add_google_review(self, item, placeId, _id):
        
        item = self.get_google_item(item, placeId, _id)

        restaurant = self.mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)})
        reviews =  restaurant["id_review"]['reviews']    
        total_review = []
        for reviw_item in reviews:
            total_review.append(reviw_item)
        total_review.append(item)

        return total_review
        

    def add_tripadvisor_review(self, item, placeId, _id):    
        item = self.get_trip_item(item, placeId, _id)

        total_review = []
        restaurant = self.mongo.db.restaurant.find_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)})
        reviews =  restaurant["id_review"]['reviews']    

        for reviw_item in reviews:
            total_review.append(reviw_item)
        total_review.append(item)
        
        return total_review


    def get_trip_item(self, item, placeId, _id):
        author_name = item["user"]['username']
        author_url = item['url']
        language = item['lang']
        profile_photo_url = item['user']['contributions']['avatar_thumbnail_url']
        rating = item['rating']
        relative_time_description = item['travel_date']
        text = item['text']

        time = item['published_date']
        title = item['title']

        item = {        
            'url': author_url,        
            'rating': rating,
            'relative_time_description': relative_time_description,
            'text': text,
            'time_created': time,
            'placeId':placeId,
            'id':_id,
            'user': {
                'profile_url':profile_photo_url,
                'image_url':profile_photo_url,
                'name':author_name
            }        
        }
        return item


    def get_google_item(self, item, placeId, _id):
        author_name = item['author_name']
        author_url = item['author_url']
        language = item['language']
        profile_photo_url = item['profile_photo_url']
        rating = item['rating']
        relative_time_description = item['relative_time_description']
        text = item['text']
        time = item['time']
        
       
        item = {        
            'url': author_url,        
            'rating': rating,
            'relative_time_description': relative_time_description,
            'text': text,
            'time_created': time,
            'placeId':placeId,
            'id':_id,
            'user': {
                'profile_url':profile_photo_url,
                'image_url':profile_photo_url,
                'name':author_name
            }        
        }
        return item

        


    