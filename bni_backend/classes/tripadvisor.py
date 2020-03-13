import requests
import json

class tripadvisor:
    def __init__(self, key):
        super().__init__()
        self.key = key      
        self.key = "6f44686b06mshc39b79231f8e93dp138755jsnda2781dd3234"  
        self.header = {
        'Accept': "application/json",        
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",    
        'x-rapidapi-host' : 'tripadvisor1.p.rapidapi.com',
        'x-rapidapi-key' :  self.key
        }

    def getNearByLocationId(self,lat,lng):
        url = "https://maps.googleapis.com/maps/api/place/details/json?"
        res = requests.request("GET", url  ,data="",  headers=self.header)
        return  res.json()  

    def getSearchLocationId(self, lat, lng , offset):
        querystring = {"limit":"1","offset":str(offset),"lang":"en_US","latitude":str(lat),"longitude":str(lng)}
        url = "https://tripadvisor1.p.rapidapi.com/restaurants/list-by-latlng" 
        response = requests.request("GET", url, headers=self.header, params=querystring)
        return  response.json()
    
    def getLocation(self, res):        
        datas = res["data"]        
        if(len(datas) > 0 ):
            for data in datas:    
                location_id = data["location_id"]
                return location_id

                # result_type = data["result_type"]                        
                # address_obj = data["result_object"]["address_obj"]
                
                # country =  address_obj["country"]
                # if result_type == "restaurants" and country == "United Kingdom":
                #     location_id = data["result_object"]["location_id"]
                #     return location_id
        return ""

    def getPhone(self, res):
        datas = res["data"]        
        if(len(datas) > 0 ):
            for data in datas:
                try:
                    ratingCount = data["phone"]
                    return ratingCount
                except:
                    return ""
        return ""

    def getRatingValue(self, res):
        datas = res["data"]        
        if(len(datas) > 0 ):
            for data in datas:
                try:
                    ratin = float(data["rating"])
                    return ratin
                except:
                    return 5
        return 5

    def getRating(self, res):        
        datas = res["data"]        
        if(len(datas) > 0 ):
            for data in datas:
                ratingCount = data["num_reviews"]
                return ratingCount


            # for data in datas:            
            #     result_type = data["result_type"]                        
            #     address_obj = data["result_object"]["address_obj"]
                
            #     country =  address_obj["country"]
            #     if result_type == "restaurants" and country == "United Kingdom":
            #         rating =  res["results"][0]["rating"]
            #         return rating
        return "0"

    def getDetails(self, placeid, offset, limit):        
        querystring = {"location_id":placeid,"limit":limit,"offset":str(offset),"lang":"en_US","currency":"USD"}
        url = "https://tripadvisor1.p.rapidapi.com/reviews/list"
        response = requests.request("GET", url, headers=self.header, params=querystring)
        return  response.json()
        
    
        
