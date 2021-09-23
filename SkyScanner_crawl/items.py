# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SkyscannerCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Airline_name = scrapy.Field()
    Ticket_provider_name = scrapy.Field()
    flexible_ticket = scrapy.Field()
    Departure_time = scrapy.Field()
    Arrival_time = scrapy.Field()
    Flight_duration = scrapy.Field()
    Non_Stop = scrapy.Field()
    Stop_Count = scrapy.Field()
    #which stops ??
    Price = scrapy.Field()
    Skyscanner_ticket_link = scrapy.Field()
    Airline_company_booking_link = scrapy.Field()
    # Best_link = scrapy.Field()
    Cheapest_link = scrapy.Field()
    Fastest_link = scrapy.Field()
    
