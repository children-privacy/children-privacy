import numpy as np
# import pyLDAvis
import argparse
import pickle
# import math
#from biterm.cbtm import oBTM
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
from biterm.utility import vec_to_biterms, topic_summuary

if __name__ == "__main__":

    texts = open('./data/comments.txt',encoding="utf8").read().splitlines()[:200]

    # # # n = 400

    # vectorize texts
    vec = CountVectorizer(stop_words='english')
    # # ,min_df=0.0001,max_df=0.05
    # # X = vec.fit_transform(texts).toarray()
    X = np.array(vec.fit_transform(texts).toarray())
    # # print(X)

    print('get vocabulary')
    vocab = np.array(vec.get_feature_names())

    # # print(vocab[:500])
    # # print(len(vocab))

    print('get biterms')
    biterms = vec_to_biterms(X)
    # # print(biterms[0])
    # # print(len(biterms))

    # print('create btm')
    # btm = oBTM(num_topics=30, V=vocab)

    # print("\n\n Train Online BTM ..")
    # for i in range(0, int(len(biterms)), 100): # prozess chunk of 200 texts
    #     biterms_chunk = biterms[i:i + 100]
    #     btm.fit(biterms_chunk, iterations=50)
    # # biterms_chunk = biterms[:n]
    # # btm.fit(biterms_chunk, iterations=50)

    # object_btm = btm
    # file_btm_obj = open('btm.obj', 'wb') 
    # pickle.dump(object_btm, file_btm_obj)

    file_btm_obj = open('btm.obj','rb') 
    btm = pickle.load(file_btm_obj)

    topics = btm.transform(biterms)

    # print("\n\n Visualize Topics ..")
    # vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), vocab, np.sum(X, axis=0))
    # # pyLDAvis.save_html(vis, './vis/online_btm_' + str(n) + '.html')
    # pyLDAvis.save_html(vis, './vis/online_btm_' + 'online_all2' + '.html')

    print("\n\n Topic coherence ..")
    topic_summuary(btm.phi_wz.T, X, vocab, 20)

    print("\n\n Texts & Topics ..")

    for k in range(10):
        j = 0
        for i in range(len(texts)):
            if topics[i].argmax() == k:
                print("{} (topic: {})".format(texts[i], topics[i].argmax()))
                j += 1
                if j > 10:
                    break
