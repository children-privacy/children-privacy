# random_select.py

import random

def shuffle_lines(input, output):
    file = open(input, "r", encoding="utf8") 
    all = [] 
    for lines in file: 
        all.append(lines.strip()) 
    random.shuffle(all) 

    out = open(output, "w+", encoding="utf8")
    for line in all:
        out.write(line + '\n')

def main():
    file = "C:\Age_Rating\App_downloader\Family_apk\App_info_summary\\app_info_summary.txt"
    output = "C:\Age_Rating\App_downloader\Family_apk\\assignment_list.txt"

    shuffle_lines(file, output)