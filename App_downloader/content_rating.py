import argparse
import json
import os
import subprocess
import time
import sys

class ContentRating:
    def __init__(self,app_list,output_path,raw_path=None) -> None:
        self.app_list = app_list
        self.output_path = output_path
        if raw_path:
            self.raw_path = raw_path

    def get_app_list(self) -> None:
        self.apps = []
        with open(self.app_list, "r", encoding="utf-8") as app_list_f:
            for line in app_list_f:
                # package_name = line.split('\t')[1].replace('.apk','')
                # print(line.split('\t'))
                package_name = line.split('\t')[1]
                storage_folder = line.split('\t')[2].replace('\n','')
                self.apps.append([package_name,storage_folder])

    def get_ratings(self, app) -> list:
        cmd = 'node scraper_app_content_rating.js ' + app
        output = subprocess.check_output(cmd, shell=True)
        return output.decode("utf-8").replace('\n','').split(',')

    def load_raw_data(self) -> list:
        self.raw = []
        with open(self.raw_path, 'r', encoding='utf-8') as raw_f:
            for line in raw_f:
                items = line.split('\t')
                package_name = items[1]
                storage_folder = items[2].replace('\n','')
                ratings = items[3].replace('\n','').split(', ')
                self.raw.append([package_name,storage_folder,ratings])

    def convert_to_number(self,ratings):
        num_ratings = []
        for rating in ratings:
            if rating:
                num_ratings.append(self.rating_items.index(rating))
        return num_ratings

    def inconsistent(self, ratings):
        text = []
        for i in ratings:
            for j in ratings:
                if self.rating_matrix[i][j] > 0:
                    text.append(str(i) + ' ' + str(j) + ' ' + str(self.rating_matrix[i][j]))
        return text

    def write_to_txt(self, content, output_path):
        with open(output_path, "a+", encoding="utf-8") as output_f:
            output_f.write(content)
            output_f.write('\n')

    def run_local(self):
        detected = []
        counter_detected = 0
        counter_tested = 0

        self.load_raw_data()
        for data in self.raw:
            counter_tested += 1
            num_rating = self.convert_to_number(data[2])
            text = self.inconsistent(num_rating)
            if len(text):
                counter_detected += 1
                detected.append(str(counter_detected) + '\t' + data[0] + '\t' + ', '.join(data[2]) + '\t' + ', '.join(text))
        self.write_to_txt('\n'.join(detected), os.path.join(self.output_path,'detected_local.txt'))

    def analyse(self):
        result = []
        counter_levels = [0,0,0,0]
        detected = []
        with open(os.path.join(self.output_path,'detected_local.txt'), 'r', encoding='utf-8') as result_f:
            for line in result_f:
                items = line.split('\t')
                package_name = items[1]
                inconsistences = items[3].replace('\n','').split(', ')
                levels = [0,0,0,0]
                for s in inconsistences:
                    n = int(s.split(' ')[2])
                    if n == 4:
                        detected.append(line)
                    levels[n-1] = 1
                counter_levels = [sum(x) for x in zip(counter_levels, levels)]
                result.append([package_name, inconsistences])
                
                # print(result)
        print(counter_levels)
        self.write_to_txt('\n'.join(detected), os.path.join(self.output_path,'detected_local_level4.txt'))


    def run(self, start=0, detected=0, success=0):
        self.get_app_list()
        counter = start
        counter_detect = detected
        counter_success = success

        ratings = []
        detected = []
        num_rating = []

        for app in self.apps[start:]:
            # app[0] = "com.aamalemuktasar"
            num_rating = []
            counter += 1
            try:
                rating = self.get_ratings(app[0])
                if len(rating) == 5:
                    # print("len != 1", str((rating[0])))
                    counter_success += 1
                    ratings.append(str(counter_success) + '\t' + '\t'.join(app) + '\t' + ', '.join(rating))
                    num_rating = self.convert_to_number(rating)
                else:
                    # print('failed: ', '\t'.join(app), ', '.join(rating))
                    self.write_to_txt(str(counter - counter_success) + '\t' + '\t'.join(app) + '\t' + ', '.join(rating), os.path.join(self.output_path,'failed.txt'))
                    # sys.exit()
            except:
                print(app)
                print(counter)
                # if len(ratings) != 0:
                #     self.write_to_txt('\n'.join(ratings), os.path.join(self.output_path,'raw_ratings_' + str(counter) + '.txt'))
                # if len(detected) != 0:
                #     self.write_to_txt('\n'.join(detected), os.path.join(self.output_path,'detected.txt'))
                sys.exit()
            
            text = self.inconsistent(num_rating)
            if len(text):
                counter_detect += 1
                print('Detect: ', str(counter_detect),' '.join(app), ', '.join(rating),str(counter_detect) + '/' + str(counter_success), str(counter_detect/counter_success))
                detected.append(str(counter_detect) +'/' + str(counter_success) + '\t' + '\t'.join(app) + '\t' + ', '.join(rating) + '\t' + ', '.join(text)) 
            
            if counter_success % 50 == 0 and counter_success != 0 and len(detected) != 0:
                self.write_to_txt('\n'.join(ratings), os.path.join(self.output_path,'raw_ratings_' + str(counter) + '.txt'))
                self.write_to_txt('\n'.join(detected), os.path.join(self.output_path,'detected.txt'))
                ratings = []
                detected = []   
            
            time.sleep(10)
    
    # rating_matrix = [
    #     [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2],
    #     [0,0,0,1,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2],
    #     [0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    #     [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,2,2,2,0,1,2,2,2,0,0,0,2,2,2,0,0,2,2,2,0,1,2,2,2],
    #     [0,0,1,2,2,0,0,1,2,2,0,0,0,1,2,2,0,0,1,2,2,0,0,1,2,2],
    #     [0,0,0,1,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2],
    #     [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,2,2,2,0,2,2,2,2,0,0,1,2,2,2,0,1,2,2,2,0,1,2,2,2],
    #     [0,0,2,2,2,0,2,2,2,2,0,0,1,2,2,2,0,1,2,2,2,0,1,2,2,2],
    #     [0,0,2,2,2,0,0,1,2,2,0,0,0,1,2,2,0,0,1,2,2,0,0,1,2,2],
    #     [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2],
    #     [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,2,2,2,0,2,2,2,2,0,0,1,2,2,2,0,1,2,2,2,0,1,2,2,2],
    #     [0,0,2,2,2,0,0,1,2,2,0,0,0,1,2,2,0,0,1,2,2,0,0,1,2,2],
    #     [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2],
    #     [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    #     [0,0,2,2,2,0,2,2,2,2,0,0,1,2,2,2,0,1,2,2,2,0,1,2,2,2],
    #     [0,0,2,2,2,0,0,1,2,2,0,0,0,1,2,2,0,0,1,2,2,0,0,1,2,2],
    #     [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2],
    #     [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
    #     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # ]

    rating_matrix = [
        [0,0,1,2,3,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2], 
        [0,0,0,1,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2], 
        [0,0,0,0,2,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], 
        [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0], 
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
        [0,0,2,3,4,0,1,2,3,4,0,0,0,2,3,4,0,0,2,3,4,0,1,2,3,4], 
        [0,0,1,2,3,0,0,1,2,3,0,0,0,1,2,3,0,0,1,2,3,0,0,1,2,3], 
        [0,0,0,1,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2], 
        [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], 
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
        [0,0,2,3,4,0,2,3,4,4,0,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4], 
        [0,0,2,3,4,0,2,2,3,4,0,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4], 
        [0,0,2,3,4,0,0,1,2,3,0,0,0,1,2,3,0,0,1,2,3,0,0,1,2,3], 
        [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2], 
        [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], 
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
        [0,0,2,3,4,0,2,3,4,4,0,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4], 
        [0,0,2,3,4,0,0,1,2,3,0,0,0,1,2,3,0,0,1,2,3,0,0,1,2,3], 
        [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2], 
        [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], 
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
        [0,0,2,3,4,0,2,3,4,4,0,0,1,2,3,4,0,1,2,3,4,0,1,2,3,4], 
        [0,0,2,3,4,0,0,1,2,3,0,0,0,1,2,3,0,0,1,2,3,0,0,1,2,3], 
        [0,0,1,2,2,0,0,0,1,2,0,0,0,0,1,2,0,0,0,1,2,0,0,0,1,2], 
        [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1], 
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    
    rating_items = [
        'General', "Parental Guidance", "Mature", 'Restricted to 15+', 'Restricted to 18+', #ACB - AU Games
        'Everyone', 'Everyone 10+', 'Teen', 'Mature 17+', 'Adults only 18+', #ESRB - US
        'PEGI 3', 'Parental guidance', 'PEGI 7', 'PEGI 12', 'PEGI 16', 'PEGI 18', #PEGI - EU
        'USK: All ages', 'USK: Ages 6+', 'USK: Ages 12+', 'USK: Ages 16+', 'USK: Ages 18+', #USK - DE
        'Rated for 3+', 'Rated for 7+', 'Rated for 12+', 'Rated for 16+', 'Rated for 18+', #IARC - other countries    
    ]

def main():
    # time.sleep(1000)

    app_list = r"C:\Age_Rating\Apk\Apk_list\apk_list.txt"
    # app_list = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\failed_r9.txt"
    output_path = r"C:\Age_Rating"

    raw_path = r'G:\My Drive\_Research\_Age_Rating\Results\Rating_results\raw.txt'

    # ContentRating(app_list, output_path).run(0,3041,13700)
    ContentRating(app_list, output_path).run(0,0,0)
    # ContentRating(app_list, output_path, raw_path).run_local()
    # ContentRating(app_list, output_path, raw_path).analyse()
    # print(ContentRating(app_list,output_path).rating_matrix[2][11])
if __name__ == "__main__":
    main()


