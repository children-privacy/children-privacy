import os
import json

top_folder = r"G:\My Drive\_Research\_Age_Rating\Results\NLP_results\Comments"
app_list_json = r"G:\My Drive\_Research\_Age_Rating\app_list.json"

def syn_data():
    

    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames:
            if filename.startswith('summary_') and filename.endswith('txt'):
                with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as f:
                    for line in f:
                        dict = {}
                        items = line.replace('\n', '').split('||')
                        package_name = items[0]
                        detected = items[1:19]
                        dict['package_name'] = package_name
                        dict['results'] = detected