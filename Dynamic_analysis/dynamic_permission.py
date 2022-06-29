# dynamic_permission.py

import os

class Dynamic_permission:
    def __init__(self, package_name):
        self.package_name = package_name
        self.out_dict = {
            'declared permissions':[],
            'requested permissions':[],
            'install permissions':[],
            'runtime permissions':[]
        }

    def dump_package_info(self):
        output = os.popen('adb shell dumpsys package ' + self.package_name).read().split('\n')

        for i in range(len(output)):
            if "declared " in output[i]:
                i = i + 1
                while "requested " not in output[i]:
                    self.out_dict['declared permissions'].append(output[i].split(':')[0].replace(' ', '')) 
                    i = i + 1
            if "requested " in output[i]:
                i = i + 1
                while "install " not in output[i]:
                    self.out_dict['requested permissions'].append(output[i].split(':')[0].replace(' ', ''))
                    i = i + 1
            if 'install ' in output[i]:
                i = i + 1
                while "User 0: " not in output[i]:
                    self.out_dict['install permissions'].append(output[i].split(':')[0].replace(' ', '')) 
                    i = i + 1
            if 'runtime ' in output[i]:
                i = i + 1
                while "disabledComponents" not in output[i] and "isSystemUser" not in output[i]:
                    self.out_dict['runtime permissions'].append(output[i].split(':')[0].replace(' ', '')) 
                    i = i + 1
        

def main():
    package_name = 'com.baidu.input_mi'
    dp = Dynamic_permission(package_name)
    dp.dump_package_info()
    print(dp.out_dict)

if __name__ == "__main__":
    main()