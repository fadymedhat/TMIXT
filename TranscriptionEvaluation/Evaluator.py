import os
import difflib
import Utils

import Constants
import numpy as np
from fuzzywuzzy import fuzz
from Tokenizer import Tokenizer
from LevenshteinEvaluation import LevenshteinEvaluation
from F1ScoreEvaluation import F1ScoreEvaluation
from EmbeddingEvaluation import EmbeddingEvaluation

class Evaluator():

    def __init__(self):
        self.similarity_list = []



    def calculate_unmatched_total(self, target_transcription, predicted_transcription):
        """

        :param target_transcription:
        :param predicted_transcription:
        :return:
        """

        unmatched_count = 0
        for key, value in target_transcription.iteritems():
            print(key, value)
            if key in predicted_transcription.keys() and predicted_transcription[key] != target_transcription[key]:
                print(" Match found")
            else:
                print(" The word: ", value, "of key ", key, " Not found in target or words mismatch")
                unmatched_count += 1

        print('Total unmatched count', unmatched_count, " out of ", len(target_transcription))



    def match_sequences(self, target_lines, predicted_lines):
        """

        :param target_transcription:
        :param document:
        :return:
        """

        print('Target    :',target_lines)
        print('Generated :',predicted_lines)


        seq = difflib.SequenceMatcher(None, target_lines[0:int(len(target_lines) / 2)],
                                      predicted_lines[0:int(len(predicted_lines) / 2)])
        d = seq.ratio() * 100
        print ('1st half ',d)

        seq = difflib.SequenceMatcher(None, target_lines[int(len(target_lines) / 2):len(target_lines)],
                                      predicted_lines[int(len(predicted_lines) / 2):len(predicted_lines)])
        d = seq.ratio() * 100
        print ('2nd half ', d)

        seq = difflib.SequenceMatcher(None, target_lines, predicted_lines)
        d = seq.ratio() * 100
        print ('Both halves ', d)


    def compare_words(self, target_paragraph, predicted_paragraph):
        """

        :param target_transcription:
        :param document:
        :return:
        """

        tokenizer = Tokenizer()
        target_words = tokenizer.tokenize_to_words(target_paragraph)
        predicted_words = tokenizer.tokenize_to_words(predicted_paragraph)


        count = 0
        words_len = min(len(target_words), len(predicted_words))
        print words_len
        for i in range(words_len):
            if target_words[i] == predicted_words[i]:
                count+=1
        print count
        print (count/float(words_len)) *100





    def compare_sentences(self, target_paragraph, predicted_paragraph):
        """

        :param target_transcription:
        :param predicted_document:
        :return:
        """

        document_similarity = []
        #
        # tokenizer = Tokenizer()
        #
        # target_sentences = tokenizer.tokenize_to_sentences_punk(target_paragraph)
        # predicted_sentences = tokenizer.tokenize_to_sentences_punk(predicted_paragraph)
        #
        # from itertools import izip_longest
        #
        # [item for slist in izip_longest(target_sentences, predicted_sentences) for item in slist if item is not None]
        # target_vs_predicted_sentence_list = list(izip_longest(target_sentences, predicted_sentences))
        #
        # for target_sentence, predicted_sentence in target_vs_predicted_sentence_list:
        #     print target_sentence
        #     print predicted_sentence
        #     print
        #
        # # print(len(target_sentences), len(predicted_sentences))
        # sent_len = min(len(target_sentences), len(predicted_sentences))
        # # print('No of sentences: ' + str(sent_len))
        # # for i in range(sent_len):
        # #     print "%s\n%s\n\n" % (target_sentences[i],predicted_sentences[i])



        # for i in range(sent_len):
        #     #seq = difflib.SequenceMatcher(None, target_sentences[i],predicted_sentences[i])
        #     #similarity_list.append(seq.ratio())
        #     seq = fuzz.partial_ratio(target_sentences[i], predicted_sentences[i])
        #     document_similarity.append(seq)
        #     self.similarity_list.append(seq)

        seq = fuzz.partial_ratio(target_paragraph, predicted_paragraph)
        document_similarity.append(seq)
        self.similarity_list.append(seq)


        #print self. similarity_list
        #print('Accuracy = '+ str((sum(similarity_list)/len(similarity_list))*100)+' %')

        return np.mean(document_similarity)




