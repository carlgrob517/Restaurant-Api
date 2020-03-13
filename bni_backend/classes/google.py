import requests
import json

class google:
    def __init__(self, key):
        super().__init__()
        self.key = key
        self.key = 'AIzaSyBRHZ24e9OnPUSM4J2pLfOzVGrXBkFia_g'        
        self.key = 'AIzaSyD1wxxlef3Y5W6ImNdB1DhTWKRUP-lKENo'        
        self.header = {
        'Accept': "application/json",        
        'Cache-Control': "no-cache",
        'Content-Type': "application/json",    
        }

    def getNearByLocationId(self,lat,lng):
        url = "https://maps.googleapis.com/maps/api/place/details/json?"
        res = requests.request("GET", url  ,data="",  headers=self.header)
        return  res.json() 

    def getSearchLocationId(self, query):
        try:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query + "&key=" + self.key
            res = requests.request("GET", url  ,data="",  headers=self.header)
            return  res.json()
        except Exception:   
            print('error')
            return ""
    
    
    def getLocation(self, res):
        if( res != ""):       
            status = res["status"]        
            if(status == "OK"):
                if( len(res["results"]) > 0  and  "United Kingdom" in res["results"][0]["formatted_address"] ):
                    placeId = res["results"][0]["place_id"]
                    return placeId
                if( len(res["results"]) > 0  and  "Ireland" in res["results"][0]["formatted_address"] ):
                    placeId = res["results"][0]["place_id"]
                    return placeId
                
        return ""

    def getRatingValue(self, res):
        if( res != ""):       
            status = res["status"]        
            if(status == "OK"):
                if( len(res["results"]) > 0  and  "United Kingdom" in res["results"][0]["formatted_address"] ):
                    rating = float(res["results"][0]["rating"])
                    return rating
        return 5


    def getDetails(self, placeid):
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + placeid +  "&key=" + self.key
        #params = "{'location_id': " + str(location_id) + "}"
        res = requests.request("GET", url  ,data="",  headers=self.header)
        return  res.json()
