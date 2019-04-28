import sent2vec
import numpy as np

import Constants
import Utils


class EmbeddingEvaluation(object):

    metric_list = [] # a list of accuracy for each document in the dataset
    metric_map = {} # a map of percentages ranges and the document count in each range


    def __init__(self):
        self.similarity_list = []

        self.model = sent2vec.Sent2vecModel()
        # self.model.load_model('./HOCRParser/rsc/wiki_unigrams.bin')
        self.model.load_model(Constants.WORD_GRAM_MODEL_NAME_PATH)

        # import gensim
        #
        # # Load Google's pre-trained Word2Vec model.
        #
        # self.model = gensim.models.KeyedVectors.load_word2vec_format(Constants.WORD_GRAM_MODEL_NAME_PATH, binary=True)
        # #self.model = gensim.models.Word2Vec.load_word2vec_format(Constants.WORD_GRAM_MODEL_NAME_PATH, binary=True)
        # self.model.wv['computer']


    def calculate(self, target_paragraph, predicted_paragraph):


        # from sklearn.manifold import TSNE

        # em_change = self.model.embed_sentence("exchange move")
        # em_a = self.model.embed_sentence("a")
        # em_x = self.model.embed_sentence("x")
        # "any", "00_09": "more", "00_10": "Labour
        # em_change = self.model["any"]
        # em_move = self.model["more"]
        # em_a = self.model["labor"]
        # em_mare = self.model["mare"]
        # em_x = self.model.wv["x"]

        # X_embedded = TSNE(n_components=2).fit_transform(np.vstack((em_a,em_x)))
        #
        # Utils.cosine_similarity_sklearn(em_a, em_change)
        # Utils.cosine_similarity_sklearn(em_x, em_change)


        embedding_target = self.model.embed_sentence(target_paragraph.lower())
        embedding_predicted = self.model.embed_sentence(predicted_paragraph.lower())
        document_vec_similarity = Utils.cosine_similarity_sklearn(embedding_target, embedding_predicted)
        self.metric_list.append(document_vec_similarity)
        key = int(np.floor_divide(document_vec_similarity, 10))
        self.metric_map[key] = self.metric_map.get(key, 0) + 1