if __name__ == '__main__':

    """
    the main evaluation entry point
    call different evaluation methods from here
    :param predicted_transcription:
    :return:
    """


    evaluator = Evaluator()


    from LevenshteinNLTKEvaluation import LevenshteinNLTKEvaluation
    from FuzzyEvaluation import FuzzyEvaluation
    from FuzzyTokenSortEvaluation import  FuzzyTokenSortEvaluation

    levenshtein = LevenshteinEvaluation()
    f1score = F1ScoreEvaluation()
    embedding = EmbeddingEvaluation()
    #levenshtein_nltk = LevenshteinNLTKEvaluation()
    fuzzy = FuzzyEvaluation()
    fuzzy_token_sort = FuzzyTokenSortEvaluation()


    file_count = 0
    for root, dirs, files in os.walk(Constants.PREDICTED_TRANSCRIPTION_PATH, topdown=False):

        for name in sorted(files):
            if name.endswith(".txt"):
                file_count += 1
                target_file = os.path.join(Constants.TARGET_TRANSCRIPTION_PATH, name)
                predicted_file = os.path.join(root, name)

                print name

                # loading the predicted and target transcription
                target_transcription = Utils.load_transcription(target_file)
                predicted_transcription = Utils.load_transcription(predicted_file)

                # concatenating the predicted and target transcription in a single line paragraph
                target_paragraph = Utils.concate_document(target_transcription)
                predicted_paragraph =  Utils.concate_document(predicted_transcription)

                # few printing lines for debugging
                # print("Target document word count", len(target_transcription))
                # print("Predicted document word count", len(predicted_transcription))
                # print('Target transcription   ', target_transcription)
                # print('Predicted transcription', predicted_transcription)
                # evaluator.calculate_unmatched_total(target_transcription, predicted_transcription)



                #------------------ START levenshtein evaluation ----------------------------------------#
                levenshtein.calculate(target_paragraph, predicted_paragraph)
                #levenshtein_nltk.calculate(target_paragraph, predicted_paragraph)
                # import nltk
                # metrics = nltk.metrics.distance.edit_distance()
                #
                # edit_distance_examples = [
                #     ("rain", "shine"), ("abcdef", "acbdef"), ("language", "lnaguaeg"),
                #     ("language", "lnaugage"), ("language", "lngauage")]
                # for s1, s2 in edit_distance_examples:
                #     print("Edit distance between '%s' and '%s':" % (s1, s2), edit_distance(s1, s2))
                # for s1, s2 in edit_distance_examples:
                #     print("Edit distance with transpositions between '%s' and '%s':" % (s1, s2),
                #           edit_distance(s1, s2, transpositions=True))
                #
                # s1 = set([1, 2, 3, 4])
                # s2 = set([3, 4, 5])
                # print("s1:", s1)
                # print("s2:", s2)
                # print("Binary distance:", binary_distance(s1, s2))
                # print("Jaccard distance:", jaccard_distance(s1, s2))
                # print("MASI distance:", masi_distance(s1, s2))

                # ------------------ END levenshtein evaluation ----------------------------------------#

                # ------------------ START precision/recall evaluation ----------------------------------------#
                f1score.calculate(target_paragraph, predicted_paragraph)
                # ------------------ START precision evaluation ----------------------------------------#
                embedding.calculate(target_paragraph, predicted_paragraph)
                fuzzy.calculate(target_paragraph, predicted_paragraph)
                fuzzy_token_sort.calculate(target_paragraph, predicted_paragraph)

                #self.match_sequences(target_paragraph, predicted_paragraph)
                # document_accuracy = evaluator.compare_sentences(target_paragraph, predicted_paragraph)
                # evaluator.compare_words(target_paragraph, predicted_paragraph)

                # if document_accuracy < 50:
                #     print('File name ----------------------------- : ', name, ' accuracy: ', document_accuracy)
                #     print


    Utils.print_evaluation_map('levenshtein', levenshtein.metric_map, levenshtein.metric_list)
    Utils.print_evaluation_map('precision', f1score.precision_count_map,f1score.precision_list)
    Utils.print_evaluation_map('recall', f1score.recall_count_map,f1score.recall_list)
    Utils.print_evaluation_map('F1Score',f1score.f1score_count_map,f1score.f1score_list)
    Utils.print_evaluation_map('Vector similarity', embedding.metric_map, embedding.metric_list)
    #Utils.print_evaluation_map('levenshtein NLTK', levenshtein_nltk.metric_map, levenshtein_nltk.metric_list)
    Utils.print_evaluation_map('fuzzy', fuzzy.metric_map, fuzzy.metric_list)
    Utils.print_evaluation_map('fuzzy token sort', fuzzy_token_sort.metric_map, fuzzy_token_sort.metric_list)
    print('File Count = ' + str(file_count))