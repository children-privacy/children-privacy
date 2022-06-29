# bert.py
import datetime
import pickle
from data_generator import DataGenerator
from math import exp, log10
from numpy.core.fromnumeric import sort
from numpy.lib.function_base import median
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics import silhouette_samples, silhouette_score
import sys

import data_generator

class Clustering:
    '''
    self.index (array): the indexes of samples.
    self.df (array): the features of samples.
    self.labels (array): the clustering labels.
    self.dis (array): the distance data.
    '''

    def __init__(self, data, k=8, top=10):
        self.k = k
        self.top = top
        # self.load_data(data)
        self.data = data
    
    def load_csv(self, file):
        '''
        Load csv file chunk by chunk.

        file (str): csv file path.

        RETURNS 
        df (array): the data loaded from csv.
        '''
        chunk = pd.read_csv(file, chunksize=1000000)
        df = pd.concat(chunk)
        print(file, 'loaded.')
        return df
    
    def load_data(self, dataset=None):
        '''
        Load data from CSV file. Remove the index and store features in self.df.

        dataset (str): the path to a csv dataset file, generated by gen_dataset_from_vec().

        UPDATES
        self.index (array): the indexes of samples.
        self.df (array): the features of samples.
        '''
        if dataset:
            df = self.load_csv(dataset)
        else:
            df = self.load_csv(self.data)
        if 'index' in df.columns:
            self.index = df.get('index')
            df.pop('index')
        self.df = df

        print('Sample size =', self.df.shape)

    def kmeans(self, k=None):
        '''
        Conducts the k-means clustering.

        UPDATES 
        self.labels (array): the clustering labels.
        self.dis (array): the distance data.
        '''
        if k:
            self.k = k

        kmeans = KMeans(n_clusters=self.k).fit(self.df)
        centers = kmeans.cluster_centers_
        cosine_dis = sort(cdist(centers, centers, 'cosine'))
        # avg_min_dis = average(cosine_dis[:,1])
        # median_dis = median(cosine_dis[:,1])
        median_dis = min(cosine_dis[:,1])
        

        print(self.k, kmeans.inertia_)
        
        self.labels = kmeans.labels_
        self.dis = kmeans.transform(self.df)
        self.interia = kmeans.inertia_
        self.cos_median = median_dis
        self.centers = kmeans.cluster_centers_

    def silhouette(self):
        # silhouette_avg = silhouette_score(self.df, self.labels)
        # print(self.k, silhouette_avg)
        sample_silhouette_values = silhouette_samples(self.df, self.labels)
        
        print(self.k, np.mean(sample_silhouette_values))
        return sample_silhouette_values
    
    # def scale_data(self):
        # '''
        # Scale data using standard scaler (sklearn.presprocessing.StandardScaler).

        # UPDATES
        # self.df (array): the features of samples.
        # '''
        # scaler = StandardScaler()
        # self.df = pd.DataFrame(scaler.fit_transform(self.df))

    def plot(self):
        # fig, (ax1) = plt.subplots(1, 1)
        # fig.set_size_inches(9, 7)
        sample_silhouette_values = self.silhouette()
        # silhouette_avg = np.mean(sample_silhouette_values)
        # y_lower = 10

        counter_3 = 0
        counter_4 = 0
        counter_5 = 0
        counter_6 = 0
        counter_7 = 0

        for i in range(self.k):
            ith_cluster_silhouette_values = sample_silhouette_values[self.labels == i]

            # print('ith_cluster_silhouette_values', ith_cluster_silhouette_values)

            ith_cluster_silhouette_values.sort()

            positive = len(np.where(ith_cluster_silhouette_values > 0)[0])

            size_cluster_i = ith_cluster_silhouette_values.shape[0]

            # print(positive, size_cluster_i, positive/size_cluster_i)

            if positive/size_cluster_i > 0.3:
                counter_3 += 1
            if positive/size_cluster_i > 0.4:
                counter_4 += 1
            if positive/size_cluster_i > 0.5:
                counter_5 += 1
            if positive/size_cluster_i > 0.6:
                counter_6 += 1
            if positive/size_cluster_i > 0.7:
                counter_7 += 1

            # y_upper = y_lower + size_cluster_i

            # color = cm.nipy_spectral(float(i) / self.k)
            # ax1.fill_betweenx(np.arange(y_lower, y_upper),
            #                 0, ith_cluster_silhouette_values,
            #                 facecolor=color, edgecolor=color, alpha=0.7)

            # Label the silhouette plots with their cluster numbers at the middle
            # ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

            # Compute the new y_lower for next plot
            # y_lower = y_upper + 10  # 10 for the 0 samples

            # ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

        # print(counter_3/self.k*self.interia, counter_4/self.k*self.interia, counter_5/self.k*self.interia, counter_6/self.k*self.interia, self.k)

        
        # plt.show()
        
        return str(counter_3) + '\t' \
                + str(counter_4) + '\t' \
                + str(counter_5) + '\t' \
                + str(counter_6) + '\t' \
                + str(counter_7) + '\t' \
                + str(self.interia) + '\t' \
                + str(self.cos_median) + '\t' \
                + str(self.k) + '\n'

    # def snnl(self):
        # '''
        # Soft Nearest Neighbor Loss
        # Frosst, Nicholas, Nicolas Papernot, and Geoffrey Hinton. 
        # "Analyzing and improving representations with the soft nearest neighbor loss." 
        # International Conference on Machine Learning. PMLR, 2019.
        # '''
        # T = 1
        # distances = euclidean_distances(self.df)

        # inner = 0
        # intra = 0
        # for i in range(self.labels.shape[0]):
        #     for j in range(self.labels.shape[0]):
        #         if i != j:
        #             intra += exp(-distances[i][j]) / T
        #             if self.labels[i] == self.labels[j]:
        #                 inner += exp(-distances[i][j]) / T
        
        # snnl = -log10(inner / intra)
        
        # # print('inner', inner)
        # # print('intra', intra)
        # # print('snnl', snnl)
        # print(snnl, '*', self.interia, '=', snnl*self.interia)

    def get_top_samples(self, top=None):
        '''
        Get the information of top samples of each cluster.

        RETURNS
        sorted_res (dict): the sorted result contains top samples in each cluster.
        '''
        if top is None:
            top = self.top

        res = {}
        for i in range(self.k):
            res[i] = []

        for i in range(len(self.labels)):
            res[self.labels[i]].append({'index':self.index[i],'dis':min(self.dis[i])})
        
        sorted_res = {}
        for key in res.keys():
            sorted_res[key] = sorted(res[key], key=lambda k: k['dis'])[0:top]
        
        return sorted_res

    def output_top_samples(self, result, comment_file):
        '''
        Ouput top samples (nearest to the cluster center) in each cluster according to its comment content.

        result (array): the sorted result of clustering (top samples in each cluster).
        comment_file (str): the path to the comment file (extacted by pre_processor.py)

        OUTPUTS
        result.json (JSON file): top comments in each cluster
        '''
        # print(sorted_res)
        comments = open(comment_file, encoding="utf8").read().splitlines()
        # print(type(comments))
        output = []
        for key in result.keys():
            dict = {}
            # output.append([str(key)])
            dict['topic'] = key
            dict['comments'] = []
            for item in result[key]:
                index = int(item['index'])
                dict['comments'].append(comments[index].split('\t')[-1])
            output.append(dict)
        
        json_file = 'result_' + comment_file.split(os.path.sep)[-1].split('.')[0] + '_' + str(self.k) + '_' + str(self.top) + '.json'

        with open(json_file, 'w+') as res_json:
            json.dump(output, res_json)

        center_file = 'centers_' + comment_file.split(os.path.sep)[-1].split('.')[0] + '_' + str(self.k) + '_' + str(self.top) + '.pkl'
        with open(center_file, "wb") as pkl_f:
            pickle.dump(self.centers, pkl_f)

