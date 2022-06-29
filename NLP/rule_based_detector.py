import json
import os
import re
import sys
# import op_app_list


class RuleBasedDetector:
    '''
    Rule-based Detector

    Input: user comments
    Output: labeled comments that reflect undesired app behaviour in tuple {package_name, rule, comment}

    Usage:
    RuleBasedDetector(top_folder, output_json_path, rule_path,stopwords).run()

    '''
    def __init__(self, top_folder, output, rule, stopwords, app_list_json) -> None:
        self.top_folder = top_folder
        self.rules = json.load(open(rule, "r", encoding="utf8")) 
        # self.stopwords = open(stopwords, "r", encoding="utf8").read().split("\n")
        self.app_list = app_list_json
        self.output = output


    def pre_process(self,comment) -> str:
        return re.sub('[^A-Za-z0-9]+', ' ', comment)

    def variants(self, word) -> list:
        return [word, word+'s', word+'es', word+'ed', word+'d', word+'ing']

    def is_matched(self, comment):
        comment_p  = self.pre_process(comment)
        for rule in self.rules:
            if rule["dist"] == 0:
                for word in rule["word_1"]:
                    for variant in self.variants(word):
                        if variant in comment_p:
                            return rule["item"], rule["index"], rule["category"], comment
            elif rule["dist"] == -1:
                for word_1 in rule["word_1"]:
                    if word_1 in comment_p:
                        for word_2 in rule["word_2"]:
                            if word_2 in comment_p:
                                return rule["item"], rule["index"], rule["category"], comment
            elif rule["dist"] > 0:
                list_1 = []
                list_2 = []

                comment_words = comment_p.split(" ")

                for i,word in enumerate(comment_words):
                    for rule_word in rule["word_1"]:
                        if word in self.variants(rule_word):
                            list_1.append(i)
                    for rule_word in rule["word_2"]:
                        if word in self.variants(rule_word):
                            list_2.append(i)
                
                for i in list_1:
                    for j in list_2:
                        if abs(i-j) <= rule["dist"]:
                            return rule["item"], rule["index"], rule["category"], comment
        return None,None,None,None

    def write_to_json(self, content, output):
        if content:
            with open(output, "w", encoding="utf8") as output_f:
                json.dump(content, output_f)

    def write_to_txt(self, content, output):
        if content:
            with open(output, "w", encoding="utf8") as output_f:
                output_f.write(content)

    def dict_to_txt(self, dict):
        text = 'Apk||' + '||'.join([x['item'] for x in self.rules]) + '\n'
        for key in dict.keys():
            tuple = [str(x) for x in dict[key]]
            text += key + '||' + '||'.join(tuple) + '\n'  
        return text

    def detect(self) -> list:
        counter = 0
        detected = [0,0,0,0]
        results = []

        json_output = os.path.join(self.output, 'detect_comments_' + self.top_folder.split(os.path.sep)[-1])
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            print(dirpath)
            for filename in filenames:
                if filename.startswith('review') and filename.endswith('txt'):
                    package_name = filename.replace('.txt',"").replace('review_',"")
                    with open(os.path.join(dirpath, filename), "r", encoding="utf8") as comment_f:
                        for comment in comment_f:
                            counter += 1
                            rule, index, category, matched_comment = self.is_matched(self.pre_process(comment))
                            if rule:
                                item = {"package_name": package_name, "rule": rule, "rule_index":index, "comment": matched_comment}
                                detected[category] += 1
                                results.append(item)  
        json_output += '_' + str(detected) + '_' + str(counter) + '.json'
        self.write_to_json(results, json_output)
        return results
    
    def detect_per_app(self, package_name):
        results = []
        json_output = os.path.join(self.output, 'detect_comments_' + package_name + '.json')
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            print(dirpath)
            for filename in filenames:
                if filename.startswith('review_' + package_name) and filename.endswith('txt'):
                    # package_name = filename.replace('.txt',"").replace('review_',"")
                    with open(os.path.join(dirpath, filename), "r", encoding="utf8") as comment_f:
                        for comment in comment_f:
                            # counter += 1
                            rule, index, category, matched_comment = self.is_matched(self.pre_process(comment))
                            if rule:
                                item = {"package_name": package_name, "rule": rule, "rule_index":index, "comment": matched_comment}
                                # detected[category] += 1
                                results.append(item)  
        # json_output += '_' + str(detected) + '_' + str(counter) + '.json'
        if results:
            with open(json_output, "a+", encoding="utf8") as output_f:
                json.dump(results, output_f)

        return results
    
    def load_detects(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def summarize(self, results):
        txt_output = os.path.join(self.output, 'summary_comments_' + self.top_folder.split(os.path.sep)[-1] + '.txt')
        record = {}
        search = {}
        text = 'Apk||' + '||'.join([x['item'] for x in self.rules]) + '||maxInstalls||score||reviews||contentRating||Category\n'

        with open(self.app_list, 'r', encoding='utf-8') as f:
            app_list = json.load(f)

        for item in results:
            package_name = item['package_name']
            if package_name not in record.keys():
                record[package_name] = [0] * len(self.rules)
            
                # index = int(item['rule_index'])
            record[package_name][item['rule_index']-1] += 1
        
            if package_name not in search.keys():
                if package_name in app_list.keys():
                    search[package_name] = app_list[package_name].values()

        for key in search.keys():
            text += key + '||' + '||'.join((str(x) for x in record[key])) + '||' + '||'.join((str(x) for x in search[key])) + '\n'
        
        # self.write_to_txt(self.dict_to_txt(record), txt_output)
        with open(txt_output, 'w', encoding='utf-8') as out:
            out.write(text)  

def main():
    top_folders = [
        r"Z:\RS\Family_1",
        r"Z:\RS\Family_2",
        r"Z:\RS\Family_3",
        r"Z:\RS\Family_4",
        r"Z:\RS\Testing_1",
        r"Z:\RS\Testing_2",
        r"Z:\RS\Testing_3",
        r"Z:\RS\Testing_4",
        r"Z:\RS\Testing_5",
        r"Z:\RS\Testing_6",
        r"Z:\RS\Testing_7",
        r"Z:\RS\Testing_8",
        r"Z:\RS\Testing_9", 
        r"Z:\RS\Testing_10"
    ]

    output_json_path = r"G:\My Drive\_Research\_Age_Rating\Results\NLP_results\Comments"
    rule_path = r"G:\My Drive\_Research\_Age_Rating\Code\NLP\rules.json"
    stopwords = r"G:\My Drive\_Research\_Age_Rating\Code\NLP\en_stopwords.txt"
    app_list_json = r"G:\My Drive\_Research\_Age_Rating\app_list.json"

    for folder in top_folders:
        rd = RuleBasedDetector(folder, output_json_path, rule_path, stopwords, app_list_json)
        # rd.summarize(rd.detect())
        rd.detect_per_app('com.miga.myapartment')
        # rd.detect_per_app('com.gi.talkinggummybear')
        # rd.detect_per_app('com.miga.world')
        # rd.detect_per_app('com.tocaboca.tocakitchen')

if __name__ == "__main__":
    main()