# btm_training.py

import numpy as np
import argparse
import pickle
import random
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer, _document_frequency
from biterm.utility import vec_to_biterms, topic_summuary

def create_vectorizer(texts):
    vec = CountVectorizer(stop_words='english', vocabulary=None)
    # vec = CountVectorizer(vocabulary=None)

    vec._validate_vocabulary()
    vocabulary, X = vec._count_vocab(texts, vec.fixed_vocabulary_)
    dfs = _document_frequency(X)
    
    # print("texts[0]", texts[0])
    # print(max(dfs), min(dfs))
    # print("len(dfs)", len(dfs))
    # print("dfs", dfs)
    # print(sorted(dfs))
    dfsorted = sorted(dfs)

    # min_df = 
    # print(dfsorted[int(len(dfs)*0.5)], dfsorted[int(len(dfs)*0.98)])

    # vec.min_df = dfsorted[int(len(dfs)*0.002)] / len(texts)
    vec.min_df = 3
    # vec.max_df = 0.95 * len(texts)
    vec.max_df = dfsorted[int(len(dfs)*0.99)] / len(texts)

    # print(vec.max_df, vec.min_df)

    # X = np.array(vec.fit_transform(texts).toarray())
    # print(len(X[0]))
    return vec

def select_samples(sample_path, num):
    # Randomly select training samples
    texts = open(sample_path,encoding="utf8").read().splitlines()
    if num == -1:
        num = len(texts)
    if num < len(texts):
        texts = random.sample(texts, num)
    print('Set size of training sets as: ' + str(num) + '.')
    
    return texts

def create_btm(texts, vcb=None, num_topics=20):
    
    vec = create_vectorizer(texts)

    X = np.array(vec.fit_transform(texts).toarray())
    
    # Get vocabulary
    vocab = np.array(vec.get_feature_names())

    # print(sum(X), len(sum(X)))

    for j in range(3):
        print("texts[j]",texts[j])
        print("sum(X[j])",sum(X[j]))
        for i in range(len(X[j])):
            if X[j][i] != 0:
                index = i
                print(i, vocab[i])
        print('\n')

    # Get biterms
    biterms = vec_to_biterms(X)

    # Create btm
    btm = oBTM(num_topics=num_topics, V=vocab)
 
    return btm, biterms, X, vocab

def train_online_btm(btm, biterms, chunk_size):
    print("Train Online BTM for {} rounds ..".format(int(len(biterms)) / chunk_size))
    for i in range(0, int(len(biterms)), chunk_size): 
        biterms_chunk = biterms[i:i + chunk_size]
        btm.fit(biterms_chunk, iterations=50)

    return btm

def write_to_pickle(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', metavar='N_REVIEWS', type=int, default=1000, help='The number of training reviews to be loaded.')
    parser.add_argument('-t', metavar='N_TOPICS', type=int, default=20, help='The number of topics.')
    parser.add_argument('-s', metavar='CHUNK_SIZE', type=int, default=100, help='Size of online learning chunk.')
    parser.add_argument('-o', metavar='OUTPUT_FILENAME', type=str, default='btm', help='Filename of output file.')
    parser.add_argument('-p', metavar='SAMPLE_PATH', type=str, default='./data/comments.txt', help='Path to comments.')

    args = parser.parse_args()

    num = args.n
    num_topics = args.t
    chunk_size = args.s
    filename = args.o + '_' + str(num) + '_' + str(num_topics)
    sample_path = args.p

    data_set = select_samples(sample_path, num)

    # write_to_pickle(data_set, filename + '.dat')

    btm, biterms, X, vocab = create_btm(data_set, num_topics=num_topics)
    model = train_online_btm(btm, biterms, chunk_size)

    topics = model.transform(biterms)
    topic_summuary(model.phi_wz.T, X, vocab, 20)

    # write_to_pickle(model, filename + '.mdl')
    # write_to_pickle(vocab, filename + '.vcb')

    # create_vectorizer(data_set)
if __name__ == "__main__":
    main()

