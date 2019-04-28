# -*- coding: utf-8 -*-
import os
import re
import csv
import glob
import nltk
import json
from collections import OrderedDict



hand_transcription_path = 'lines_tab_delimiter.txt'
printed_transcription_path = 'printed_raw_text_files'
generated_target='iamdb_generated_target'



def load_printed_text(filename):

    printed_text = open(filename, 'r').readlines()
    # remove newline from each line in the printed character file
    printed_text = [x.rstrip('\n') for x in printed_text]
    return printed_text


def load_hand_text():
    csv_row_count = 0
    handwritten_document_lines_map = {}
    with open(hand_transcription_path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            csv_row_count += 1
            print(row)
            file_key = row['filename'].rpartition('-')[0]
            print(file_key)
            if file_key not in handwritten_document_lines_map.keys():
                handwritten_document_lines_map[file_key] = []

            line_list = handwritten_document_lines_map[file_key]
            line_list.append(row['transcription'])
            handwritten_document_lines_map[file_key] = line_list

    print("number of sentences :", csv_row_count)
    print("number of documents :", len(handwritten_document_lines_map))
    return handwritten_document_lines_map



def retrieve_document_map(filename, mismatch_document_count):
    print(filename)

    document_id = os.path.basename(filename).replace('.txt', '')

    printed_content = load_printed_text(filename)
    print("Printed transcription : ", printed_content)

    handwritten_content = handwritten_document_lines_map[document_id]
    print("Handwritten transcription : ", handwritten_content)


    complete_document = {}
    complete_document = OrderedDict()

    printed_validation_count = 0
    line_index = 0
    word_index = 0
    for line in printed_content:
        # split line using nltk tokenizer
        word_list = nltk.word_tokenize(line)
        print (word_list)
        for word in word_list:
            complete_document["{:>02}".format(line_index)+'_'+"{:>02}".format(word_index)] = word
            word_index += 1
            printed_validation_count += 1
        word_index = 0
        line_index += 1
    print("Printed    Output  : ", complete_document)


    #complete_document = {}
    word_index = 0
    handwritten_validation_count = 0
    for line in handwritten_content:
        word_list = [word_delimiter for word_delimiter in re.split('(\.|\||\,)', line) if
                     word_delimiter != '' and word_delimiter != '|']
        for word in word_list:
            complete_document["{:>02}".format(line_index) + '_' + "{:>02}".format(word_index)] = word
            word_index += 1
            handwritten_validation_count += 1

        word_index = 0
        line_index += 1

    print("Handwritten Output : ", complete_document)

    print('Complete document has word count =', len(complete_document))
    print('Printed word count =', printed_validation_count)
    print('Handwritten word count =', handwritten_validation_count)

    if handwritten_validation_count != printed_validation_count:
        # if os.path.basename(filename) in exception_list.keys():
        #     word_difference_count = exception_list[os.path.basename(filename)]
        #     printed_validation_count += word_difference_count
        #assert handwritten_validation_count == printed_validation_count
        print("Handwritten word count ='",handwritten_validation_count,
              "Printed word count ='",printed_validation_count, "------------------ Count mismatch")
        mismatch_document_count +=1
    else:
        print(filename, " ========================================================= Match")


    #for key in sorted(complete_document.iterkeys()):
    #    print "%s: %s" % (key, complete_document[key])
    print(complete_document)
    return mismatch_document_count , complete_document






    # print([line.replace('|',' ') for line in handwritten_content])





handwritten_document_lines_map = load_hand_text()


# retrieve the list of filenames
filename_list = [file_name for file_name in glob.glob(printed_transcription_path + "/*.txt")]


document_count = 0
mismatch_document_count = 0
for filename in filename_list:
    mismatch_document_count, complete_document = retrieve_document_map(filename, mismatch_document_count)
    document_count += 1
    with open(os.path.join(generated_target, os.path.basename(filename)), 'w') as outfile:
        json.dump(complete_document,outfile)
    print("Document Count :", document_count)


print ("Mismatch Document Count = ",mismatch_document_count)


#--- lines.txt ---------------------------------------------------------------#
#
# iam database line information
#
# format: a01-000u-00 ok 154 19 408 746 1663 91 A|MOVE|to|stop|Mr.|Gaitskell|from
#
#     a01-000u-00  -> line id for form a01-000u
#     ok              -> result of word segmentation
#                            ok: line is correctly segmented
#                            err: segmentation of line has one or more errors
#
#                        notice: if the line could not be properly segmented
#                                the transcription and extraction of the whole
#                                line should not be affected negatively
#
#     154             -> graylevel to binarize line
#     19              -> number of components for this line
#     408 746 1663 91 -> bounding box around this line in x,y,w,h format
#
#     A|MOVE|to|stop|Mr.|Gaitskell|from
#                     -> transcription for this line. word tokens are separated
#                        by the character |
#
