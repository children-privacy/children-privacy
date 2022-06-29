from typing import Counter


input_file = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\Round 1\failed_r1.txt"
output_file = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Rating_results\failed" + "_r" + str(1) + ".txt"

list_package = []
list_text = []

with open(input_file, "r", encoding="utf-8") as f:
    counter = 0
    for line in f:
        text = "\t".join(line.split("\t")[1:3])
        # print(text)
        package = line.split("\t")[1]
        # print(package)
        # print(text)
        if package not in list_package:
            counter += 1
            list_package.append(package)
            list_text.append(str(counter) + '\t' + text)
        # break

with open(output_file, "w", encoding="utf-8") as f:
    for line in list_text:
        f.write(line + '\n')
            