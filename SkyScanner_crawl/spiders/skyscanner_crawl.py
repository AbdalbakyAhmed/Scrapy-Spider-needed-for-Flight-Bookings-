import scrapy
import time
import sys
from scrapy import Request
from scrapy.exceptions import CloseSpider
import requests
from SkyScanner_crawl.items import SkyscannerCrawlItem
from .utils_search import get_payload_data

class  SkyScanner(scrapy.Spider):
    name = 'skyscanner'
    start_urls = [
        # "https://www.skyscanner.net/transport/flights/cai/nyca/210505/?adults=1&adultsv2=1&cabinclass=economy&children=0&childrenv2=&destinationentityid=27537542&inboundaltsenabled=false&infants=0&originentityid=27539681&outboundaltsenabled=false&preferdirects=false&preferflexible=false&ref=home&rtn=0",
        "https://www.skyscanner.com"
    ]
    filters = {
        'from_city': 'Washington Ronald Reagan',
        'to_city': 'Dublin',
        'departure_time': '2021-09-14',
        'return_time': '', #e.g. 2021-06-06
        'currency': 'USD',
        'adults': 1,    #e.g. 5 "integer number"
        'childerns': 0, #e.g. 3 "integer number"
        'child_ages': [], #e.g. [3,5,6]
        'cabin_class': 'economy', #economy, premiumeconomy, business or first
        'nearby_airports_from_city': False, #True or False
        'nearby_airports_to_city': True,   #True or False
        'non_stop_flights': False, #True or False
        'flexible_tickets': False   #True or False
    }

    def parse(self, response):
        """
             This method is being run by default when the spider starts.
         :param response: The response from the start URL request
         :return:
         """
        time.sleep(5)  # delay between system requests
        # Load the response payload from website
        json_response = get_payload_data(SkyScanner.filters)
        # print( "\n \n .....\n", json_response ,"\n \n ......." )
        item = SkyscannerCrawlItem()

        ##
        # get origin city code
        orig_id = requests.get('https://www.skyscanner.net/g/autosuggest-flights/EG/en-GB/{}'.format(SkyScanner.filters['from_city']) ).json()[0]['PlaceId']
        # get destination city code
        dest_id = requests.get('https://www.skyscanner.net/g/autosuggest-flights/EG/en-GB/{}'.format(SkyScanner.filters['to_city']) ).json()[0]['PlaceId']
        ##
        
        min_price = json_response['stats']['itineraries']['total']['min_price'] #price
        min_duration = json_response['stats']['itineraries']['min_longest_itinerary_leg_duration'] #time in minutes
        ##

        
        #create new dictionary contains all agentIDs which provide the ticket price 
        agents_names = dict()
        for agent in json_response['agents']:
            agents_names[ agent['id']] = agent['name']
        ##
        
        #create new dictionary contains all tickets data
        tickets_info = dict()
        for _info in json_response['legs']:
            lst = [_info['departure'], _info['arrival'], _info['duration'], _info['stop_count'], str(_info['operating_carrier_ids'][-1])]
            tickets_info[ _info['id'] ] = lst          
        ##
        
        #create new dictionary contains all Airline carriers "Companies"
        carrier_name = dict()
        for carrier in json_response['carriers']:
            carrier_name[ str( carrier['id'] ) ] = carrier['name']
        ##
        
        # Create list contains flexible agents names 
        temp_dict = json_response['plugins'][-1]['universal_product_brand_attributes']['agents']
        flexible_agents = list(temp_dict.keys())
        ##

        print("\n \n \n", agents_names, "\n \n \n", tickets_info, "\n \n \n", carrier_name, "\n \n \n",flexible_agents , "\n \n \n")
        time.sleep(2)
        
        print("Num of Tickets providers = {}".format( len( json_response["itineraries"]) ) )
        count = 0
        while count < len(json_response["itineraries"]) :
            flg_fast = False
            # Items Arguments "varriables"
            provide_name = ""
            flexible_ticket = ""
            departure_time = ""
            arrival_time = ""
            flight_duration = 0
            stop_count = 0
            non_stop = ''
            airline_company = ''
            price = 0
            skyscanner_ticket_link = ''
            airline__booking_link = ''
            cheapest_link = ''
            fastest_link = ''
            ##
            # Ticket id
            container = json_response["itineraries"][count]
            ##
            ticket_id = container['leg_ids'][0]
            ''' ticket_id consists of "origin_airport_id-date_time -- Airline_company- quote_age- destination_airport_id" '''
            ##
            #Ticket provider Agent Name
            agent_id = container['pricing_options'][0]['agent_ids'][0]
            print("\n agent_id= ", agent_id)
            if agent_id in agents_names:
                provide_name = agents_names[agent_id]
                if agent_id in flexible_agents:
                    flexible_ticket = 'Yes'
                else:
                    flexible_ticket = 'No'
            else:
                provide_name = None
                flexible_ticket = None
            ##
            # # This extracts the Departure/Arrival Time, Flight duration, Non-Stop item
            if ticket_id in tickets_info :
                temp_info = tickets_info[ticket_id]
                departure_time = temp_info[0]
                arrival_time = temp_info[1]
                # flight_duration = tickets_info[ticket_id][2] # in Minutes
                flight_duration = format( int(temp_info[2])/60 , ".2f") #Format duration in hours
                # for fastest link scope:
                if temp_info[2] == min_duration:
                    flg_fast = True
                else:
                    flg_fast = False
                ##
                stop_count = temp_info[3]
                if temp_info[3] > 0:
                    non_stop = 'No'
                else:
                    non_stop = 'Yes'
                # Airline Company name
                if temp_info[4] in carrier_name:
                    airline_company = carrier_name[temp_info[4]]
                else:
                    airline_company = None
            else:
                departure_time = None
                arrival_time = None
                flight_duration = None
                stop_count = None
                airline_company = None                   
            ##
            # Ticket Price
            # price = int(container['pricing_options'][0]['price']['amount'])/2
            price = container['pricing_options'][0]['price']['amount']
            ##
            # Ticket Link
            '''Format the date from "2021-05-20" to "210520"'''
            dep_time = SkyScanner.filters['departure_time'][2:].replace("-",'')
            arr_time = SkyScanner.filters['return_time'][2:].replace("-",'') 
            skyscanner_ticket_link = "https://www.skyscanner.net/transport/flights/{d1}/{d2}/{d3}/{d4}/config/{d5}".format(
                d1 = orig_id,
                d2 = dest_id,
                d3 = dep_time,
                d4 = arr_time,
                d5 = container["id"]
            )
            ##
            # Airline compane booking deeplink
            deeplink = container['pricing_options'][0]['items'][0]['url']
            airline__booking_link = "https://www.skyscanner.net" + deeplink
            ##
            # cheapest and fastest link
            if price == min_price:
                cheapest_link = skyscanner_ticket_link 
            else:
                cheapest_link = None
            #
            if flg_fast:
                fastest_link = skyscanner_ticket_link
            else:
                fastest_link = None
            # 
            count += 1
            # Collecting Items
            item['Airline_name'] = airline_company
            item['Ticket_provider_name'] = provide_name
            item['flexible_ticket'] = flexible_ticket
            item['Departure_time'] = departure_time
            item['Arrival_time'] = arrival_time
            item['Flight_duration'] = flight_duration
            item['Stop_Count'] = stop_count
            item['Non_Stop'] = non_stop
            item['Price'] = price
            item['Skyscanner_ticket_link'] = skyscanner_ticket_link
            item['Airline_company_booking_link'] = airline__booking_link
            item['Cheapest_link'] = cheapest_link
            item['Fastest_link'] = fastest_link
            ##
            yield(item)

    def closed(self, reason):
        print("\n \n \n FINISHED \n \n \n")







        


        

    
        

        
    # def selenium_parse(self):
    #     print("\n \n \n Start...    \n \n \n")
    #     # binary = FirefoxBinary('path/to/installed firefox binary') #path/to/installed firefox binary ? >> which firefox => /usr/bin/firefox
    #     # browser = webdriver.Firefox(firefox_binary=binary)  
    #     self.options = selenium.webdriver.FirefoxOptions()
    #     # options.add_argument("--headless")
    #     self.browser = selenium.webdriver.Firefox(firefox_options=self.options)
    #     time.sleep(1) #wait 5 sec
    #     self.browser.get(SkyScannerSpider.start_urls[0]) #load website
    #     time.sleep(5)
    #     element = self.browser.find_element_by_name("fsc-origin-search")
    #     element.send_keys(" ")
    #     time.sleep(5)
    #     element.send_keys("Cairo")
    #     time.sleep(5)
    #     element = self.browser.find_element_by_name("fsc-destination-search")
    #     element.send_keys("Torino")
    #     time.sleep(5)
    #     y = self.browser.find_element_by_class_name("BpkButtonBase_bpk-button__3QGRV.BpkButtonBase_bpk-button--large__2KqI4.App_submit-button__3h6Y5.App_submit-button-oneline__1v1tr")
    #     y.click()
    #     time.sleep(3)
    #     return self.browser.current_url
        





