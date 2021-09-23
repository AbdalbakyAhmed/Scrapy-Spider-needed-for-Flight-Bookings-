import time

import requests
import json
import random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=500)
##
false = False
true = True
##
url = 'https://www.skyscanner.net/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner' \
      '&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs'
# data = {"market": "UK", "locale": "en-GB",
#         "currency": '',
#         "alternativeOrigins": false,
#         "alternativeDestinations": false,
#
#         "adults": 1,
#         "cabin_class": "business",
#         "child_ages": [9],
#         "options": {
#             "include_unpriced_itineraries": true,
#             "include_mixed_booking_options": true
#         },
#         "prefer_directs": false,
#         "state": {},
#         "viewId": "a582a7c1-dd0e-4748-a9a2-28eba87c86d4",
#         "travellerContextId": "3196f69d-d354-4a4d-91dc-9693d6138c60",
#         "trusted_funnel_search_guid": "a582a7c1-dd0e-4748-a9a2-28eba87c86d4",
#         "legs": [
#             {
#                 "origin": "CAI",
#                 "destination": "YTOA",
#                 "date": "2021-04-03",
#                 "return_date": "2021-04-10",
#                 "add_alternative_origins": false,
#                 "add_alternative_destinations": false
#             }
#         ]
#         }
# headers = {
#     'content-type': 'application/json',
#     'origin': 'https://www.skyscanner.net',
#     'user-agent': user_agent_rotator.get_random_user_agent(),
#     'x-skyscanner-channelid': 'website',
#     'x-skyscanner-devicedetection-ismobile': 'false',
#     'x-skyscanner-devicedetection-istablet': 'false',
#     'x-skyscanner-traveller-context': '283a9a65-0a27-43d3-a1ee-841db591ace0',
#     'x-skyscanner-utid': '283a9a65-0a27-43d3-a1ee-841db591ace0',
#     'x-skyscanner-viewid': '191df64e-d760-4f2f-9289-347dd128deb3',
# }


##
def get_payload_data(filter=dict()):
    time.sleep(5)
    data = {"market": "UK", "locale": "en-GB",
            "currency": '',
            "alternativeOrigins": false,
            "alternativeDestinations": false,

            "adults": 1,
            "cabin_class": "business",
            "child_ages": [9],
            "options": {
                "include_unpriced_itineraries": true,
                "include_mixed_booking_options": true
            },
            "prefer_directs": false,
            "state": {},
            "viewId": "a582a7c1-dd0e-4748-a9a2-28eba87c86d4",
            "travellerContextId": "3196f69d-d354-4a4d-91dc-9693d6138c60",
            "trusted_funnel_search_guid": "a582a7c1-dd0e-4748-a9a2-28eba87c86d4",
            "legs": [
                {
                    "origin": "CAI",
                    "destination": "YTOA",
                    "date": "2021-04-03",
                    "return_date": "2021-04-10",
                    "add_alternative_origins": false,
                    "add_alternative_destinations": false
                }
            ]
            }
    # get origin city code
    orig_id = \
    requests.get('https://www.skyscanner.net/g/autosuggest-flights/EG/en-GB/{}'.format(filter['from_city'])).json()[0][
        'PlaceId']
    # get destination city code
    dest_id = \
    requests.get('https://www.skyscanner.net/g/autosuggest-flights/EG/en-GB/{}'.format(filter['to_city'])).json()[0][
        'PlaceId']
    ##
    # Update the request payeload message
    data['currency'] = filter['currency']
    data['alternativeOrigins'] = filter['nearby_airports_from_city']
    data['alternativeDestinations'] = filter['nearby_airports_to_city']
    data['adults'] = filter['adults']
    data['cabin_class'] = filter['cabin_class']
    data['child_ages'] = filter['child_ages']
    data['prefer_directs'] = filter['non_stop_flights']
    data["legs"][0]['origin'] = orig_id
    data["legs"][0]['destination'] = dest_id
    data["legs"][0]['date'] = filter['departure_time']
    data["legs"][0]['return_date'] = filter['return_time']
    data["legs"][0]['add_alternative_origins'] = data['alternativeOrigins']
    data["legs"][0]['add_alternative_destinations'] = data['alternativeDestinations']

    print('\n \n \npayload message = ', data, '\n \n \n')
    return (get_request(data))  # Post request with search parameters

