# summarize_lumen_result.py

import sqlite3
import os
import sys
sys.path.insert(1, r'C:\Age_Rating\App_downloader')
import misc
import json

class Summarize_lumen_result:
    sp = '||'
    packages = set()

    def __init__(self, folder, output_folder):
        self.folder = folder
        self.output_folder = output_folder
        self.ad_tracker_list = self.init_tracker_list()

    def init_tracker_list(self):
        with open(os.path.join(r'C:\Age_Rating\Static_analysis\tracker_list.json'), 'r') as f_trackers:
            trackers = json.load(f_trackers)
            ad_tracker_list = []
            for t in trackers:
                for suffix in t['network_signature'].split('|'):
                    ad_tracker_list.append(suffix)
        return ad_tracker_list

    def importdb(self, db):
        '''
        Read db file into self.privacy and self.flow lists.
        Output: self.privacy, self.flow
        '''
        conn = None
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            self.privacy = list(c.execute('SELECT app_package, app_name, pii_type, sink_dns_fqdn, pii_value from privacy_table'))
            self.flow = list(c.execute('SELECT app_package, app_name, sink_dns_fqdn from passive_table')) 
        except sqlite3.Error as e:
            print(e)
            # sys.exit(-1)

    def is_value_existed(self, value, file):
        with open(file, "r", encoding="utf8") as f:
            if value in f.read():
                return True

    def to_str_list(self, list):
        new_list = []
        for tuple in list:
            tuple = [str(x) for x in tuple]
            string = self.sp.join(tuple)
            new_list.append(string)
        return new_list

    def extract_ad_tracker(self):
        '''
        Extract ad and trackers from flow.txt files.
        '''
        table_ad_tracker = []
        ad_tracker_dict = {}

        table_ad_tracker.append('Package Name' + self.sp + misc.arr_to_sp_str(self.ad_tracker_list, self.sp))

        with open(os.path.join(self.folder, r'lumen_flow.txt'), 'r', errors='ignore') as flow_f:
            for flow in flow_f:
                flow = flow.split(self.sp)
                package_name = flow[0]
                self.packages.add(package_name)
                
                # print(flow[2].split('.'))
                if len(flow) == 3:
                    suffix = flow[2].split('.')[-2:]
                else:
                    print(flow)

                # print(suffix)
                if len(suffix) == 2:
                    suffix = '.'.join(suffix).split('\n')[0]
                    # print(suffix)
                    if suffix in self.ad_tracker_list:
                        if package_name not in ad_tracker_dict.keys():
                            ad_tracker_dict[package_name] = set()
                        ad_tracker_dict[package_name].add(suffix)

        for key in ad_tracker_dict.keys():
            line = misc.convert_to_zero_one(ad_tracker_dict[key], self.ad_tracker_list)
            line = str(key) + self.sp + misc.arr_to_sp_str(line, self.sp)
            table_ad_tracker.append(line)

        return table_ad_tracker

    # def gen_ad_tracker_table(self):
    #     table_ad_tracker = []
    #     header = self.sp.join(self.ad_tracker_list)
    #     table_ad_tracker.append(header)

    #     with open(os.path.join(self.folder, r'lumen_ad_tracker.txt'), 'r') as f:
    #         for line in f:



    def write_to_file(self, list, file):
        for line in list:
            if not os.path.exists(file):
                with open(file, "w+", encoding='utf8') as out_f:
                    out_f.write(line + '\n')
            else:
                if not self.is_value_existed(line, file):
                    with open(file, "a", encoding='utf8') as out_f:
                        out_f.write(line + '\n')

    def summarize_db(self, db):
        '''
        Import the db file and summarize the results in two txt files under each APK folder.
        Output: [output_floder]/lumen_privacy_[folder].txt, [output_floder]/lumen_flow_[folder].txt
        '''
        self.importdb(db)
        self.write_to_file(self.to_str_list(self.privacy), os.path.join(self.output_folder, r'lumen_privacy_' + self.folder.split(os.path.sep)[-1] + '.txt'))
        self.write_to_file(self.to_str_list(self.flow), os.path.join(self.output_folder, r'lumen_flow_' + self.folder.split(os.path.sep)[-1] + '.txt'))

    def summarize(self):
        '''
        Summarize privacy, flow, and ad tracker data.
        '''
        for (dirpath, dirnames, filenames) in os.walk(self.folder):
            for filename in filenames:
                if filename.endswith('db') and filename.startswith('lumen'):
                    print('Summarizing', os.path.join(dirpath, filename))
                    self.summarize_db(os.path.join(dirpath, filename))
        # self.write_to_file(self.extract_ad_tracker(), os.path.join(self.folder, 'lumen_ad_tracker_' + str(len(self.packages)) + '.txt'))
        # print("# of packages:", len(self.packages))

def main():
    # folder = r'C:\Age_Rating\Apk\Testing'
    folder = sys.argv[1]
    output_folder = r'C:\Users\User\My_Drive\_Research\_Age_Rating\Results'
    
    Summarize_lumen_result(folder, output_folder).summarize()
    # Summarize_lumen_result(folder).gen_ad_tracker_table()

