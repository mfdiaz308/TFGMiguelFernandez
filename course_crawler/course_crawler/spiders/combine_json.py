import json
import os
import time
import pandas as pd

folders = ['spiders/course_crawler_data/coursera','spiders/course_crawler_data/edx','spiders/course_crawler_data/udemy']
all_jsons_file = 'spiders/course_crawler_data/all.json'
all_csv = 'spiders/course_crawler_data/all.csv'

def combine_json(folders, all_jsons_file, all_csv):
    start = time.time()

    res = []
    for folder in folders:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.json'):
                    with open(os.path.join(root, file), 'r') as f:
                        try:
                            data = json.load(f)
                            res.append(data)
                        except json.JSONDecodeError as e:
                            print(f'Error al leer el archivo {file}: {e}')
    
    with open(all_jsons_file, 'w') as outfile:
        json.dump(res, outfile, indent=4)
        
    df = pd.DataFrame(res)
    df.to_csv(all_csv, encoding='utf-8', index=False)

    finish = time.time()

    elapsed_time = finish-start
    print(f'Elapsed time: {elapsed_time}')

if __name__ == '__main__':
    combine_json(folders,all_jsons_file,all_csv)
    print('Json files combined')