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

    def getSearchLocationId(self, query , offset):
        querystring = {"limit":"30","sort":"relevance","offset":str(offset),"lang":"en_US","currency":"USD","units":"km","query":query}
        url = "https://tripadvisor1.p.rapidapi.com/locations/search" 
        response = requests.request("GET", url, headers=self.header, params=querystring)
        return  response.json()
    

    def getDetails(self, placeid, offset):        
        querystring = {"location_id":placeid,"limit":"20","offset":str(offset),"lang":"en_US","currency":"USD"}
        url = "https://tripadvisor1.p.rapidapi.com/reviews/list"
        response = requests.request("GET", url, headers=self.header, params=querystring)
        return  response.json()
        
