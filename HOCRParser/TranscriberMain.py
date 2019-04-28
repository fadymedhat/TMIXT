# -*- coding: utf-8 -*-
import json
import os
import sys

import Constants
from DocumentProcessor import DocumentProcessor
from HParser import HParser
from Nominator import Nominator



# this couple of lines to prevent throwing exceptions when unicode characters are
# present in the text
reload(sys)
sys.setdefaultencoding('utf8')


class Transcriber():

    def transcribe(self):

        print "Current working dir : %s" % os.getcwd()

        # parse the HOCR html file
        parser = HParser()
        parser.retrieve_printed_transcription_map(Constants.SRC_HOCR_PATH)

        # process each word in the document processor
        document_processor = DocumentProcessor()
        document_processor.process_printed_transcription(parser.line_word_map)

        #print ("Processing Printed : " , document_processor.document_line_word_map)

        # transcribe the handwritten text
        document_processor.call_hand_transcriber()
        document_processor.process_hand_transcription(Constants.HAND_TRANSCRIPTION_OUTPUT_PATH)
        # print ("Processing Hand : " , document_processor.document_line_word_map)


        # nominate one word for any of the list of options generated from the previous steps
        nominator = Nominator()
        #nominator.smart_pick_one_word(document_processor.document_line_word_map)
        nominator.dummy_pick_one_word(document_processor.document_line_word_map)
        #print(document_processor.document_line_word_map)

        full_transcription_filename = os.path.basename(Constants.SRC_HOCR_PATH).replace('.hocr','.txt')

        with open(os.path.join(Constants.COMPLETE_TRANSCRIPTION_OUTPUT_PATH, full_transcription_filename), 'w') as outfile:
            json.dump(document_processor.document_line_word_map, outfile)


        # # evaluate the final document containing both the printed and handwriting transcription
        # evaluator = Evaluator()
        # evaluator.evaluate(document_processor.document_line_word_map)


if __name__ == '__main__':
    transcriber = Transcriber()
    transcriber.transcribe()
