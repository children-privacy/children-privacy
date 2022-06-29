# db_to_plot.py

import sqlite3
import os
import sys

class DB_to_plot:
    def __init__(self, input_folder, output_folder) -> None:
        self.input_folder = input_folder
        self.output_folder = output_folder

    def import_db(self):
        '''
        Read .db file into self.privacy and self.flow lists.
        '''
        conn = None
        try:
            conn = sqlite3.connect(self.db)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            self.privacy = list(c.execute('SELECT app_package, app_name, pii_type, sink_dns_fqdn, pii_value from privacy_table'))
            # test
            print(self.privacy)
            self.flow = list(c.execute('SELECT app_package, app_name, sink_dns_fqdn from passive_table')) 
            # test
            # print(self.flow)
        except sqlite3.Error as e:
            print(e)
            sys.exit(-1)

    def summarize_data(self):
        pass

    def summarize(self):
        for (dirpath, dirnames, filenames) in os.walk(self.input_folder):
            for filename in filenames:
                if filename.endswith('db') and filename.startswith('lumen'):
                    print('Summarizing', os.path.join(dirpath, filename))
                    self.db = os.path.join(dirpath, filename)
                    self.import_db()
                    self.summarize_data()

def main():
    input_folder = sys.argv[1]
    output_folder = r'C:\Users\User\My_Drive\_Research\_Age_Rating\Results\Privacy_Leakage\Summary'
    
    DB_to_plot(input_folder, output_folder).summarize()

if __name__ == "__main__":
    main()
