# Ingesta de datos de plataformas de enseñanza y publicación en página web  

## Proceso de scrapping mediante _Scrapy_ y creacion de página web mediante _Flask_  

Este proyecto pertenece al Trabajo de Fin de Grado "Automatización de ingesta de datos y publicación en web de datos de educación". El código ha sido clonado en una máquina virtual linux asociada al proyecto AI4Labour en el que, mediante crontab, se ejecutan los scrappers (de Coursera, edX y Udemy) y el recopilador (_combine_json.py_) una vez por semana para tener la información lo más actualizada posible. La página web está disponible en [https://ai4labour.linkeddata.es/miguel/](https://ai4labour.linkeddata.es/miguel/).  

Temas tratados en este trabajo:
- Scrapping de páginas web con _BeautifulSoup_ y _Scrapy_.
- Creación de hash con la librería _hashlib_.
- Tratamiento de caracteres especiales con _unicodedata_.
- Recopilación de datos mediante _json_ y _pandas_.
- Creación de páginas web con _Flask_.
- Análisis de texto para elaborar taxonomía de Bloom.
- Diseño de páginas web con _html_, _css_ y _javascript_.

## Uso
### Antes de empezar
Instalar los módulos especificados en el archivo _requirements.txt_.  

También cabe destacar que en caso de no estar operativo el servidor apache2 de la máquina virtual asociada a [AI4Labour](https://ai4labour.com/) la página web no funcionará.  

### Scrapping
A la hora de ejecutar los scrappers habrá que situarse en la terminal en /course_crawler/course_crawler. Una vez ahí:
1. Para _coursera_scrapper.py_ y _edx_scrapper.py_ se escribirá en la terminal `scrapy crawl name_of_spider`, siendo `name_of_spider` el parámetro `name` asociado a la clase del scrapper que se desea ejecutar. Solo guardará aquellos cursos en Español o Inglés y que tengan descripción.
2. Para _udemy_scrapper.py_ habrá que ejecutar el fichero mediante `py` o `python3` (en caso de duda ejecutar `which python` en la terminal para saber qué comando utilizar) seguido de la dirección relativa del fichero: `python3 spiders/udemy_scrapper.py`.

---  
Al ejecutar los 3 scripts de scrapping se obtienen una serie de ficheros json de cada curso y 2 globales, un json y un csv, en el que se recopilan todos los datos. El fichero _all.json_ es el que se utiliza para realizar consultas desde la página web.  

### Página web
Para inicializar la página web hay 2 opciones:  
- Introducir la URL asignada mediante la creación del servidor en la máquina virtual: [https://ai4labour.linkeddata.es/miguel/](https://ai4labour.linkeddata.es/miguel/).
- Ejecutar _app.py_ e introducir la URL que aparece en la terminal para, una vez realizada una búsqueda, ser redirigido a la URL del servidor apache2. En ese caso, este es la URL que aparece en la terminal:  
![Debugging screen](https://github.com/mfdiaz308/TFGMiguelFernandez/assets/105811825/e9590fdd-fa73-47ca-8e17-e9028b0a379f)    

---  
Al completar una búsqueda se obtiene la siguiente pantalla:  
![search_results](https://github.com/mfdiaz308/TFGMiguelFernandez/assets/105811825/774215dd-e492-4cfb-9c01-6c90ad6e53b9)  

De izquierda a derecha se tiene:  

- Enlace al curso
- Nombre
- Descripción acortada con botón _Ver más_ que muestra la descripción completa en un cuadro de texto.
- Diagrama con la taxonomía de Bloom correspondiente y enlace con explicación detallada ([Taxonomía Bloom](https://www3.gobiernodecanarias.org/medusa/edublog/cprofestenerifesur/2015/12/03/la-taxonomia-de-bloom-una-herramienta-imprescindible-para-ensenar-y-aprender/)).  



## Estructura del código
En primer lugar, los scrappers están contenidos en la carpeta _spiders_, como es costumbre en los proyectos de _Scrapy_, y tienen dentro otra carpeta _course_crawler_data_ en la que se guardan los ficheros json individuales de cada curso. Están separados por página web y nombrados con un hash de su url para evitar duplicados.  
También dentro de _spiders_ está el fichero _combine_json.py_, que al ejecutarse combina todos los ficheros individuales de las 3 carpetas en un fichero _all.json_ y otro _all.csv_.  
Fuera de _spiders_ están el fichero _app.py_, encargado de inicializar la página web, y la carpeta _templates_. Esta contiene los ficheros para cada situación que puede surgir a la hora de realizar búsquedas: página de inicio (_index.html_), página de resultados (_results.html_) y no se han encontrado resultados (_no_results.html_).  

## Posibles mejoras
1. Ofrecer la posibilidad de descargar el archivo json correspondiente al curso desde la página web.
2. Implementar _Scrapy_ para Udemy (tras varios intentos solo se consigue error 403).
3. Usar los demás contenidos scrappeados de los cursos (topics, skills, language y outcomes).  
