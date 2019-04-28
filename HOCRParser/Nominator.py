from __future__ import division

import itertools
import math
import sent2vec
from decimal import *
getcontext().prec = 100

import Utils
import Constants



import os
import enchant
import nltk
import numpy as np

import Constants
from StopWords import nlt_stop_words

from collections import OrderedDict
from operator import itemgetter
from PIL import Image
from autocorrect import spell

enchant_dic = enchant.Dict("en_US")
# st_wo = STOP_WORDS


class Nominator():


    def __init__(self):
        self.model = sent2vec.Sent2vecModel()
        # self.model.load_model('./HOCRParser/rsc/wiki_unigrams.bin')
        self.model.load_model(Constants.WORD_GRAM_MODEL_NAME_PATH)


    def dummy_pick_one_word(self, transcribed_document):
        """
        choose a word from the list of options
        :param transcribed_document:
        :return:
        """

        mid_dict = int(len(transcribed_document) / 2)
        for indx, key in enumerate(transcribed_document):
            # print(indx, key)
            value = transcribed_document[key]
            #print(value)
            if len(value) == 1:
                transcribed_document[key] = value[0]
            else:

                # word_list_exclude_unknown = [word for i ,word in enumerate(value) if value[i].lower().find('<unk>') ]
                #
                # word_set, word_count_per_set = np.unique(word_list_exclude_unknown, return_counts=True)
                # majority_vote_index = np.argmax(word_count_per_set)
                # transcribed_document[key] = value[majority_vote_index]


                # if the list is three elements then the printed and spelled printed are different and the handwritten
                # spell checking is the same as the handwritten so most probably the handwritten is the right one

                options_count = len(value)
                if options_count == 2:

                    transcribed_document[key] = value[options_count - 1]
                    # take the fist option if the second is unknown
                    if value[options_count - 1].lower().strip().find('<unk>') != -1:
                        transcribed_document[key] = value[0]

                elif options_count == 3:

                    # transcribed_document[key] = value[options_count-1]
                    # if value[options_count-1].lower().strip().find('<unk>') != -1:
                    # take the third option
                    transcribed_document[key] = value[2]
                    if value[options_count - 1].lower().strip().find('<unk>') != -1:
                        transcribed_document[key] = value[0]

                elif options_count == 4:
                    transcribed_document[key] = value[options_count - 1]
                    # take the second option if the fourth is unknown
                    if value[options_count - 1].lower().strip().find('<unk>') != -1:
                        transcribed_document[key] = value[1]
                        if value[1].lower().strip().find('<unk>') != -1:
                            transcribed_document[key] = value[0]

                            # if indx < mid_dict:
                            #     transcribed_document[key] = value[0]
                            # else:
                            #     transcribed_document[key] = value[index]
                            # for key, options in transcribed_document.items():
                            #     print(key, options)
                            #     if type(options) == list:
                            #
                            #         transcribed_document[key] = options[0]

            #print(transcribed_document[key])





    def generate_bigrams(self, list_a, list_b):
        """

        :param list_a:
        :param list_b:
        :return:
        """
        bigram_list = []

        if list_a == None:
            bigram_list = list_b
        elif list_b == None:
            bigram_list = list_a
        else:
            bigram_cross_join_list = list(itertools.product(list_a, list_b))

            for bigram_tuple in bigram_cross_join_list:
                string_tuple = ' '.join(bigram_tuple)
                #word_token_list = nltk.word_tokenize(string_tuple)
                #string_tuple = ' '.join(word_token_list)
                bigram_list.append(string_tuple)

        return bigram_list

    def generate_embeddings_vectors(self, bigram_option_list):
        """

        :param bigram_option_list:
        :return:
        """

        embeddings_list = []
        for string in bigram_option_list:
            embedding = self.model.embed_sentence(string.lower())
            embeddings_list.append(embedding)

        return embeddings_list

    def compute_similarity(self, prev_embedding_list, next_embedding_list):
        """

        :param prev_embedding_list:
        :param next_embedding_list:
        :param base:
        :return:
        """
        next_similarity_list = []
        similarity_list = []
        for prev_embedding in prev_embedding_list:
            for next_embedding in next_embedding_list:

                # similarity_value = Utils.cosine_similarity_sklearn(Utils.softmax(prev_embedding), Utils.softmax(next_embedding))
                similarity_value = Utils.cosine_similarity_sklearn(prev_embedding,next_embedding)
                #similarity_value =  np.linalg.norm(prev_embedding + next_embedding)

                next_similarity_list.append(similarity_value)

            max_next_similarity = max(next_similarity_list)
            similarity_list.append(max_next_similarity)


        index = similarity_list.index(max(similarity_list))# + 1 # +1 to makeup for the zero-indexed list

        return index #int(math.ceil(float(index)/base)-1) # -1 to makeup for the zero-indexed list



    def smart_pick_one_word(self, transcribed_document):
        """
        choose a word from the list of options
        :param transcribed_document:
        :return:
        """

        for index, key in enumerate(transcribed_document):

            # print "---------------------NEW word-----------------"
            # print(index, key)
            previous_option_list = None
            current_option_list = None
            next_option_list = None

            current_option_list = transcribed_document[key]


            if index != 0:
                previous_option_list = transcribed_document.values()[index-1]

            if index != len(transcribed_document)-1 :
                next_option_list = transcribed_document.values()[index+1]


            prev_bigram_option_list = self.generate_bigrams(previous_option_list, current_option_list)
            next_bigram_option_list = self.generate_bigrams(current_option_list,next_option_list)

            prev_bigram_option_list = [x.encode('utf-8') for x in prev_bigram_option_list]
            next_bigram_option_list = [x.encode('utf-8') for x in next_bigram_option_list]

            prev_bigram_option_list =  map(str.lower, prev_bigram_option_list)
            next_bigram_option_list = map(str.lower, next_bigram_option_list)


            # print(prev_bigram_option_list)
            # print(current_option_list)
            # print(next_bigram_option_list)


            prev_embedding_option_list = self.generate_embeddings_vectors(prev_bigram_option_list)
            next_embedding_option_list = self.generate_embeddings_vectors(next_bigram_option_list)

            # base = len(current_option_list)
            # if next_option_list != None:
            #     base *= len(next_option_list)
            candidate_index = self.compute_similarity(prev_embedding_option_list, next_embedding_option_list)


            transcribed_document[key] = [current_option_list[candidate_index]]


            #print current_option_list[candidate_index]
            # bigram_option_list = itertools.chain(prev_bigram_option_list, next_bigram_option_list)

        for index, key in enumerate(transcribed_document.keys()):
            transcribed_document[key] = transcribed_document[key][0]
















    #
    # def take_similarity(self, word0, word1, word2):
    #     str1 = ' '.join([word0,word1])
    #     str2 = ' '.join([word1,word2])
    #     emb1 = self.model.embed_sentence(str1.lower())
    #     emb2 = self.model.embed_sentence(str2.lower())
    #     print('emb1 =', len(emb1))
    #     print('emb2 =', len(emb2))
    #     similarity_value = self.cosine_similarity_custom(emb1, emb2)
    #     print('similarity_value',similarity_value , 'String 1', str1 , 'String 2', str2)
    #     return similarity_value
    #
    #
    # def choose_best_pair(self,word0,value, word1):
    #     max_val = 0
    #     num = [[None]*len(value)]*len(word1 )
    #     selected_value_index=0
    #     for i in range(len(word1)):
    #         for j in range(len(value)):
    #             # print('i=',i,'j=',j)
    #             # print(num)
    #             word0 = word0[0]
    #             num[i][j] = self.take_similarity(word0, value[j], word1[i])
    #             if num[i][j] > max_val:
    #                 max_val = num[i][j]
    #                 selected_value_index = j
    #     return selected_value_index
    #
    #
    # def smart_pick_one_word(self, transcribed_document):
    #     """
    #     choose a word from the list of options
    #     :param transcribed_document:
    #     :return:
    #     """
    #     transcribed_document_list = transcribed_document.items()
    #     list_key = []
    #     list_value = []
    #
    #     value = []
    #     #put keys and values of whole document in separate lists
    #     for i in range(len(transcribed_document_list)):
    #         list_key.append(transcribed_document_list[i][0])
    #         list_value.append(transcribed_document_list[i][1])
    #     #for two first words of the document
    #     if len(list_value[0])== 1 and len(list_value[1])==1:
    #        transcribed_document_list[0] = list_value[0]
    #        transcribed_document_list[1] = list_value[1]
    #     else:
    #         word0 = transcribed_document_list[0]
    #         word1 = transcribed_document_list[1]
    #         num=[]
    #         max_val=0
    #         for i in range(len(word0)):
    #             for j in range(len(word1)):
    #                 num[i][j]= self.cosine_similarity_custom(self, word0[i], word1[j])
    #                 if num[i][j]>max_val:
    #                     max_val= num[i][j]
    #                     best_val_word0=i
    #                     best_val_word1=j
    #         transcribed_document_list[0] = word0[best_val_word0]
    #         transcribed_document_list[1] = word1[best_val_word1]
    #         list_value[0] = word0[best_val_word0]
    #         list_value[1] = word0[best_val_word1]
    #     #for third word onwards
    #     for i in range(2, len(transcribed_document_list)):
    #         value = list_value[i]
    #         word0 = list_value[i - 1]
    #         #if we have not reached the last word and there is no word after that
    #         if i == len(transcribed_document_list)-1:
    #             word1 = list_value[i + 1]
    #             #if the last current word is just one option
    #             if len(value)==1:
    #                 transcribed_document_list[i]=list_value[i]
    #
    #             else:
    #                 #if current word is more than one option
    #                 max_val = 0
    #                 best_val = self.choose_best_pair(word0, value, word1)
    #                 transcribed_document_list[i] = value[best_val]
    #                 list_value[i] = value[best_val]
    #         else:
    #             num = []
    #             #if we have reached the last word and its just one option
    #             if len(value) ==1:
    #                 transcribed_document_list[i] = list_value[i]
    #             else:
    #                 #if the last word is more than one option
    #                 for j in range(len(value)):
    #                     emb1 = self.model.embed_sentence(value[j].lower())
    #                     emb2 = self.model.embed_sentence(word0[0].lower())
    #                     num.append(self.cosine_similarity_custom(emb1, emb2))
    #
    #                     # if num[j]> max_val:
    #                     #
    #                     #     max_val= num[j]
    #                     #     best_val_word1=j
    #
    #                 best_val_word1 = num.index(max(num))
    #                 transcribed_document_list[i] = word1[best_val_word1]
    #                 list_value[i] = word1[best_val_word1]
    #
    #     print ('The recognized text:',transcribed_document_list)
