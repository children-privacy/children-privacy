import numpy as np
import pyLDAvis
from biterm.btm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms, topic_summuary

if __name__ == "__main__":

    texts = open('./data/reuters.titles').read().splitlines()[:100]

    # print(texts)
    # print(texts[1])

    # vectorize texts
    vec = CountVectorizer(stop_words='english')
    X = vec.fit_transform(texts).toarray()
    # print(len(X[0]))
    # print(X[0])

    # get vocabulary
    vocab = np.array(vec.get_feature_names())
    # print(vocab)

    # get biterms
    biterms = vec_to_biterms(X)
    # print(biterms)

    # create btm
    btm = oBTM(num_topics=20, V=vocab)
    # print(btm)

    print("\n\n Train BTM ..")
    topics = btm.fit_transform(biterms, iterations=100)

    print("\n\n Visualize Topics ..")
    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), vocab, np.sum(X, axis=0))
    pyLDAvis.save_html(vis, './vis/simple_btm.html')

    # print("\n\n Topic coherence ..")
    # topic_summuary(btm.phi_wz.T, X, vocab, 10)

    # print("\n\n Texts & Topics ..")
    # for i in range(len(texts)):
    #     # if topics[i].argmax() == 1:
    #     print("{} (topic: {})".format(texts[i], topics[i].argmax()))
