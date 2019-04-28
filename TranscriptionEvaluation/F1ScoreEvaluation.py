import numpy as np
import Utils
from Tokenizer import Tokenizer

class F1ScoreEvaluation(object):


    precision_list = []
    precision_count_map = {}

    recall_list = []
    recall_count_map = {}

    f1score_list = []
    f1score_count_map = {}



    def calculate(self, target_paragraph, predicted_paragraph):

        tokenizer = Tokenizer()

        target_words_list = tokenizer.tokenize_to_words_nltk(target_paragraph.encode('utf-8'))
        predicted_words_list = tokenizer.tokenize_to_words_nltk(predicted_paragraph.encode('utf-8'))

        dictionary = Utils.construct_dictionary([target_words_list, predicted_words_list])
        target_bow, predicted_bow = Utils.retrieve_bag_of_words(dictionary, target_words_list, predicted_words_list)
        document_precision, document_recall, document_f1score = Utils.calculate_bow_precision_recall(target_bow,
                                                                                                     predicted_bow,
                                                                                                     len(target_words_list),
                                                                                                     len(predicted_words_list))
        self.precision_list.append(document_precision)
        key = int(np.floor_divide(document_precision, 10))
        self.precision_count_map[key] = self.precision_count_map.get(key, 0) + 1

        self.recall_list.append(document_recall)
        key = int(np.floor_divide(document_recall, 10))
        self.recall_count_map[key] = self.recall_count_map.get(key, 0) + 1

        self.f1score_list.append(document_f1score)
        key = int(np.floor_divide(document_f1score, 10))
        self.f1score_count_map[key] = self.f1score_count_map.get(key, 0) + 1