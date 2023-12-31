import os
import json

carpetas = ['spiders/course_crawler_data/coursera','spiders/course_crawler_data/edx','spiders/course_crawler_data/udemy']
archivo_salida = 'spiders/course_crawler_data/all.json'

# Función para combinar archivos JSON
def combinar_archivos_json(carpetas, archivo_salida):
    res = []
    for carpeta in carpetas:
        for root, _, files in os.walk(carpeta):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            data = json.load(f)
                            res.append(data)
                        except json.JSONDecodeError as e:
                            print(f"Error al leer el archivo {file}: {e}")
    
    with open(archivo_salida, 'w') as outfile:
        json.dump(res, outfile, indent=4)
        print(f"Archivos combinados exitosamente en {archivo_salida}")


if __name__ == '__main__':
    combinar_archivos_json(carpetas, archivo_salida)
