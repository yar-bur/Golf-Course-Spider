import scrapy
from urllib.parse import urljoin

class GolfCourseSpider(scrapy.Spider):
    name = 'golfnationwide'

    start_urls = [
        'http://www.golfnationwide.com/Default.aspx'
    ]
    
    def parse(self, response):
        links = response.css('td a::attr(href)').extract()
        for link in links:
            url = urljoin(response.url, link)
            yield scrapy.Request(url, callback=self.parse_second)
    
    def parse_second(self, response):
        links = response.css('td a::attr(href)').extract()
        for link in links:
            url = urljoin(response.url, link)
            yield scrapy.Request(url, callback=self.parse_course)

    def parse_course(self, response):
        details = [tag.css('::text').get(default='') for tag in response.css('dl span')]
        website_link = response.css('dl dd a::attr(href)').get()
        yield{
            'Course Name': details[0],
            'Street': details[1],
            'City/State': details[2] +'/'+ details[3],
            'Zip': details[4] +'-'+ details[5],
            'County': details[6],
            'Email': details[7],
            'Website': website_link,
            'Phone': details[8],
            'Fax': details[9],
            'Description': details[10],
            'Classification': details[11],
            'Year Built': details[12],
            'Annual Rounds': details[13],
            'Season': details[14],
            'Manager': details[15],
            'Club Pro': details[16],
            'Superintendant': details[17],
            'Guest Policy': details[18],
            'Designer': details[19],
            'Pro Shop Hours': details[20],
            'Dress Code': details[21],
            'Greens Fees Weekend': details[22],
            'Greens Fees Weekday': details[23],
            'Tee Time Reservation': details[24],
            'Online Reservation': details[25],
            'Earliest Tee Time': details[26],
            'Holes': details[27],
            'Greens': details[28],
            'Fairways': details[29],
            'Water Hazards': details[30],
            'Bunkers': details[31],
            'Metal Spikes': details[32],
            'Greens Aerated': details[33],
            'Overseeding': details[34],
            'Five Somes': details[35],
        }