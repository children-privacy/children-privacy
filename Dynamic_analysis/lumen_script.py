import os
import argparse
import sys
import subprocess
import time
import json
from send_email import send_email

class Dynamic_test:
    def __init__(self, top_folder, output_folder, device):
        self.device = device
        self.lumen = "edu.berkeley.icsi.haystack"
        self.top_folder = top_folder
        self.output_folder = output_folder
        self.dyn_perm_dict = {
            'declared permissions':[],
            'requested permissions':[],
            'install permissions':[],
            'runtime permissions':[]
        }
    
    def lumen_test(self):
        for (dirpath, dirnames, filenames) in os.walk(self.top_folder):
            if dirpath.endswith('APKs'):
                self.dyn_result_folder = os.path.join(self.output_folder, dirpath.split(os.path.sep)[-3])
                if not os.path.exists(self.dyn_result_folder):
                    os.mkdir(self.dyn_result_folder)
                self.dyn_result_folder = os.path.join(self.dyn_result_folder, dirpath.split(os.path.sep)[-2])
                if not os.path.exists(self.dyn_result_folder):
                    os.mkdir(self.dyn_result_folder)

                self.dyn_perm_folder = os.path.join(self.dyn_result_folder, 'dyn_perm')
                if not os.path.exists(self.dyn_perm_folder):
                    os.mkdir(self.dyn_perm_folder)

                self.log = os.path.join(self.dyn_result_folder, 'lumen_log.txt')
                if not os.path.exists(self.log):
                    with open(self.log, 'w+'): pass

                self.counter = 0

                for filename in filenames:
                    if filename.endswith('.apk'):
                        self.load_apk(dirpath, filename)

                        if not self.is_tested():
                            self.is_app_running(self.lumen)
                            print('# ' + str(self.counter) + ' ' + self.package_name + ' starts testing ...\n')
                            print('Location: ' + dirpath) 

                            self.check_network()
                            self.install_apk()
                            self.test_apk()
                            self.dump_permission_info()
                            self.uninstall_apk()
                            self.write_to_log()
                            self.pull_data(20)
                print('End of test.')
                # send_email('Testing ends.')
                self.pull_data(1)

    def load_apk(self, dirpath, filename):
        self.apk_path = os.path.join(dirpath, filename)
        self.package_name = os.path.splitext(filename)[0]
        self.counter += 1
    
    def is_tested(self):
        with open(self.log, "r+") as log_f:
            if self.package_name in log_f.read():
                print('# ' + str(self.counter) + ' ' + self.package_name + ' has been tested.')
                return True
        return False

    def is_app_running(self, package_name):
        cmd = "adb -s " + self.device + " shell pidof " + package_name
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            print('Lumen is not running. Stop testing.')
            send_email('Lumen is not running. Stop testing.')
            sys.exit(0) 
        
    def check_output(self, output, str):
        if str in output:
            send_email(output)
            sys.exit(0)
    
    def install_apk(self):
        cmd = 'adb -s ' + self.device + ' install "' + self.apk_path + '"'
        # self.check_output(subprocess.check_output(cmd, shell=True), 'denied')
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            send_email('apk install failed.')
        time.sleep(5)
    
    def test_apk(self):
        cmd = 'adb -s ' + self.device + ' shell monkey -p ' + self.package_name + ' -c android.intent.category.LAUNCHER 1'
        subprocess.check_output(cmd, shell=True)
        # os.system('adb -s ' + self.device + ' shell monkey -p ' + self.package_name + ' -c android.intent.category.LAUNCHER 1')
        time.sleep(60)
        cmd = 'adb -s ' + self.device + ' shell am force-stop ' + self.package_name
        subprocess.check_output(cmd, shell=True)
        # os.system('adb -s ' + self.device + ' shell am force-stop ' + self.package_name)
        time.sleep(2)

    def dump_permission_info(self):
        perm_info = os.popen('adb -s ' + self.device + ' shell dumpsys package ' + self.package_name).read().split('\n')
        
        dyn_perm_dict = {
            'declared permissions':[],
            'requested permissions':[],
            'install permissions':[],
            'runtime permissions':[]
        }

        flag = ''
        for line in perm_info:
            if 'requested permissions' in line:
                flag = 'requested permissions'
            elif 'declared permissions' in line:
                flag = 'declared permissions'
            elif 'install permissions' in line:
                flag = 'install permissions'
            elif 'runtime permissions' in line:
                flag = 'runtime permissions'
            elif 'enabledComponents' in line or 'disabledComponents' in line or 'isSystemUser' in line or 'User 0' in line or 'overlay paths' in line:
                flag = ''
            elif flag != '':
                dyn_perm_dict[flag].append(line.replace(' ', '')) 

        with open(os.path.join(self.dyn_perm_folder, 'dyn_perm_' + self.package_name + '.json'), 'w+') as f_json:
            json.dump(dyn_perm_dict, f_json)
        time.sleep(20)

    def uninstall_apk(self):
        try:
            os.system('adb -s ' + self.device + ' uninstall "' + self.package_name + '"')
        except:
            send_email('uninstall failed.')
        time.sleep(2)

    def write_to_log(self):
        with open(self.log, "a+") as log_f:
            log_f.write(self.package_name + '\n')
    
    def pull_data(self, interval):
        if self.counter % interval == 0:
            out_db_path = os.path.join(self.dyn_result_folder, "lumen_" + str(self.counter) + '.db')
            try:
                # cmd = 'adb -s ' + self.device + ' pull /data/data/edu.berkeley.icsi.haystack/databases/haystack.db ' + out_db_path
                # subprocess.check_output(cmd, shell=True)
                # cmd = 'adb -s ' + self.device + ' shell rm -f /data/data/edu.berkeley.icsi.haystack/databases/haystack.db'
                # subprocess.check_output(cmd, shell=True)
                os.system('adb -s ' + self.device + ' pull /data/data/edu.berkeley.icsi.haystack/databases/haystack.db ' + out_db_path)
                os.system('adb -s ' + self.device + ' shell rm -f /data/data/edu.berkeley.icsi.haystack/databases/haystack.db')
            except:
                send_email('Pull data failed.')
                sys.exit()
            # os.system('adb -s ' + self.device + ' pull /data/data/edu.berkeley.icsi.haystack/databases/haystack.db ' + out_db_path)
            # os.system('adb -s ' + self.device + ' shell rm -f /data/data/edu.berkeley.icsi.haystack/databases/haystack.db')

    def check_network(self):
        print('checking network...')
        cmd = "adb -s " + self.device + " shell ip tuntap"

        if bool(subprocess.check_output(cmd, shell=True)) is False:
            print('VPN is not running. Stop testing.')
            send_email('VPN is not running. Stop testing.')
            sys.exit(0)  

def main():
    
    device = sys.argv[1]
    apk_folder = sys.argv[2]
    output_folder = r"C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Privacy_Leakage\Raw"

    dt = Dynamic_test(apk_folder, output_folder, device)

    dt.lumen_test()

if __name__ == "__main__":
    main()
