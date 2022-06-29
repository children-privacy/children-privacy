from numpy.core.fromnumeric import size
import spacy
import csv
import os
import numpy as np
import pandas as pd
import datetime
import sys
from sklearn.model_selection import train_test_split


class DataGenerator:
    def __init__(self, folder, sampling=0.02):
        self.folder = folder
        self.sampling = sampling
        self.comment_files = self.get_files('comment','txt')

    def get_comment_paths(self):
        '''
        Get the paths of raw_comments_[FOLDER]_[RATINGS].txt files.

        RETURN comment_files: the paths of comment files in a list
        '''
        comment_files = []
        
        for (dirpath, dirnames, filenames) in os.walk(self.folder):
            for filename in filenames:
                if filename.startswith('raw') and filename.endswith('txt'):
                    comment_files.append(os.path.join(dirpath, filename))

        print(len(comment_files), 'comment files loaded.')
        return comment_files

    def get_vector_paths(self):
        '''
        Get the paths of vector_FOLDER_[RATINGS].csv files.

        RETURN vector_files: the paths of comment files in a list
        '''
        vecotr_files = []
        
        for (dirpath, dirnames, filenames) in os.walk(self.folder):
            for filename in filenames:
                if filename.startswith('vectors') and filename.endswith('csv'):
                    vecotr_files.append(os.path.join(dirpath, filename))

        print(len(vecotr_files), 'vector files loaded.')
        return vecotr_files

    def get_files(self, start, extend):
        '''
        Get the paths of start*.extend fileys.

        RETURN files: the paths of start*.extend files in a list
        '''
        files = []
        
        for (dirpath, dirnames, filenames) in os.walk(self.folder):
            for filename in filenames:
                if filename.startswith(start) and filename.endswith(extend):
                    files.append(os.path.join(dirpath, filename))

        print(len(files), 'files loaded.')
        return files

    def sampling_buffer(self):
        '''
        Sampling the self.comments_buffer according to self.sampling
        '''
        if self.sampling < 1:
            _, self.comments_buffer = train_test_split(self.comments_buffer, test_size=self.sampling)
        elif len(self.comments_buffer) > self.sampling:
            _, self.comments_buffer = train_test_split(self.comments_buffer, test_size=self.sampling/len(self.comments_buffer))

    def gen_sampled_comments(self):
        '''
        Generate sampled comment files.

        RETURN data: a list of slected comments 
        '''
        
        for comment_file in self.comment_files:
            self.comments_buffer = open(comment_file, encoding="utf8").read().splitlines()
            self.comments_buffer = list(filter(None, self.comments_buffer))
            print(comment_file, 'with', len(self.comments_buffer), 'comments loaded.')
            # _, test = train_test_split(comments, test_size=self.sampling)
            self.sampling_buffer()
            # data += self.comments_buffer

            output_file = comment_file.replace('comments', 'sampled_comments')
            # 'sampled_' + comment_file.split(os.path.sep)[-1] + '_' + str(len(self.comments_buffer)) + '_' + str(datetime.datetime.now().strftime("%f")) + '.txt'
        
            with open(output_file, 'w+', encoding="utf8") as out_f:
                for i in range(len(self.comments_buffer)):
                    out_f.write(str(i) + '\t' + self.comments_buffer[i] + '\n') 
        
            print('Dataset', output_file, 'generated.')

        # return data, output_file

    def gen_comments_to_vec(self,files):
        '''
        Covnert comments to vectors using RoBERTa.
        
        comment_file (str): the path to comments.txt extacted by pre_processor.py.

        OUTPUTS vectors_filename.csv (a file): contains the index and 300 features
        '''
        nlp = spacy.load('en_core_web_lg')
        dim = nlp(" ").vector.shape[0]

        # comments, filename = self.sampling_comments()
        for file in files:
            print(file)
            comments = open(file, encoding="utf8").read().splitlines()
            comments = list(filter(None, comments))
            vector_save_path = file.split('.')[0].replace('sampled_comments', 'vectors') + '.csv'
            
            with open(vector_save_path, 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                head = []
                head.append('index')
                for i in range(dim):
                    head.append('feature' + str(i))
                spamwriter.writerow(head)

                for i in range(len(comments)):
                    vec = nlp(comments[i]).vector
                    vec = np.append([i], vec)
                    spamwriter.writerow(vec)
                    if i % 1000 == 0:
                        print(i, 'comements have been converted.',os.stat(vector_save_path).st_size/1000000, 'MB')
            
        # return vector_save_path
            
    
    # def init_vec_files(self):
    #     vec_files = []
    #     for (dirpath, dirnames, filenames) in os.walk(self.folder):
    #         for filename in filenames:
    #             if filename.startswith('vector') and filename.endswith('csv'):
    #                 vec_files.append(os.path.join(dirpath, filename))
    #     self.vec_files = vec_files
    #     print(len(self.vec_files), 'vector files found.')

    # def gen_dataset_from_vec(self, ratio, vec_file=None):
    #     '''
    #     Generate a dataset from vecotr file, stored in a csv file.

    #     vec_file (str): the path to vector file.
    #     ratio (float): the ratio of training set in the dataset to be generated.

    #     RETURNS 
    #     output_file (str): the path to the generated csv file, named as dataset_size.csv.
    #     '''
    #     if vec_file is not None:
    #         self.vec_files = []
    #         self.vec_files.append(vec_file)

    #     data = DataFrame()
        
    #     for vec in self.vec_files:
    #         df = self.load_csv(vec)
    #         print(df.shape[0], 'samples loaded.')
    #         _, test = train_test_split(df, test_size=ratio)
    #         if len(data) == 0:
    #             data = test
    #         else:
    #             data = pd.concat([data, test])
    #         print(data.shape[0], 'samples selected.')

        
    #     print(str(data.shape[0]), 'samples will be generated.')
    #     input_str = input("Press y to continue...")
        
    #     if input_str == 'y':
    #         output_file = 'dataset_' + str(data.shape[0]) + '_' + str(datetime.datetime.now().strftime("%f")) + '.csv'
    #         print('Start dataset generating...')
    #         data.to_csv(output_file, index=False)
    #         print('Dataset', output_file, 'with', len(data), 'samples generated.')

    #         return output_file
    #     else:
    #         sys.exit()

    def load_csv(self, csv_path):
        '''
        Load csv file chunk by chunk.

        csv_path (str): csv file path.

        RETURNS 
        df (array): the data loaded from csv.
        '''
        chunk = pd.read_csv(csv_path, chunksize=1000000)
        df = pd.concat(chunk)
        print(csv_path, 'loaded.')
        return df

def main():
    # folder = r'C:\Age_Rating\NLP\raw_comments[1,2]'
    folder = sys.argv[1]
    sampling = 50000

    # dg = DataGenerator(folder, sampling)
    # DataGenerator(folder, sampling).comments_to_vec()
    # dg.gen_dataset_from_vec(sampling)


    dg = DataGenerator(folder, sampling)
    # dg.gen_sampled_comments()
    sampled_files = dg.get_files('sampled','txt')
    dg.gen_comments_to_vec(sampled_files)
    


if __name__ == "__main__":
    main()