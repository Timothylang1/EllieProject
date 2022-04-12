import scrapy
from scrapy.crawler import CrawlerProcess


total = []
class MySpider(scrapy.Spider):
    name = 'myspider'

    def __init__(self, *args, **kwargs):
        self.myurls = kwargs.get('myurls', [])
        super(MySpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.myurls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        data = response.text
        print(data)

        # print("THIS IS DATA" + data)
        initialCoor = data.find("center=") + 7
        middlePlace = data.find("%2C", initialCoor)
        endPlace = data.find("&amp", middlePlace)

        lat = float(data[initialCoor : middlePlace])
        long = float(data[middlePlace + 3 : endPlace])
        total.append([lat, long])
        # print("HERE IT IS LATITUDE = " + lat)


def thisWorks():
    process = CrawlerProcess()
    process.crawl(MySpider, myurls = [
    "https://www.google.com/maps/search/1095+McGregor+Way+Palo+Alto", 
    "https://www.google.com/maps/search/859+Barron+Ave+Palo+Alto"
    ])

    process.start()
    print(total)


thisWorks()