def count_comments(folder):
    counter = 0
    for (dirpath, dirnames, filenames) in os.walk(folder):
        for filename in filenames:
            if filename.startswith('comments') and filename.endswith('txt'):
                with open(os.path.join(dirpath, filename), "r", encoding="utf8") as f_comments:
                    num_lines = sum(1 for line in f_comments)
                    counter += num_lines
    print(counter)

def main():
    # data = r'C:\Age_Rating\NLP\vectors_64953_730877.csv'
    # sampling = 0.02
    # count_comments(folder)
    # c = Clustering(data)
    # dg.load_coment_paths()
    # dg.comments_to_vec()
    # c.init_vec_files()
    # dg.gen_dataset_from_vec(sampling)
    
    # c.kmeans()


    # comment_file = 'comments_Family_1_[1, 2].txt'
    
    # dataset = None
    # # dataset = 'dataset_56957_591672.csv'
    k = 40
    top = 20
    # sampling = 0.0001

    # c = Clustering(k, top)

    # if dataset is None:
    #     dataset = c.gen_dataset_from_vec('vectors_comments_Family_1_[1, 2].csv', sampling)

    # c.load_data(dataset)
    # c.kmeans()
    # c.output_top_samples(c.get_top_samples(top), comment_file)

    # c.load_data()
    # for i in range(1,21):
    #     c.kmeans(i*5)
    #     c.plot()
        
        # c.snnl()

    # c.kmeans(dataset, k)
    # c.get_top_samples(k, top, comment_file)

    # folder = r'C:\Age_Rating\NLP\data'
    folder = r'Z:\RS\Comments\per_category'
    # sampling = 0.005

    vector_files = DataGenerator(folder).get_files('vectors', 'csv')

    for file in vector_files:
    # for t in range(10):
    #     print('---------------', t, '----------------')
    #     file = DataGenerator(folder,sampling).comments_to_vec()
    #     print('Data file', file, 'generated.')
        
        # c = Clustering(file)
        # c.load_data()
        # output_file = 'result_' + str(datetime.datetime.now().strftime("%f")) + '.txt'
        # for i in range(1,21):
        #     c.kmeans(i*5)
        #     result = c.plot()
        #     with open(output_file, 'a+', encoding="utf8") as out_f:
        #         out_f.write(result) 

        c = Clustering(file,k,top)
        c.load_data()
        c.kmeans()
        comment = DataGenerator(folder).get_files(file.replace('vectors', 'sampled_comments').split('.')[0].split(os.path.sep)[-1],'txt')[0]
        c.output_top_samples(c.get_top_samples(), comment)
    


if __name__ == "__main__":
    main()