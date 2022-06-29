# Dyn_data_analysis.py

import os
import sys


class Dyn_data_analysis:
    sp = '||'
    list = []

    def __init__(self, input_folder, output_folder, category, mode, top):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.category = category
        self.top = top
        self.mode = mode
        self.header = self.setting[self.mode]['header'] + self.category
        self.load_files(self.header, 'txt')
    
    def aggregate_list_by_columns(self, arr, length) -> dict:
        '''
        Summarize the self.list according to the arr array
        Input: arr, the array. For example, [2,3] means summarizing the item[2] and item[3]
        Return: a dict sorted by numbers. 
        '''
        dict = {}
        for tuple in self.list:
            tuple = tuple.split(self.sp)
            if len(tuple) != length:
                continue
            item = self.sp.join(tuple[i] for i in arr)
            if item in dict.keys():
                dict.update({item:dict[item]+1})
            else:
                dict[item] = 1
        return sorted(dict.items(), key=lambda i: i[1])

    def search_list_by_item(self, item) -> list:
        list = []
        for tuple in self.list:
            if item in tuple:
                list.append(tuple)
        return list
    
    def summarize_lists(self, arr, length) -> list:
        list = []
        for a in arr:
            list += self.aggregate_list_by_columns(a, length)[-self.top:]
            list += '\n'
        return list

    def search(self, keyword):
        res = self.search_list_by_item(keyword)
        output_path = os.path.join(self.output_folder, r'search_' + self.category + '_' + keyword.replace(":","_").replace('.','_').replace(' ','_') + '.txt')
        print(output_path)
        self.write_to_file(res, output_path)
    
    def search_keywords(self, keywords):
        for keyword in keywords:
            self.search(keyword)
    
    def load_file(self, path):
        list = []
        with open(path, "r", encoding="utf8") as f:
            for line in f:
                if line not in list:
                    list.append(line)
        
        # check whether the app is in the apk_list
        with open(r"C:\Age_Rating\Apk\Apk_list\apk_list.txt", 'r') as apk_list:
            apk_list = apk_list.read()
            for tuple in list:
                package = tuple.split(self.sp)[0]
                if self.category == 'Family':
                    package = package + '.apk	FAMILY'
                if package in apk_list and tuple not in self.list:
                    self.list.append(tuple)

    def load_files(self, header, exp):
        for (dirpath, dirnames, filenames) in os.walk(self.input_folder):
            for filename in filenames:
                if filename.endswith(exp) and filename.startswith(header):
                    print('Loading', os.path.join(dirpath, filename))
                    self.load_file(os.path.join(dirpath, filename))

    def join_with_sp(self, list) -> list:
        new_list = []
        for tuple in list:
            tuple = [str(x) for x in tuple]
            string = self.sp.join(tuple)
            new_list.append(string)
        return new_list

    def write_to_file(self, list, file):
        if os.path.exists(file):
            os.remove(file)
        for line in list:
            with open(file, "a+", encoding='utf8') as out_f:
                if not line.endswith('\n'):
                    line += '\n'
                out_f.write(line)

    def analyze_flow(self):
        '''
        Summarize the flow result in self.list to .txt file.
        Output: [output_floder]/lumen_flow_[category]_[top].txt, including the lists of 
        
        '''
        pass

    def analyze(self):
        '''
        Analyze the privacy result. 
        Loop in the folder and load all lumen_privacy_*txt files into self.list by calling self.load_txt()
        Summarize self.list by calling self.summariz_lists()

        mode: "privacy" - ; "flow" - ; "permission" - .

        Output: [output_floder]/lumen_privacy_[category]_[top].txt, including the lists of 
        top apps, top pii types, tope destinations, and top pii vs destination
        '''
        
        arr = self.setting[self.mode]['arr']
        length = self.setting[self.mode]['length']
        # header = self.mode[self.mode]['header'] + self.category

        # self.load_files(header, 'txt')

        output_path = os.path.join(self.output_folder, self.header + '_' + str(self.top) + '.txt')

        list = self.summarize_lists(arr, length)

        self.write_to_file(self.join_with_sp(list), output_path)

    setting = {
        # 0 = package name, 1 = app name, 2 = pii type, 3 = destination, 4 = pii value
        'privacy':{
            'arr':[[0], [2], [3], [2,3]], 
            'length':5, 
            'header':'lumen_privacy_'
        },
        'stat':{
            'arr':[[2,3]],
            'length':5, 
            'header':'lumen_privacy_'
        },
        # 0 = package name, 1 = app name, 2 = destination
        'flow': {'arr':[[0,1,2]], 'length':3, 'header':'lumen_flow_'}
    }




def main():
    input_folder = sys.argv[1]
    output_folder = r'C:\Users\User\My_Drive\_Research\_Age_Rating\Results'
    category = sys.argv[2]
    top = 0
    mode = 'stat'
    
    dda = Dyn_data_analysis(input_folder, output_folder, category, mode, top)
    dda.analyze()
    # dda.analyze('flow')

    # keywords = [
        # 'com.FMG.LandOfTheDragon',
        # 'com.mbagames.vegetables',
        # 'com.math.games.multiply.nas',
        # 'com.turborocketgames.wildcraft',
        # 'com.sinyee.babybus.world',
        # 'Keyword:city',
        # 'Keyword:adID',
        # 'persist.sys.timezone',
        # 'Keyword:Location',
        # 'Private IP',
        # 'Android Serial',
        # 'com.learnwithhomer.webapp'
        # ]

    # dda.search_keywords(keywords)

if __name__ == "__main__":
    main()