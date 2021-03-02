import scrapy
from urllib.parse import urljoin
from collections import defaultdict

class GolfCourseSpider(scrapy.spiders.SitemapSpider):
    name = 'golfadvisorcom'
    custom_settings = {"DOWNLOAD_DELAY": 0.25,
    }
    sitemap_urls = [
        'https://www.golfadvisor.com/sitemap1.xml',
        'https://www.golfadvisor.com/sitemap2.xml'
    ]

    def sitemap_filter(self, entries):
        for entry in entries:
            if  ('/courses/bvr/' or '/courses/badges/' or '/courses/feed/') in entry.get('loc'):
                continue
            if '/courses/' in entry.get('loc'):
                yield entry  
        
    def parse(self, response):
        
        # checking if it is an actual course page. excluded it for final ran, didnt fully
        # exists = response.css('.CoursePageSidebar-map').get()
        # if exists:

        # the page is split in multiple sections with different amount of details specified on each.
        # I decided to use nested for loop (for section in sections, for detail in section) to retrieve data.
        about_section = response.css('.CourseAbout-information-item')
        details_section = response.css('.CourseAbout-details-item')
        rental_section = response.css('.CourseAbout-rentalsServices-item')
        practice_section = response.css('.CourseAbout-practiceInstruction-item')
        policies_section = response.css('.CourseAbout-policies-item')

        sections = [
            about_section,
            details_section,
            rental_section,
            practice_section,
            policies_section
        ]
        # created a default list dict to add new details from for loops
        dict = defaultdict(list)
        # also have details added NOT from for loop sections, but hard coded using css and xpath selectors.
        dict = {
            'link': response.url,
            'Name': response.css('.CoursePage-pageLeadHeading::text').get().strip(),
            'Review Rating': response.css('.CoursePage-stars .RatingStarItem-stars-value::text').get('').strip(),
            'Number of Reviews': response.css('.CoursePage-stars .desktop::text').get('').strip().replace(' Reviews',''),
            '% Recommend this course': response.css('.RatingRecommendation-percentValue::text').get('').strip().replace('%',''),
            'Address': response.css('.CoursePageSidebar-addressFirst::text').get('').strip(),
            'Phone Number': response.css('.CoursePageSidebar-phoneNumber::text').get('').strip(),
            # website has a redirecting link, did not figure out how to get the main during scraping process
            'Website': urljoin('https://www.golfadvisor.com/', response.css('.CoursePageSidebar-courseWebsite .Link::attr(href)').get()),
            'Latitude': response.css('.CoursePageSidebar-map::attr(data-latitude)').get('').strip(),
            'Longitude': response.css('.CoursePageSidebar-map::attr(data-longitude)').get('').strip(),
            'Description': response.css('.CourseAbout-description p::text').get('').strip(),
            # here, I was suggested to use xpath to retrieve text. should it be used for the fields above and why?
            'Food & Beverage': response.xpath('//h3[.="Available Facilities"]/following-sibling::text()[1]').get('').strip(),
            'Available Facilities': response.xpath('//h3[.="Food & Beverage"]/following-sibling::text()[1]').get('').strip(),
            # another example of using xpath for microdata
            'Country': response.xpath("(//meta[@itemprop='addressCountry'])/@content").get('')
        }
        # nested for loop I mentioned above
        for section in sections:
            for item in section:
                dict[item.css('.CourseValue-label::text').get().strip()] = item.css('.CourseValue-value::text').get('').strip()
        
        yield dict