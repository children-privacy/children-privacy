import os
from typing import Counter

def load_files(input_folder, header, exp):
    list = []
    for (dirpath, dirnames, filenames) in os.walk(input_folder):
        for filename in filenames:
            if filename.endswith(exp) and filename.startswith(header):
                list.append(os.path.join(dirpath, filename))
    return list

def summarize(f_list):
    list_package = []
    list_text_1 = []
    list_text_2 = []
    counter_1 = 0
    counter_2 = 0
    counter_all = 0

    for file in f_list:
        with open(file, "r", encoding="utf-8") as f:
            print(file)
            for line in f:
                counter_all += 1
                items = line.split("\t")
                package = items[1]
                text = items[1] + '\t' + '_'.join(items[2].split('_')[:-2]) + '\t' + items[3]
                levels = []
                for tuple in items[4].replace('\n','').split(','):
                    levels.append(int(tuple[-1]))
                level = max(levels)

                if package not in list_package:
                    list_package.append(package)
                    if level == 1:
                        counter_1 += 1
                        list_text_1.append(str(counter_1) + '\t' + text)
                    else:
                        counter_2 += 1
                        list_text_2.append(str(counter_2) + '\t' + text)
    
    # print(counter_all)

    return list_text_1, list_text_2

def write_to_file(content, file):
    with open(file, "w+", encoding="utf-8") as f:
        for line in content:
            if not line.endswith('\n'):
                line += '\n'
            f.write(line)

def summarize_raw(f_list):
    list_package = []
    list_text = []
    counter = 0

    for file in f_list:
        print(file)
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                # counter_all += 1
                items = line.split("\t")
                package = items[1]
                text = items[1] + '\t' + '_'.join(items[2].split('_')[:-2]) + '\t' + items[3]

                if package not in list_package:
                    counter += 1
                    list_package.append(package)
                    list_text.append(str(counter) + '\t' + text)
    print(len(list_text))
    return list_text


input_folder = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\Raw"
output_1= r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\summary_1.txt"
output_2 = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\summary_2.txt"

raw_output = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\raw.txt"

# f_list = load_files(input_folder, 'detected', 'txt')
# list_1, list_2 = summarize(f_list)
# write_to_file(list_1, output_1)
# write_to_file(list_2, output_2)

f_list = load_files(input_folder, 'raw_ratings', 'txt')
list = summarize_raw(f_list)
write_to_file(list, raw_output)