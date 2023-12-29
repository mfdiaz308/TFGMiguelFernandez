import hashlib
import json
import unicodedata
import scrapy

# The name of each file is the hash of its url
def generate_hash(url):
   hash_obj = hashlib.sha256(url.encode())
   return hash_obj.hexdigest()

class CourseCrawler(scrapy.Spider):
    name = 'courses_spider'

    def start_requests(self):
        # Sitemaps de cada tipo de curso
        sitemaps_urls = [
            'https://www.coursera.org/sitemap~www~courses.xml', #course
            'https://www.coursera.org/sitemap~www~professional-certificate.xml', #certificate
            'https://www.coursera.org/sitemap~www~onDemandSpecializations.xml', #specialization
            'https://www.coursera.org/sitemap~www~mastertrack.xml', #mastertrack
            'https://www.coursera.org/sitemap~www~guided-projects.xml' #project
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
        # Scrapea solo si el idioma es español o inglés
        language = response.css('p.cds-119.cds-Typography-base.css-80vnnb.cds-121::text').get()
        if 'English' in language.split(' ') or 'Spanish' in language.split(' '):
            name = response.css('title::text').get()

            if name is not None:
                name_utf8 = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()

                url = response.url

                topics = response.css('a.cds-119.cds-113.cds-115.css-mzc3kb.cds-142::text').getall()

                topics_utf8 = []
                for topic in topics:
                    topics_utf8.append(unicodedata.normalize('NFKD', topic).encode('ascii', 'ignore').decode())

                # No se incluye 'skills' porque es para edX y Udemy, no Coursera

                # Se decide no añadir 'type', ya que no se guardan los archivos en carpetas diferentes

                description = response.css('div.rc-TogglableContent.about-section.collapsed ::text').get()
                description_utf8 = unicodedata.normalize('NFKD', description).encode('ascii', 'ignore').decode()

                outcomes = response.css('li.cds-9.css-0.cds-11.cds-grid-item.cds-56.cds-64 ::text').getall()

                outcomes_utf8 = []
                for skill in outcomes:
                    outcomes_utf8.append(unicodedata.normalize('NFKD', skill).encode('ascii', 'ignore').decode())

                data = {
                    "url":url,
                    "name":name_utf8,
                    "topics":topics_utf8,
                    # "skills":"",
                    # "type":"",
                    "description":description_utf8,
                    "language":language.split(' ')[2],
                    "outcomes":outcomes_utf8
                }

                with open(f'C:/Users/migue/Escritorio/UPM/TFG/course_crawler_scrapy/course_crawler/course_crawler/spiders/course_crawler_data/{generate_hash(url)}.json', 'w', encoding='UTF8') as f:
                    json.dump(data,f,indent=4)
        else:
            print('Unsupported language.')
            return
