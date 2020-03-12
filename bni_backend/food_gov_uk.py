# all establishments details on - https://ratings.food.gov.uk/OpenDataFiles/FHRS807en-GB.xml
import requests
from app import db_client

BaseUrl = "https://ratings.food.gov.uk/{0}/json"
headers = {'x-api-version': '2'}


# Get all ratings of a restaurant from food.gov.uk webstie
def getRatings(fhrs_id):
    try:
        response = requests.get(BaseUrl.format("business/" + str(fhrs_id)), headers=headers)
        data = response.json()
        edetails = data["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"]
        return createDetailsDict(edetails)
    except Exception as e:
        print(e)
        return {}


# Get address of a restaurant from details dictionary
def getAddress(edetails):
    addr = []
    addrKeys = ["AddressLine1", "AddressLine2", "AddressLine3", "AddressLine4"]
    for ak in addrKeys:
        if ak in edetails and not edetails[ak] is None:
            addr.append(str(edetails[ak]).strip())
    return ','.join(addr)


# Create output dictionary which contains details of a restaurant
def createDetailsDict(edetails):
    result = dict()
    scores = edetails['Scores']
    result['fhrs_id'] = edetails['FHRSID']
    result['name'] = edetails['BusinessName']
    result["rating_details"] = {'rating': edetails['RatingValue'], 'hygiene': scores['Hygiene'],
                                'structural': scores['Structural'],
                                'confidenceInManagement': scores['ConfidenceInManagement']}
    result["address"] = getAddress(edetails)
    return result


# extract required details of a restaurant from result from food.gov.uk website
def extractDetails(est):
    ecollections = est['FHRSEstablishment']['EstablishmentCollection']['EstablishmentDetail']
    return [createDetailsDict(e) for e in ecollections]


# get all Belfast restaurants/cafe
# belfast authority code is 807
# restaurants/cafe business type  is 1
# last int in url is number of records to fetch
def get_all_restaurants(total_restaurants):
    ep = BaseUrl.format("enhanced-search/en-GB/^/^/ALPHA/1/807/1/" + str(total_restaurants))
    response = requests.get(ep, headers=headers)
    return extractDetails(response.json())


# update data in database for restaurants
def update_restaurant_data():
    data = get_all_restaurants(5000)
    print("Updating restaurant records in database")
    for d in data:
        db_client.add_restaurant(d)