max_count  = 50 # for 5 miniute
temp_body = {}
def get_request(data=dict()):
    temp_data = data
    # temp_data = {"market":"UK","locale":"en-GB","currency":"USD","alternativeOrigins":true,"alternativeDestinations":true,"destination":{"id":"ROME","name":"Rome","cityId":"ROME","cityName":"Rome","countryId":"IT","type":"City","centroidCoordinates":[12.4908803859,41.8904833603],"geoContainerId":"27539793"},"adults":1,"cabin_class":"economy","child_ages":[],"options":{"include_unpriced_itineraries":true,"include_mixed_booking_options":true},"origin":{"id":"WASA","name":"Washington","cityId":"WASA","cityName":"Washington","countryId":"US","type":"City","centroidCoordinates":[-77.0104637903,38.9091498695],"geoContainerId":"27538424"},"outboundDate":"2021-07-12","prefer_directs":false,"state":{},"viewId":"dc9f1c2e-f690-45c9-8323-f85803a8d5d3","travellerContextId":"3196f69d-d354-4a4d-91dc-9693d6138c60","trusted_funnel_search_guid":"dc9f1c2e-f690-45c9-8323-f85803a8d5d3","legs":[{"origin":"WASA","destination":"ROME","date":"2021-07-12","add_alternative_origins":true,"add_alternative_destinations":true}]}
    headers = {
        'authority': 'www.skyscanner.net',
        'method': 'POST',
        'path': '/g/conductor/v1/fps3/search/?geo_schema=skyscanner&carrier_schema=skyscanner&response_include=query%3Bdeeplink%3Bsegment%3Bstats%3Bfqs%3Bpqs',
        'scheme': 'https',
        'accept': 'application/json',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
        'content-length': '1008',
        'content-type': 'application/json',
        # 'cookie': "_pxhd=dae57d649a6ff4a8f7460378626b484394e7daf025a75e5a95f58b97ea973a94:7ee9edb1-8fb3-11eb-9c9d-0bfaef19d2fe; abgroup=34939633; traveller_context=3196f69d-d354-4a4d-91dc-9693d6138c60; __Secure-ska=a35be55c-aede-4a66-8637-e2c81e95f551; device_guid=a35be55c-aede-4a66-8637-e2c81e95f551; preferences=3196f69dd3544a4d91dc9693d6138c60; _ga=GA1.2.877277841.1616928929; _pxvid=7ee9edb1-8fb3-11eb-9c9d-0bfaef19d2fe; ssculture=locale:::en-GB&market:::UK&currency:::USD; gdpr=information:::true&adverts:::true&version:::2; usbls=1; _csrf=LTak3SKosFQmKT0OjwVSqCaS; scanner=currency:::USD&legs:::CAI|2021-05-05|DEL|DEL|2021-05-07|CAI&to:::NYCA&preferDirects:::false&outboundAlts:::true&inboundAlts:::true&preferFlexible:::false&childrenV2&infants:::0&children:::0&from:::CAI&tripType:::one-way&rtn&iym:::2105&iday:::07&wy:::0&adultsV2:::1&adults:::1&oym:::2105&oday:::05; ssaboverrides=; ssab=AAExperiment_V9:::a&BD_Mobile_RR_Dbook_Partners_V3:::b&BD_Nearby_Map_V2:::b&BD_Web_flights_search_control_popular_destination_V2:::a&BD_improve_search_control_V2:::a&BD_preference_search_bar_V1:::b&BD_recommend_HotelCard_DV_V1:::a&EUR_flights_dbook_coupon_flow_V2:::b&EnableNewRelicPOC_V5:::a&FALCON_split_ap_northeast_1_V8:::a&FALCON_split_ap_southeast_1_V12:::a&FALCON_split_eu_central_1_V8:::a&FALCON_split_eu_west_1_V16:::a&Merchandise_Flights_StandAloneInsurance_Desktop_banner_V2:::b&WOM_new_tab_layout_V3:::d&content_service_split_ap_northeast_1_V5:::a&content_service_split_ap_southeast_1_V5:::a&content_service_split_eu_central_1_V5:::a&content_service_split_eu_west_1_V6:::a&cross_linking_service_split_ap_northeast_1_V3:::a&cross_linking_service_split_ap_southeast_1_V3:::a&cross_linking_service_split_eu_central_1_V3:::a&cross_linking_service_split_eu_west_1_V3:::a&culture_data_service_split_ap_northeast_1_V12:::a&culture_data_service_split_ap_southeast_1_V12:::a&culture_data_service_split_eu_central_1_V12:::a&culture_data_service_split_eu_west_1_V12:::a&dbook_eurw_trafficcontrol_web_desktop_100_V2:::a&dbook_gateway_split_ap_northeast_1_V7:::a&dbook_gateway_split_ap_southeast_1_V6:::a&dbook_gateway_split_eu_central_1_V7:::a&dbook_gateway_split_eu_west_1_V7:::a&dbook_leve_trafficcontrol_web_V1:::a&dbook_tkru_trafficcontrol_web_V1:::a&dbook_vuel_trafficcontrol_phase2_desktop_V5:::a&domestic_travel_version_control_web_V1:::a&entity_service_split_ap_southeast_1_V6:::a&fps_mr_fqs_flights_ranking_mandalore_V4:::a&hercules_carhire_split_ap_northeast_1_V5:::a&hercules_carhire_split_ap_southeast_1_V5:::a&hercules_carhire_split_eu_central_1_V5:::a&hercules_carhire_split_eu_west_1_V6:::a&hercules_split_ap_northeast_1_V5:::a&hercules_split_ap_southeast_1_V3:::a&hercules_split_eu_central_1_V3:::a&hercules_split_eu_west_1_V3:::a&hotels_website_split_ap_northeast_1_V7:::a&hotels_website_split_ap_southeast_1_V7:::a&hotels_website_split_eu_central_1_V8:::a&hotels_website_split_eu_west_1_V8:::a&inline_plus_ota_kiwi_test_premium_V1:::b&kaleidoscope_ingester_split_ap_northeast_1_V2:::a&kaleidoscope_ingester_split_ap_southeast_1_V2:::a&kaleidoscope_ingester_split_eu_central_1_V2:::a&kaleidoscope_ingester_split_eu_west_1_V3:::a&quote_suppression_split_ap_northeast_1_V2:::a&quote_suppression_split_ap_southeast_1_V3:::a&quote_suppression_split_eu_central_1_V2:::a&quote_suppression_split_eu_west_1_V8:::a&travel_restrictions_data_source_web_V5:::travelsafe; experiment_allocation_id=7602ed5893a175e064ee2e44086249e386ce29f906e7d958b71f26a07da8ab9d; _gid=GA1.2.1928661076.1618160378; _gat=1; _pxff_bsco=1; _fbp=fb.1.1618165350800.1862948961; akacd_Acorn_Split_Traffic=1618770155~rv=71~id=a8f6aab021fb5b8edf4a6af14c1d8a3f; _uetsid=4fe3a3d09ae711eba748b9f032823fa9; _uetvid=1cf630308fb411eba9de0dc7f9d919ed; _px3=fe7bc9b56f37a3e6b2f623688c2077d7732da2bd3d1798efa734c8c287698cff:ucwX4QiU2FxA0VbFvnuUXq9Xm9TpNe7l5gpt64QUFm/rZsds3U3tyRU7NBnxeLVK0uAHD6eeEnL8iW7op0D5gg==:1000:QH9Uyx/SaNhim3wejDetO7f7jJC+RAMR1l3LuFcZ8DnFkLwDomnNnjMVjlMpwQ4It/IllXLr9Fd3i7vjRLQdTHd9lqLORH7VdJL3EvVoauIy2pofFArFZoyab/UMjxiR0ZpQaOwvqj0iiBplhMh88h5UJwkyrtFmTmxwXSz9Sqs=",
        'origin': 'https://www.skyscanner.net',
        'referer': 'https://www.skyscanner.net/transport/flights/cai/nyca/210505/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&destinationentityid=27537542&inboundaltsenabled=false&infants=0&originentityid=27539681&outboundaltsenabled=false&preferdirects=false&preferflexible=false&ref=home&rtn=0',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': user_agent_rotator.get_random_user_agent(),
        'x-skyscanner-channelid': 'website',
        'x-skyscanner-devicedetection-ismobile': 'false',
        'x-skyscanner-devicedetection-istablet': 'false',
        'x-skyscanner-traveller-context': random.choice(['283a9a65-0a27-43d3-a1ee-841db591ace0', '3196f69d-d354-4a4d-91dc-9693d6138c60', 'a824aa4d-cb9c-49e0-86b3-f6611e07bb65']),
        'x-skyscanner-utid': random.choice(['283a9a65-0a27-43d3-a1ee-841db591ace0', '3196f69d-d354-4a4d-91dc-9693d6138c60', 'a824aa4d-cb9c-49e0-86b3-f6611e07bb65']),
        'x-skyscanner-viewid': random.choice(['191df64e-d760-4f2f-9289-347dd128deb3', '43d336dd-9f54-49d8-91a2-32dfd1747242', '53b0c73b-5921-4641-8b53-0b83da435178'])
    }
    print("\n \n user_agent= \n", headers['user-agent'], "\n \n")
    
    with requests.Session() as s:
        json_payload = s.post(url, headers=headers, data=json.dumps(temp_data)).json()
        print(json_payload)

    if ("itineraries" in json_payload) and len(json_payload['itineraries']) > 10:
        print("\n \n Num of Tickets = ",len(json_payload['itineraries']), "\n \n")
        return json_payload
    else:
        global max_count
        global temp_body
        max_count -= 1
        # print("\n count=\t",max_count,"\n")
        if ("itineraries" in json_payload) and len(json_payload['itineraries']) <= 10:
            print("\n \n Num of Tickets = ",len(json_payload['itineraries']), "\n \n")
            temp_body = json_payload
        ##
        if max_count == 0:
            return temp_body
        ##
        time.sleep(2)
        return get_request(temp_data)
    # global max_count


