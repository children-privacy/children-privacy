# virus_total.py

import json
import os
import time
# import gevent.monkey
# gevent.monkey.patch_all()
import requests
import hashlib
import sys

class VT:
    api_key = '42d507135665c4e7b479d7c96db2b769030d9e4f8f7f83195ede0b3f1d060686'
    # api_key = '743601a0304c2c835a56430f03aec0217b7a3e1eb7ddd00363c0d31522325052' #Jason
    sp = '||'
    
    def __init__(self, top_folder):
        self.top_folder = top_folder

    def get_report_all(self):
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            if dirpath.split(os.path.sep)[-1] == "APKs":
                for filename in filenames:
                    print('Check apk: ', dirpath.split(os.path.sep)[-2], filename)
                    json_path = os.path.join(os.path.dirname(dirpath), 'VT_results' + os.path.sep + filename + '.json')
                    if not os.path.exists(json_path):
                        if os.stat(os.path.join(dirpath, filename)).st_size >= 32000000:
                            print('Too large file size!')
                        else:
                            result = self.get_report(os.path.join(dirpath, filename))
                            if result is not None:
                                print('Existed, get result from VT')
                                self.write_to_json(result, json_path)
                            time.sleep(20)
                    else:
                        print('Already tested.')
    
    def get_report(self, apk_path):
        with open(apk_path, 'rb') as f:
            sha = hashlib.sha256(f.read()).hexdigest()
            y = requests.get("https://www.virustotal.com/vtapi/v2/file/report", params={'resource': sha, 'apikey': self.api_key})
            if y.status_code != 200:
                print('Not 200!', y)
                sys.exit()
            response = json.loads(y.text)
            if response['response_code'] != 1:
                print('Not existed, start uploading ...')
                self.upload_file(apk_path)
                return          
            return response

    def upload_file(self, apk_path):
        with open(apk_path, 'rb') as f:
            requests.post("https://www.virustotal.com/vtapi/v2/file/scan", files={'file': f, 'apikey':self.api_key})
            print('Uploaded: ', apk_path.split(os.path.sep)[-1])

    def write_to_json(self, content, json_path):
        if not os.path.exists(os.path.dirname(json_path)):
            os.mkdir(os.path.dirname(json_path))

        with open(json_path, "w+", encoding="utf8") as f_json:
            json.dump(content, f_json)

# def remove_duplicate(json_path):
#     with open(json_path, 'rb') as f:
#         hash = hashlib.sha256(f.read()).hexdigest()
#     basename = os.path.basename(json_path)
#     for (dirpath, dirnames, filenames) in os.walk(os.path.dirname(json_path)):
#         for filename in filenames:
#             if filename.split('_')[0] == basename.split('_')[0] and filename != basename:
#                 with open(os.path.join(dirpath, filename), 'rb') as f:
#                     if hashlib.sha256(f.read()).hexdigest() == hash:
#                         os.remove(json_path)
#                         print('duplicate removed')


                # remove_duplicate(json_path)

    def collect_result(self):
        txt_path = os.path.join(self.top_folder, 'vt_results.txt')
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            if dirpath.split(os.path.sep)[-1] == "VT_results":
                for filename in filenames:
                    with open(os.path.join(dirpath, filename)) as json_f:
                        result = json.load(json_f)
                        if result['positives'] != 0:
                            # print(result['positives'], '\t', dirpath.split(os.path.sep)[-2], '\t', filename)
                            self.write_to_txt(str(result['positives']) + self.sp + dirpath.split(os.path.sep)[-2] + self.sp + filename + '\n', txt_path)
                            # for key in result['scans'].keys():
                            #     if result['scans'][key]['detected'] == True:
                                    # print(key, '\t', result['scans'][key]['result'])
                                    # write_to_txt(key + sp + result['scans'][key]['result'] + '\n')
                            # print("\n")
                            # print(result['scans'].keys())

    def write_to_txt(self, content, txt_path):
        with open(txt_path, "a+") as txt_f:
            txt_f.write(content)

def main():
    top_folder = sys.argv[1]
    vt = VT(top_folder)
    vt.get_report_all()
    vt.collect_result()
    
if __name__ == "__main__":
    main()