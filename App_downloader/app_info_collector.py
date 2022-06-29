# app_info_collector.py

import os
import hashlib
from hash_list_checker import is_value_existed
from app_list_cleaner import clean_all_app_list
from app_list_converter import convert_all_app_list

def concatenate_files(path, target_filename, output_path):
    if not os.path.exists(os.path.dirname(output_path)):
        os.mkdir(os.path.dirname(output_path))
    with open(output_path, "w+", encoding="utf8") as f_out:
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if filename == target_filename:
                    with open(dirpath + '\\' + filename, "r", encoding="utf8") as f_in:
                        for line in f_in:
                            f_out.write(line)

def remove_duplicate_content(input_file_path):
    folder = os.path.dirname(input_file_path)
    hash_set = set()                
    with open(input_file_path, "r", encoding="utf8") as input, open(folder + "\\app_info_summary.txt", "w+", encoding="utf8") as output:
        for line in input:
            md5 = hashlib.md5(line.encode("utf8")).hexdigest()
            if md5 not in hash_set:
                output.write(line)
                hash_set.add(md5)
    os.remove(input_file_path)

def main():
    target_filename = "app_info.txt"
    hash_list = "C:\\Age_Rating\\App_downloader\\Downloads\\Hash_list\\hash_list.txt"

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', metavar='TOP_FOLDER_NAME', type=str, required=True, help='The name of the top folder of apk files.') 
    parser.add_argument('-l', metavar='HASH_LIST', type=str, default=hash_list, help='The path to the hash list.')
    parser.add_argument('-o', metavar='OUTPUT', type=str, help='The path of output file.')       
    args = parser.parse_args()

    path = "C:\\Age_Rating\\App_downloader\\" + args.f + "\\"
    hash_list = args.l
    output_raw = path + "App_info_summary\\app_info_summary_raw.txt"

    clean_all_app_list(path, hash_list)
    convert_all_app_list(path)

    concatenate_files(path, target_filename, output_raw)
    remove_duplicate_content(output_raw)

if __name__ == "__main__":
    main() 