'''
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us; Silk/1.1.0-80) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16 Silk-Accelerated=true',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',

]
filters = {
    'from_city' : 'Cairo',  
    'to_city' : 'Toronto',   
    'departure_time' : '2021-05-05',
    'return_time' : '2021-05-06',
    'currency':'usd',
    'adults' : 3,
    'childerns' : 3,
    'child_ages':[3,10,12],
    'cabin_class' : 'economy', #economy, premiumeconomy, business or first 
    'nearby_airports_from_city' : True,
    'nearby_airports_to_city' : True,
    'non_stop_flights' : True,
    'flexible_tickets' : True
}

def get_payload_data (filter=dict()):
    org_id = ''
    dest_id = ''
    child_age = ''
    suggest_url = "https://www.skyscanner.net/g/autosuggest-flights/USA/en-GB/"
    req = requests.get(suggest_url+str(filter['from_city']))
    if req.status_code == 200:
        data = req.json()
        org_id = data[0]['PlaceId']
        originentityid = data[0]['GeoContainerId']
    else:
        print("Failed to load from city abbreviation")
    ##
    req = requests.get(suggest_url+str(filter['to_city']))
    if req.status_code == 200:
        data = req.json()
        dest_id = data[0]['PlaceId']
        destinationentityid = data[0]['GeoContainerId']
    else:
        print("Failed to load to city abbreviation")
    ####
    if len(filter['child_age']) > 1:
        i = 1
        while i < len(filter['child_age']):
            child_age = child_age + "%7c" + str( filter['child_age'][i] )
            i += 1
        child_age = str( filter['child_age'][0] ) + child_age
        print("child_age = ", child_age)
    elif len(filter['child_age']) == 1:
        child_age = filter['child_age'][0]
    else:
        pass
    search_url = "https://www.skyscanner.com/transport/flights/{orig}/{dest}/{dep_t}/{arr_t}/?adults={d1}&adultsv2={d1}".format(
        orig=org_id, 
        dest=dest_id, 
        dep_t=filter['departure_time'].replace('-',''), 
        arr_t=filter['return_time'].replace('-',''),
        d1=str(filter['adults'])
        )
    search_url = search_url + "&cabinclass={d1}&children={d2}&childrenv2={d3}&currency={dd3}&inboundaltsenabled={d4}&market=US&outboundaltsenabled={d5}".format(
        d1=filter['cabin_class'], 
        d2=str(filter['childerns']), 
        d3=child_age,
        dd3 = filter['currency'], 
        d4=filter['nearby_airports_to_city'], 
        d5=filter['nearby_airports_from_city']
    )
    search_url = search_url + "&preferdirects={d1}&preferflexible={d2}&ref=home&rtn=1".format(
        d1 = filter['non_stop_flights'],
        d2 = filter['flexible_tickets']
    )
    print("\n \n \n search url = ")
    print(search_url.lower() ,"\n \n \n")
    return( search_url.lower() )

'''