if __name__ == "__main__":
    main()

 # ad_tracker_list = [
    #     '360dialog.com', # '360Dialog'
    #     'adnxs.com', # 'AppNexus'
    #     'adsafeprotected.com', # 'Integral Ad Science'
    #     'atdmt.com',
    #     'casalemedia.com',
    #     'doulbeclick.net',
    #     'googleadservices.com',
    #     'googlesyndication.com',
    #     'crashlytics.com', # 'Google CrashLytics'
    #     'scorecardresearch.com', # 'Score Card Research'
    #     'adobedtm.com',
    #     'branch.io', # 'Branch'
    #     'demdex.net', # 'Demdex'
    #     'appsflyer.com', #'AppsFlyer'
    #     'mobillsutils.azurewebsites.net',
    #     'windows.net',
    #     'ip-api.com',
    #     'xiaomi.net', 'xiaomi.com', # 'Xiaomi Push Service' |42\\.62\\.94\\.2|114\\.54\\.23\\.2|111\\.13\\.142\\.2|111\\.206\\.200\\.2"
    #     'segment.io', 'segment.com', # 'Segment'
    #     'liftoff.io',
    #     'onesignal.com', # 'OneSignal'
    #     'startappservice.com', # 'Startapp'
    #     'unity.com', 'unity3d.com', # 'Unity3d Ads'
    #     'locuslabs.com',
    #     'omtrdc.com', 'omtrdc.net', # 'Omniture'
    #     'urbanairship.com', # 'Urbanairship' 
    #     'accuwether.com',
    #     'amazon-adsystem.com',
    #     'foursquare.com', # 'Pilgrim by Foursquare' 
    #     'mapbox.com', # 'Mapbox' 
    #     'mparticle.com', # 'mParticle'
    #     'rubiconproject.com', # 'Rubicon Project'
    #     'scorecardresearrch.com',
    #     'smartadserver.com', 'adsrvr.org', # 'Smart'
    #     'spotxchange.com',
    #     'stickyadstv.com',
    #     'tremorhub.com',
    #     'cuebiq.com', # 'Cuebiq' 
    #     'doubleverify.com',
    #     'inmobicdn.net', 'inmobi', 'inmobi.us', 'inmobi.info', 'inmobi.cn', 'inmobi.com', # 'Inmobi'
    #     'nr-data.net', 'newrelic.com', # 'New Relic'
    #     'adsmoloco.com',
    #     'mopub.com', # 'Twitter MoPub'
    #     'gvt1.com',
    #     'firebaseio.com',
    #     'amplitude.com', # 'Amplitude' 
    #     'mixpanel.com', # 'MixPanel' 
    #     'adjust.com', # 'Adjust' "network_signature": "adj\\.st|adjust\\.com"
    #     'go2s.co',
    #     'moat.com', 'moatads.com', # 'Moat'  
    #     'umengcloud.com', 'yunos.com', 'umeng.com', # 'Umeng' "network_signature": "100\\.69\\.165\\.28|100\\.69\\.168\\.33|110\\.75\\.98\\.154|106\\.11\\.61\\.135|106\\.11\\.61\\.137|agoodm\\.m\\.taobao\\.com|agoodm\\.wapa\\.taobao\\.com|amdcopen\\.m\\.taobao\\.com|amdc\\.wapa\\.taobao\\.com|amdc\\.taobao\\.net|umengacs\\.m\\.taobao\\.com|umengjmacs\\.m\\.taobao\\.com"
    #     'vungle.akadns.net', 'vungle.com', # 'Vungle'
    #     'nexage.com', # 'Nexage' 
    #     'applvn.com', 'applovin.com', # 'AppLovin (MAX and SparkLabs)' 
    #     'chartboost.com', # ChartBoost' 
    #     'sectigo.com',
    #     'ssacdn.com', 'supersonic.com', 'supersonicads.com', 'supersonicads-a.akamaihd.net', # 'Supersonic Ads' 
    #     'app-measurement.com',
    #     'google-analytics.com', # 'Google Analytics' 
    #     'kochava.com', # 'Kochava'
    #     'cmcm.com', # 'Cheetah Ads' 
    #     'ksmobile.com', 'ksmobile.net',
    #     'openspeech.cn',
    #     'qq.com', # 'Tencent' 
    #     'voicecloud.cn',
    #     'usebutton.com', # 'Button' 
    #     'flurry.com', # 'Flurry'
    #     'gvt2.com',
    #     'acompli.net',
    #     'helpshift.com', # 'HelpShift' 
    #     'msedge.net',
    #     'singular.net', # 'Singular'
    #     'doodlemobile.com',
    #     'perfectionholic.com',
    #     'tapjoy.com', '5rocks.io', # 'Tapjoy' 
    #     'crwdcntrl.net', # 'Lotame' 
    #     'bugsnag.com', # 'Bugsnag'
    #     'charbeat.net',
    #     'bluekai.com', # 'BlueKai (acquired by Oracle)' 
    #     'criteo.net', # 'Criteo' 
    #     'wego.com',
    #     'wzrkt.com', # 'CleverTap' 
    #     'igexin.com'
    # ]