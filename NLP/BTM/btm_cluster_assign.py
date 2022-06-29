# btm_cluster_assign.py

import numpy as np
import random
import argparse
import pickle
from btm_training import select_samples, create_btm
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms, topic_summuary

def load_pickle(filename):
    with open(filename,'rb') as file:
        obj = pickle.load(file)
    return obj

def assign_cluster(data_set, btm, vocab, output=True):
    _, biterms, X, _ = create_btm(data_set, vcb=vocab)
    result = btm.transform(biterms)

    if output==True:
        print("\n\n Topic coherence ..")
        topic_summuary(btm.phi_wz.T, X, vocab, 20)

    print(result[0])
    
    return result

def display(data_set, result, n_top):
    n_sample, n_topic  = result.shape
    top = np.zeros((n_topic, n_top, 2))
    top = top -1

    print(top)
    result_summary = np.zeros([n_sample, 3])

    for i in range(n_sample):
        result_summary[i] = [result[i].argmax(), max(result[i]), i]
    
    print(top)
    print(result_summary[0])

    for pair in result_summary:
        if top[int(pair[0])][0][0] < pair[1]:
            top[int(pair[0])][0] = [pair[1], pair[2]]
            for i in range(len(top)):
                top[i] = top[i][top[i][:,0].argsort()]
    
    print(top)



    for i in range(len(top)):
        for top_topic in top[i]:
            if int(top_topic[1]) != -1:
                print("(topic: {}) {} ".format(i, data_set[int(top_topic[1])]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', metavar='NUMBER', type=int, default=10000, help='The number of input reviews.')
    parser.add_argument('-m', metavar='INPUT', type=str, required=True, help='Filename of btm obj and vocabulary files.')
    parser.add_argument('-d', metavar='DATA', type=str, default='./data/comments.txt', help='Path to comments.')

    args = parser.parse_args()

    num = args.n
    model = args.m
    data_path = args.d

    data_set = select_samples(data_path, num)
    vcb = load_pickle(model + '.vcb')
    btm = load_pickle(model + '.mdl')

    result = assign_cluster(data_set, btm, vcb)

    display(data_set, result, 10)

if __name__ == "__main__":
    main()
