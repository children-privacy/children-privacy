# counter.py

import sys
import os

def count_app(top_folder):
    counter = 0
    for (dirpath, dirnames, filenames) in os.walk(top_folder):
        for filename in filenames:
            if filename.endswith('.apk'):
                counter += 1
    return counter

def main():
    top_folder = sys.argv[1]

    print(top_folder, count_app(top_folder))

if __name__ == "__main__":
    main()