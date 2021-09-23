### Scrapy Spider needed for Flight Bookings 

A Python Scrapy spider for `https://www.skyscanner.com`. The spider should take the following inputs:
- From city
- To city
- Number of adults
- Currency (please write for USD)
- Class (Economy, Economy premium, business, first class)
- Include nearby airports from city (boolean True/ False)
- Include nearby airports to city (boolean True/ False)
- Non-stop flights (boolean True/ False)
- Flexible Tickets only (boolean True/ False)
- Departure date
- Return date
- Departure time range e.g. 5pm - midnight
- Arrival time range, e.g. 9am-3pm

It must be able to `support roundtrip`, and `one-way` trips. If only the departure date is given, then it should be assumed it is a one-way trip.

Once it searches, it should scrape the:
- Airline name
- If it is a flexible ticket
- Departure time
- Arrival time
- Flight duration
- If it is non-stop
- Which stops, if any
- Price
- Link to booking details
- Best, cheapest, and fastest links along with prices and durations
