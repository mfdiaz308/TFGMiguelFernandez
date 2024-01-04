import hashlib
import json
import unicodedata
import scrapy

# Execution data: {
#     time: 2488s = 41 min
#     files: 13227
# }

# The name of each file is the hash of its url
def generate_hash(url):
   hash_obj = hashlib.sha256(url.encode())
   return hash_obj.hexdigest()

# Ignore special characters
def convert_to_utf8(var):
    return unicodedata.normalize('NFKD', var).encode('ascii', 'ignore').decode()

class CourseraScrapper(scrapy.Spider):
    name = 'coursera_spider'

    def start_requests(self):
        # Sitemaps de cada tipo de curso
        sitemaps_urls = [
            'https://www.coursera.org/sitemap~www~courses.xml', #course -> /learn
            'https://www.coursera.org/sitemap~www~professional-certificate.xml', #certificate -> /certificates
            'https://www.coursera.org/sitemap~www~onDemandSpecializations.xml', #specialization -> /specializations
            'https://www.coursera.org/sitemap~www~mastertrack.xml', #mastertrack -> /mastertrack 
            'https://www.coursera.org/sitemap~www~guided-projects.xml' #project -> /projects
        ]

        for sitemap in sitemaps_urls:
            yield scrapy.Request(url=sitemap, callback=self.parse_sitemap)

    def parse_sitemap(self, response):
        # Parsea el sitemap  y extrae las urls
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = response.xpath('//ns:url/ns:loc/text()', namespaces=namespaces).getall()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # Scrapea solo si el idioma es español o inglés y tiene descripcion
        try:
            language = response.css('div.css-ddn3zj ::text').get().split(' ')[2]
        except:
            print(f'Exception: language not found')
            return
        # description = response.css('div.rc-TogglableContent.about-section ::text').getall()
        description = response.css('div.css-1m8ahwj ::text').getall()

        if language in ['English','Spanish'] and description is not None:
            name = response.css('title::text').get()

            if name is not None:
                name_utf8 = convert_to_utf8(name)

                url = response.url

                topics = response.css('a.cds-119.cds-113.cds-115.css-mzc3kb.cds-142::text').getall()
                topics_utf8 = []
                for topic in topics:
                    topics_utf8.append(convert_to_utf8(topic))

                skills = response.css('li.cds-9.css-0.cds-11.cds-grid-item.cds-56.cds-64 ::text').getall()
                skills_utf8 = []
                for skill in skills:
                    skills_utf8.append(convert_to_utf8(skill))

                # Se decide no añadir 'type', ya que no se guardan los archivos en carpetas diferentes
                
                description_utf8 = ''
                if description is not None:
                    for desc in description:
                        description_utf8 += f'{convert_to_utf8(desc)} '

                outcomes = response.css('ul.cds-9.css-7avemv.cds-10 ::text').getall()
                outcomes_utf8 = []
                for outcome in outcomes:
                    outcomes_utf8.append(convert_to_utf8(outcome))

                data = {
                    "url":url,
                    "name":name_utf8,
                    "topics":topics_utf8,
                    "skills":skills_utf8,
                    "description":description_utf8,
                    "language":language,
                    "outcomes":outcomes_utf8
                }

                print(f'Processing: {url}')

                with open(f'C:/Users/migue/Escritorio/UPM/TFG/course_crawler_scrapy/course_crawler/course_crawler/spiders/course_crawler_data/coursera/{generate_hash(url)}.json', 'w', encoding='UTF8') as f:
                    json.dump(data,f,indent=4)
        else:
            print('Exception: unsupported language.')
