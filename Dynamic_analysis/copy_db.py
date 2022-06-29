import shutil
import os

folder = r"Z:\RS"

for (dirpath, dirnames, filenames) in os.walk(folder):
    for filename in filenames:
        if filename.endswith('db') and filename.startswith('lumen'):
            path = os.path.join(dirpath, filename)
            # print(path)
            target_path = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Privacy_Leakage" + path.replace("Z:", "").replace("\\", "_")
            # print(target_path)
            shutil.copyfile(path, target_path)