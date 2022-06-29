# op_app_list.py

import os
import json

# top_folder = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\NLP_results\Comments"
top_folder = r"G:\My Drive\_Research\_Age_Rating\Results\NLP_results\Comments"
app_list_json = r"G:\My Drive\_Research\_Age_Rating\app_list.json"
# search_json = r"C:\Users\User\My_Drive\_Research\_Age_Rating\app_search.json"

# Mac
# top_folder = r"/Volumes/GoogleDrive/My Drive/_Research/_Age_Rating/Results/NLP_results/Comments"
# app_list_json = r"/Volumes/GoogleDrive/My Drive/_Research/_Age_Rating/app_list.json"
# search_json = r""

def gen_app_list():
    app_list = {}
    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames:
            if filename.startswith('list_') and filename.endswith('json'):
                with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as f:
                    apps = json.load(f)
                    for app in apps:
                        try:
                            package_name = app['appId']
                            if package_name not in app_list.keys() or app["maxInstalls"] > app_list[package_name]["maxInstalls"]:
                                category = 'Family' if 'Family_' in dirpath else app['genreId']
                                app_list[package_name] = {
                                    "maxInstalls": app["maxInstalls"],
                                    "score": app["score"],
                                    "reviews": app["reviews"],
                                    "contentRating": app["contentRating"],
                                    "category": category
                                }
                        except:
                            print(package_name, filename)

    with open(app_list_json, 'w', encoding='utf-8') as f:
        json.dump(app_list, f)
                            
def search_app_list():
    with open(app_list_json, 'r', encoding='utf-8') as f:
        app_list = json.load(f)
        
    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames:
            if filename.startswith('summary_') and filename.endswith('txt'):
                text = 'Apk||maxInstalls||score||reviews||contentRating||Category\n'
                with open(os.path.join(dirpath, filename), 'r', encoding='utf-8') as f:
                    for line in f:
                        # print(line)
                        package_name = line.split('||')[0]
                        if package_name in app_list.keys():
                            # print(app_list[package_name]['maxInstalls'])
                            text += package_name + '||' + '||'.join(str(x) for x in app_list[package_name].values()) + '\n'
                            # text += package_name + '||' + app_list[package_name]['maxInstalls'] + '||' + app_list[package_name]['score'] + '||' + app_list[package_name]['reviews'] + '||' + app_list[package_name]['contentRating'] + '\n'
                with open(os.path.join(dirpath, filename.replace('summary_', 'search_')), 'w', encoding='utf-8') as out:
                    out.write(text)  

# def search_app_list(package_name):
#     with open(app_list_json, 'r', encoding='utf-8') as f:
#         app_list = json.load(f)
    
#     if package_name in app_list.keys():
#         return app_list[package_name].values()
#     else:
#         return None

# gen_app_list()
search_app_list()