# -*- coding: utf-8 -*-



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


class DocumentProcessor():

    # document_line_word_map = None


    def __init__(self):
        self.document_line_word_map = OrderedDict()

    def process_printed_transcription(self, line_word_map):
        """
        the function process a dictionary of lines and the words in each line
        each word is spell checked and added in a new dictionary with the output of the spell checker
        :param line_word_map:
        :return:
        """
        word_index = 0

        # spell check and crop uncorrect words
        for line_id, words in line_word_map.iteritems():
            # print(line_id, words)

            for word_index, word_box_map in enumerate(words):

                word_id = u"{:>02}".format(line_id) + '_' + "{:>02}".format(word_index)

                possible_words_list = self.generate_word_option_list(word_box_map.keys()[0])

                if len(possible_words_list) > 1:
                    self.crop_word_from_page(Constants.SRC_PAGE_PATH, Constants.CROPPED_IMAGES_PATH,
                                             current_box=word_box_map[word_box_map.keys()[0]],
                                             word_id=word_id)

                self.document_line_word_map[word_id] = possible_words_list

                word_index += 1

            word_index = 0

    def generate_word_option_list(self, word_to_check):
        """
        generate the options for each word based on the spell checking output
        :param word_to_check:
        :return:
        """
        #print(word_to_check)

        numeric_flag = False

        word_to_check_token_list = nltk.word_tokenize(word_to_check.decode('utf-8'))
        # print(word_to_check_token_list)
        # get the longest word from the token list and ignore the rest
        word_to_check_stripped = max(word_to_check_token_list, key=len)
        # get the index of the longest word to replace it with the corrected word
        token_index = word_to_check_token_list.index(word_to_check_stripped)
        # print (word_to_check_stripped)
        corrected_word = spell(word_to_check_stripped)
        # put the corrected word back in the list to merge them back in one string.
        try:
            float(word_to_check_stripped)
            numeric_flag = True
            corrected_word = word_to_check_stripped
        except (ValueError, TypeError):
            pass

        word_to_check_token_list[token_index] = corrected_word


        # merge all the tokens into one word together with the short tokens that were ignored previously
        corrected_word = ''.join(token for token in word_to_check_token_list)

        #print("Word To Check : ", word_to_check.lower(), " Corrected Word : ", corrected_word)

        if numeric_flag == False and ( (len(word_to_check) < 4 and word_to_check.lower() not in nlt_stop_words) \
                or word_to_check.lower() != corrected_word.lower() \
                or enchant_dic.check(word_to_check_stripped) == False):
            possible_words_list = [word_to_check.decode("utf-8", errors='ignore'),
                                   corrected_word.decode("utf-8", errors='ignore')]


        else:
            possible_words_list = [word_to_check.decode("utf-8", errors='ignore')]

        return possible_words_list

    def crop_word_from_page(self, page_path, dst_crop_path, current_box, word_id):
        """
        extract the word using the bounding box from the page and save it
        :param page_path:
        :param dst_crop_path:
        :param current_box:
        :param word_id:
        :return:
        """

        rows = [] #[previous_bound_box, current_bound_box, next_bound_box]

        current_bound_box = [int(number) for number in current_box.split(' ')]
        rows.append(current_bound_box)



        #rows = [previous_bound_box, current_bound_box, next_bound_box]

        min_x1 = min(map(itemgetter(0), rows))
        min_y1 = min(map(itemgetter(1), rows))
        max_x2 = max(map(itemgetter(2), rows))
        max_y2 = max(map(itemgetter(3), rows))


        whole_page = Image.open(page_path)
        #cropped_word = whole_page.crop(map(float, current_box.split()))
        cropped_word = whole_page.crop((min_x1,min_y1,max_x2,max_y2))

        old_size = cropped_word.size


        # new_size = np.asarray(cropped_word.size) + np.asarray([40,40]) #(800, 800)
        new_size = np.asarray(cropped_word.size)
        image_with_whitespace = Image.new("RGB", tuple(new_size), (255, 255, 255))  ## luckily, this is already black!
        image_with_whitespace.paste(cropped_word, ((new_size[0] - old_size[0]) / 2,
                                    (new_size[1] - old_size[1]) / 2))
        #image_with_whitespace.show()

        #cropped_word.save(os.path.join(dst_crop_path,word_id + ".png"))
        image_with_whitespace.save(os.path.join(dst_crop_path, word_id + ".png"))

    def call_hand_transcriber(self):
        """
        execute the hand transcriber (Laia)
        :return:
        """
        # os.system(
        #     'mogrify ' + Constants.CROPPED_IMAGES_PATH + os.sep + '"*" -resize "100x67%!" ' + Constants.CROPPED_IMAGES_PATH + os.sep + '*.png')
        os.system(
            'mogrify ' + Constants.CROPPED_IMAGES_PATH + os.sep + '"*" -resize "x64" -strip ' + Constants.CROPPED_IMAGES_PATH + os.sep + '*.png')
        os.system(Constants.HAND_TRANSCRIPTION_SCRIPT)

    def load_hand_written_transcription(self,hand_transcription_output_path):
        """
        load the output of Laia into a key,value dictionary
        :param hand_transcription_output_path:
        :return:
        """

        # load the hand writtn text
        word_hand_dictionary = {}
        f = open(os.path.join(hand_transcription_output_path, 'word.txt'), 'rU')
        for line in f:  ## iterates over the lines of the file
            key, value = line.partition(" ")[::2]
            if value.strip() != '':
                word_hand_dictionary[key] = value
            # print line,    ## trailing , so print does not add an end-of-line char
            ## since 'line' already includes the end-of line.
        f.close()
        return word_hand_dictionary

    def spell_check_hand_written_transcription(self, word_hand_map):
        """
        apply spell checking for each word from the handwriting transcription
        :param word_hand_map:
        :return:
        """

        for key, hand_word_context in word_hand_map.items():
            #print(key, hand_word_context)
            if key in self.document_line_word_map.keys():

                word_option_list = self.document_line_word_map[key]
                # hand_word_list = nltk.word_tokenize(hand_word_context)
                #print(key, hand_word_list)
                # hand_word = ' '.join(word for word in hand_word_list[1:-1])
                #hand_word = hand_word_list[0]

                # print(hand_word_context)
                word_option_list.append(hand_word_context.strip().decode('utf-8'))

                ##########
                word_to_check_token_list = nltk.word_tokenize(hand_word_context)
                # print(word_to_check_token_list)
                # get the longest word from the token list and ignore the rest
                word_to_check_stripped = max(word_to_check_token_list, key=len)
                # get the index of the longest word to replace it with the corrected word
                token_index = word_to_check_token_list.index(word_to_check_stripped)
                # print (word_to_check_stripped)
                corrected_word = spell(word_to_check_stripped)
                # put the corrected word back in the list to merge them back in one string.
                word_to_check_token_list[token_index] = corrected_word
                # merge all the tokens into one word together with the short tokens that were ignored previously
                corrected_word = ''.join(token for token in word_to_check_token_list)
                ############
                #word_option_list.append(corrected_word.strip().decode('utf-8'))


                #corrected_word = spell(hand_word)
                if hand_word_context.lower().strip() != corrected_word.lower().strip():
                    word_option_list.append(corrected_word)
                    #print (word_option_list)

                self.document_line_word_map[key] = word_option_list

    def process_hand_transcription(self,hand_transcription_output_path):
        """
        load the output of laia and spell check it
        :param hand_transcription_output_path:
        :return:
        """
        word_hand_map = self.load_hand_written_transcription(hand_transcription_output_path)
        self.spell_check_hand_written_transcription(word_hand_map)



