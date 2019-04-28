import json
import numpy as np
from gensim import corpora

from collections import OrderedDict
from Tokenizer import Tokenizer
from sklearn.metrics.pairwise import cosine_similarity


def load_transcription(file_path):
    """
    load the target data
    :param file_path:
    :return:
    """
    json_data = open(file_path).read()
    # to load the json file ordered with the key, we use the Ordered Dictionary
    target_transcription = json.loads(json_data, object_pairs_hook=OrderedDict)
    return target_transcription



def concate_document(document):

    return ' '.join(document[k].strip().lower() for k in document)




def retrieve_bag_of_words(raw_text):
    dictionary = corpora.Dictionary([raw_text])
    corpus = [dictionary.doc2bow(tok) for tok in [raw_text]][0]
    corpus_dictionary = dict(corpus)


    [dictionary[key] for key, value in corpus_dictionary.iteritems()]
    return corpus


def retrieve_bag_of_words(dictionary, target_words_list, predicted_words_list):

    bag_of_words = [dictionary.doc2bow(tok) for tok in [target_words_list, predicted_words_list]]
    target_bow = dict(bag_of_words[0])
    predicted_bow = dict(bag_of_words[1])

    # print target_bow
    # print predicted_bow
    return target_bow, predicted_bow


def construct_dictionary(token_list):

    dictionary = corpora.Dictionary(token_list)
    #print dictionary
    dictionary.compactify()
    return dictionary


# def calculate_bow_precision_recall(target_bow, predicted_bow):
#     word_match_count = 0
#     for index, key in enumerate(predicted_bow):
#         if target_bow.has_key(key) == False:
#             print key, "not here"
#         else:
#             if target_bow[key] > 0:
#                 print 'before', target_bow[key]
#                 target_bow[key] -= 1
#                 word_match_count += 1
#                 print 'after', target_bow[key]
#                 print key, "decremented"
#             else:
#                 del (target_bow[key])
#                 print key, "deleted"
#
#     # no. of true positives found in the prediction over total words in the target (true +ve and false -ve)
#     recall = float(word_match_count) / len(target_bow.items())
#
#     # no. of true positives  found in the prediction over total words in the prediction (true +ve and false +ve)
#     precision = float(word_match_count) / len(predicted_bow.items())
#
#     print precision, recall

def calculate_bow_precision(target_bow, predicted_bow):

    true_positive_count = 0
    false_positive_count = 0

    for index, key in enumerate(predicted_bow):
        if target_bow.has_key(key) == False:
            #print key, "not here"
            false_positive_count += predicted_bow[key]
        else:
            # here we found the key and we have 3 possible scenarios
            # count target is equal to predicted
            # count target is more than predicted
            # cound target is less than predicted

            if target_bow[key] == predicted_bow[key]:
                true_positive_count += predicted_bow[key]
            elif target_bow[key] > predicted_bow[key]:
                #false_negatives_count = 0 # not interested in this at the moment for precision
                true_positive_count += target_bow[key] - predicted_bow[key]
            elif target_bow[key] < predicted_bow[key]:
                false_positive_count += predicted_bow[key] - target_bow[key]


    # no. of true positives  found in the prediction over total words in the prediction (true +ve and false +ve)
    precision = float(true_positive_count) / (true_positive_count + false_positive_count) * 100
    #print precision
    return precision


def calculate_bow_precision_recall(target_bow, predicted_bow, target_count, predicted_count):

    true_positive_count = 0

    for index, key in enumerate(predicted_bow):

        if target_bow.has_key(key) == True:
            # here we found the key and we have 3 possible scenarios
            # count target is equal to predicted
            # count target is more than predicted
            # cound target is less than predicted

            if target_bow[key] == predicted_bow[key]:
                true_positive_count += predicted_bow[key]
            elif target_bow[key] > predicted_bow[key]:
                true_positive_count += predicted_bow[key]
            elif target_bow[key] < predicted_bow[key]:
                true_positive_count += target_bow[key]


    # no. of true positives  found in the prediction over total words in the prediction (true +ve and false +ve)
    precision = float(true_positive_count) / (predicted_count) * 100
    recall = float(true_positive_count) / (target_count) * 100

    f1score = (2 * precision * recall)/(precision + recall)
    #print precision, recall, f1score
    return precision, recall,f1score


def print_evaluation_map(evaluation_name, map, evaluation_list):
    print('______________________ '+evaluation_name +' Ranges ______________________')
    sorted_ranges_map = sorted(map.items())
    for key, value in sorted_ranges_map:
        print('Documents between ' + str(key * 10) + '% and ' + str((key + 1) * 10) + '% are ' + str(value))

    print(evaluation_name + ' = ' + str(np.mean(evaluation_list)) + ' %')


def cosine_similarity_sklearn(x, y):
    """

    :param x:
    :param y:
    :return:
    """

    result = cosine_similarity(np.array(x).reshape(1, -1), np.array(y).reshape(1, -1))
    return result[0][0]*100