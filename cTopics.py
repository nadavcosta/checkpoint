import pickle
import string
import heapq
from itertools import chain
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from prettytable import PrettyTable


class Topics(object):
    "Using the titles of the articles collected; generate a list of top 5 topics per month \
    Show results for each month of 2019."

    def __init__(self, file):
        self.file = file
        self.data = self._load_and_clean_data()

        self.vectorizer = TfidfVectorizer(stop_words='english',
                                          use_idf=True,
                                          max_features=3000,
                                          smooth_idf=True)

        self.svd = TruncatedSVD(n_components=5,
                                algorithm='randomized',
                                random_state=23,
                                n_iter=10)

    def _load_and_clean_data(self):
        data_dict = self._load_data()

        for k, v in data_dict.items():
            data_dict[k] = [s.translate(str.maketrans('', '', string.punctuation)) for s in
                            list(chain.from_iterable(list(v.values())))]
        # @[,]
        return data_dict

    def _load_data(self):
        with open(self.file, 'rb') as h:
            data_dict = pickle.load(h)
        # @[,dict]
        return data_dict

    def fit_transform(self, data):
        """
        Args:
            data (list):
        """
        U = Pipeline([('tfidf', self.vectorizer), ('svd', self.svd)]).fit_transform(data)  # documents-topics
        V_T = self.svd.components_         # topics-words
        return U, V_T

    def print_n_dominante_words_topic_(self, V=None, n=30):
        """
        :param n (int):
        :param V_T (words, topics):
        :return:
        """
        if not V:
            V = self.svd.components_  # words-topics

        words = self.vectorizer.get_feature_names()
        pt = PrettyTable()

        pt.add_column('Topic1', [words[i] for i in range(len(words)) if i in V[0, :].argsort()[-n:][::-1]])
        pt.add_column('Topic2', [words[i] for i in range(len(words)) if i in V[1, :].argsort()[-n:][::-1]])
        pt.add_column('Topic3', [words[i] for i in range(len(words)) if i in V[2, :].argsort()[-n:][::-1]])
        pt.add_column('Topic4', [words[i] for i in range(len(words)) if i in V[3, :].argsort()[-n:][::-1]])
        pt.add_column('Topic5', [words[i] for i in range(len(words)) if i in V[4, :].argsort()[-n:][::-1]])

        print(pt)


if __name__ == '__main__':

    topics_ = Topics(file="./titles_2002.pickle")



