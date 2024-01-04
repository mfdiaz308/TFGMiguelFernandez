import hashlib
import json
import unicodedata
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

# Execution data: {
#     time: 46s
#     files: 970
# }

# The name of each file is the hash of its url
def generate_hash(url):
   hash_obj = hashlib.sha256(url.encode())
   return hash_obj.hexdigest()

# Ignore special characters
def convert_to_utf8(var):
    return unicodedata.normalize('NFKD', var).encode('ascii', 'ignore').decode()

class EdxScrapper(CrawlSpider):
    name = 'edx_spider'
    start_urls = ['https://www.edx.org/sitemap']

    rules = (
        Rule(LinkExtractor(allow='doctorate'), callback='parse_items'),
        Rule(LinkExtractor(allow='bachelors'), callback='parse_items'),
        Rule(LinkExtractor(allow='masters'), callback='parse_items'),
        Rule(LinkExtractor(allow='certificates'), callback='parse_items'),
        Rule(LinkExtractor(allow='xseries'), callback='parse_items')
    )

    def parse_items(self,response):
        language = response.css('html ::attr(lang)').get()
        description = response.css('div.overview-info ::text').getall()

        if language in ['en','es'] and description is not None:
            name = response.css('title::text').get()

            if name is not None:
                name_utf8 = convert_to_utf8(name)
                url = response.url

                topics = response.css('ol.pathway span ::text').getall()

                topics_utf8 = []
                for topic in topics:
                    topics_utf8.append(convert_to_utf8(topic))

                # Se decide no añadir 'type', ya que no se guardan los archivos en carpetas diferentes

                description_utf8 = ''
                for desc in description:
                    description_utf8 += f'{convert_to_utf8(desc)} '

                outcomes = response.css('li.bullet-point.mb-2 ::text').getall()

                outcomes_utf8 = []
                for outcome in outcomes:
                    outcomes_utf8.append(convert_to_utf8(outcome))

                data = {
                    "url":url,
                    "name":name_utf8,
                    "topics":topics_utf8,
                    "skills":[],
                    "description":description_utf8,
                    "language":language,
                    "outcomes":outcomes_utf8
                }

                print(f'Processing: {url}')

                with open(f'C:/Users/migue/Escritorio/UPM/TFG/course_crawler_scrapy/course_crawler/course_crawler/spiders/course_crawler_data/edx/{generate_hash(url)}.json', 'w', encoding='UTF8') as f:
                    json.dump(data,f,indent=4)
        else:
            print('Unsupported language.')
