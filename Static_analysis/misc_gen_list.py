# misc_gen_list.py

import json
import xml.etree.ElementTree as et

# https://reports.exodus-privacy.eu.org/en/trackers/ exodus
# https://whotracks.me/trackers.html whotracksme


def gen_perm_list():
    tree = et.parse('AndroidManifest11.xml')
    root = tree.getroot()
    permissions = {}

    for child in root:
        if child.tag == 'permission':
            name = child.attrib['{http://schemas.android.com/apk/res/android}name'].split('.')[-1]
            level = child.attrib['{http://schemas.android.com/apk/res/android}protectionLevel'].split('|')[0]

            permissions[name] = level
    
    with open('permission.json', 'w') as file:
        json.dump(permissions, file)

def gen_tracker_list():
    trackers = []

    allowed = ['adcolony', 'applovin', 'chartboost', 'google ad manager',
        'google admob', 'admob', 'inmobi', 'ironsource', 'kidoz', 'superawesome',
        'unity3d ads', 'vungle']
    
    with open('trackers_exodus.json', "r") as tracker_f:
        for item in json.load(tracker_f)['trackers']: 
            tracker = {}
            tracker['name'] = item['name']
            if tracker['name'].lower() in allowed or 'google' in tracker['name'].lower():
                tracker['allowed'] = True
                print(tracker['name'])
            else:
                tracker['allowed'] = False

            tracker['code_signature'] = item['code_signature'].replace('.', '/')
            
            if item['network_signature'] == '':
                web = item['website']
                web = web.replace('https://', '')
                web = web.replace('http://', '')
                web = web.replace('www.', '')
                web = web[:-1]
                tracker['network_signature'] = web
            else:
                tracker['network_signature'] = item['network_signature'].replace('\\', '')
            
            trackers.append(tracker)    

    with open('tracker_lumen.json', "r") as tracker_f:
        for item in json.load(tracker_f):
            tracker = {}
            tracker['name'] = item['name']
            if tracker['name'].lower() in allowed or 'google' in tracker['name'].lower():
                tracker['allowed'] = True
                print(tracker['name'])
            else:
                tracker['allowed'] = False
            tracker['code_signature'] = ""
            tracker['network_signature'] = item['network_signature']
            trackers.append(tracker) 

    json_path = r'C:\Age_Rating\Static_analysis\tracker_list.json'
    with open(json_path, "w+", encoding="utf8") as f_json:
        json.dump(trackers, f_json)

    # with open(json_path, "r", encoding="utf8") as f_trackers:
    #     trackers_json = json.load(f_trackers)
    #     for tr in trackers_json:
    #         if "adpop" in tr['signature']:
    #             print('yes')
    #             print(tr)
    #             break


def main():
    gen_perm_list()
    # gen_tracker_list()

if __name__ == "__main__":
    main()