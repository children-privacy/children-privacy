# static_analyzer.py

import os
import json
from posixpath import dirname
import sys
import pickle

from androguard.misc import AnalyzeAPK

class StaticAnalyzer:
    dangerous_permissions = []
    signature_permissions = []
    trackers = []
    permissions_without_requiring = []

    def __init__(self, top_folder):
        self.top_folder = top_folder
        self.sp = '||'
        self.apk_folder_name = 'APKs'
        self.init_perm_list(r'C:\Age_Rating\Static_analysis\permission.json')
        self.init_tracker_list(r'C:\Age_Rating\Static_analysis\tracker_list.json')
        self.txt_path = os.path.join(self.top_folder, 'static_results.txt')

    def init_perm_list(self, permission_list_path):  
        with open(os.path.join(os.path.dirname(__file__), permission_list_path),'rb') as file_permission:
            self.permissions = json.load(file_permission)

        permDic = {
            "dangerous": [],
            "normal": [],
            "signature": []
        }

        for perm in self.permissions:
            permDic[self.permissions[perm]].append(perm)

        self.dangerous_permissions = permDic["dangerous"]
        self.signature_permissions = permDic["signature"]
    
    def init_tracker_list(self, tracker_list_path):
        with open(os.path.join(tracker_list_path), 'r') as f_trackers:
            self.trackers = json.load(f_trackers)
            self.tracker_names = []
            for t in self.trackers:
                self.tracker_names.append(t['name'])

    def static_analyze_all(self):
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            if dirpath.split(os.path.sep)[-1] == self.apk_folder_name:
                self.static_analyze(dirpath)


    def static_analyze(self, apk_folder):
        counter = 0
        output_folder = os.path.join(os.path.dirname(apk_folder), "Static_results")
        pickle_folder = os.path.join(output_folder, "pickles")
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        if not os.path.exists(pickle_folder):
            os.mkdir(pickle_folder)

        for (dirpath, dirnames, filenames) in os.walk(apk_folder):
            for filename in filenames: 
                package_name = filename.replace('.apk', '')
                pickle_f = os.path.join(pickle_folder, package_name + '.pkl')
                json_path = os.path.join(output_folder, package_name + '.json')
                
                counter += 1

                if os.path.exists(json_path):
                    print('#' + str(counter) + ': ' + os.path.join(dirpath, filename) + 'already tested.')
                else:
                    print('Analyzing #' + str(counter) + ': ' + os.path.join(dirpath, filename))
                    
                    if os.path.exists(pickle_f):
                        with open(pickle_f, 'rb') as f:
                            pkl_dict = pickle.load(f)
                    else:
                        try:
                            a, df, dx = AnalyzeAPK(os.path.join(dirpath, filename)) 
                        except:
                            continue
                        app_name = a.get_app_name()
                        package_name = a.get_package()
                        permissions = a.get_permissions()
                        dx_classes = []
                        for key in dx.classes.keys():
                            dx_classes.append(key)
                        pkl_dict = {
                            'App name': app_name,
                            'Package name': package_name,
                            'Permissions': permissions,
                            'Classes': dx_classes
                        }
                        
                        with open(pickle_f, "wb") as pkl_f:
                            pickle.dump(pkl_dict, pkl_f)

                    self.analyze_manifest(pkl_dict)
                    self.analyze_tracker(pkl_dict)
                    self.res = {**self.permission_result, **self.tracker_result}

                    with open(json_path, "w+", encoding="utf8") as f_json:
                        json.dump(self.res, f_json)
                    

    def analyze_manifest(self, pkl_dict):   
        permissions = pkl_dict['Permissions']

        permDic = {
            "dangerous": [],
            "normal": [],
            "signature": [],
            "signatureOrSystem": [],
            "others": []  # custom permission
        }

        for perm in permissions:
            perm: str = perm
            if perm.startswith("android.permission"):
                permSuffix = perm[len("android.permission") + 1:]
                if permSuffix in self.permissions:
                    permItem = self.permissions[permSuffix]
                    permDic[permItem].append(permSuffix)
                else:
                    permDic["others"].append(permSuffix)
            else:
                permDic["others"].append(perm)

        self.permission_result = {
            'App name': pkl_dict['App name'],
            'Package name': pkl_dict['Package name'],
            'Dangerous permissions': permDic["dangerous"],
            'Signature and system permissions': permDic["signature"] + permDic["signatureOrSystem"],
            'Normal permissions': permDic["normal"],
            'Custom permissions': permDic["others"]
        }
    
    def analyze_tracker(self, pkl_dict):
        trackers = []
        classes = pkl_dict['Classes']
        
        for item in self.trackers:
            hit = False
            for signature in item['code_signature'].split('|'):
                for c in classes: 
                    if signature != '' and signature in c:
                        hit = True
                        break
            if hit:
                trackers.append(item['name'])
                        
        self.tracker_result = {'Trackers': trackers}
    
    def summarize(self):
        if os.path.exists(self.txt_path):
            os.remove(self.txt_path)
        self.write_header()
        self.write_resutls()
            

    def write_header(self):
        strings = []
        strings.append('Apk Name')
        strings.append(self.sp.join(self.dangerous_permissions))
        strings.append(self.sp.join(self.signature_permissions))
        strings.append(self.sp.join(self.tracker_names))
        with open(self.txt_path, "a+") as txt_f: 
            txt_f.write((self.sp + self.sp).join(strings) + '\n')

    def write_resutls(self):
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            for filename in filenames: 
                if dirpath.split(os.path.sep)[-1] == "Static_results" and os.path.splitext(filename)[-1] == '.json':
                    results = []
                    with open(os.path.join(dirpath, filename), "r") as json_f:
                        static_result = json.load(json_f)
                        results.append(static_result['Package name'])
                        results.append(self.convert_to_zero_one(static_result['Dangerous permissions'], self.dangerous_permissions))
                        results.append(self.convert_to_zero_one(static_result['Signature and system permissions'], self.signature_permissions))
                        tracker_name = []
                        for tracker in self.trackers:
                            tracker_name.append(tracker['name'])
                        results.append(self.convert_to_zero_one(static_result['Trackers'], self.tracker_names))
                        
                        with open(self.txt_path, "a+") as txt_f:
                            txt_f.write((self.sp + self.sp).join(results) + '\n')

    def convert_to_zero_one(self, items, pool):
        out = []
        for item in pool:
            if item in items:
                out.append(str(1))
            else:
                out.append(str(0))
        return self.sp.join(out)

def main():
    top_folder = sys.argv[1]
    sa = StaticAnalyzer(top_folder)
    # print(sa.trackers)
    sa.static_analyze_all()
    sa.summarize()

if __name__ == "__main__":
    main()