# dyn_privacy_analysis.py

# Dyn_data_analysis.py

import os
import sys


class Dyn_privacy_analysis:
    sp = '||'
    privacy = []
    def __init__(self, input_folder, output_folder, category, top):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.category = category
        self.top = top
    
    def summarize_list_by_columns(self, arr):
        '''
        Summarize the self.privacy list according to the arr array
        Input: arr, the array. For example, [2,3] means summarizing the item[2] and item[3]
        Return: a sorted dict. 
        '''
        dict = {}
        for tuple in self.privacy:
            tuple = tuple.split(self.sp)
            if len(tuple) != 5:
                continue
            item = self.sp.join(tuple[i] for i in arr)
            if item in dict.keys():
                dict.update({item:dict[item]+1})
            else:
                dict[item] = 1
        return sorted(dict.items(), key=lambda i: i[1])[-self.top:]

    def summarize_list_by_item(self, item):
        list = []
        for tuple in self.privacy:
            if item in tuple:
                list.append(tuple)
        return list
    
    def summarize_lists(self, arr):
        list = []
        for a in arr:
            list += self.summarize_list_by_columns(a)
            list += '\n'
        return list
    
    def summarize_privacy(self):
        '''
        Summarize the self.privacy list to .txt file.
        Output: [output_floder]/lumen_privacy_[category]_[top].txt, including the lists of 
        top apps, top pii types, tope destinations, and top pii vs destination
        '''
        # 0 = package name, 2 = pii type, 3 = destination
        arr = [[0], [2], [3], [2,3]]
        list = self.summarize_lists(arr)

        output_path = os.path.join(self.output_folder, r'lumen_privacy_' + self.category + '_' + str(self.top) + '.txt')
        self.write_to_file(self.join_with_sp(list), output_path)

    def search(self, keyword):
        res = self.summarize_list_by_item(keyword)
        output_path = os.path.join(self.output_folder, r'search_' + self.category + '_' + keyword + '.txt')
        self.write_to_file(res, output_path)
    
    def load_txt(self, path):
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
                if package in apk_list:
                    self.privacy.append(tuple)

    def join_with_sp(self, list):
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
                        out_f.write(line + '\n')

    def analyze_privacy(self):
        '''
        Analyze the privacy result. 
        Loop in the folder and load all lumen_privacy_*txt files into self.privacy by calling self.load_txt()
        Summarize self.privacy by calling self.summariz_lists()
        '''
        for (dirpath, dirnames, filenames) in os.walk(self.input_folder):
            for filename in filenames:
                if filename.endswith('txt') and filename.startswith('lumen_privacy_' + self.category):
                    print('Summarizing', os.path.join(dirpath, filename))
                    self.load_txt(os.path.join(dirpath, filename))
        self.summarize_privacy()

def main():
    input_folder = sys.argv[1]
    output_folder = r'C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Try'
    category = sys.argv[2]
    top = 50
    
    Dyn_privacy_analysis(input_folder, output_folder, category, top).analyze_privacy()

if __name__ == "__main__":
    main()