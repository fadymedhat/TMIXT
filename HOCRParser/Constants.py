import os
import sys

SRC_HOCR_PATH = sys.argv[1]
# SRC_HOCR_PATH = os.path.join(os.getcwd(),'RecognitionPrinted/dir_output/b06-027.hocr')
SRC_PAGE_PATH = SRC_HOCR_PATH.replace('.hocr', '.tif')

# SRC_HOCR_PATH = None
# SRC_PAGE_PATH = None
#TRG_TRANSCRIPTION_PATH = os.path.join(os.getcwd(), "IAMDBLabelGeneration/iamdb_generated_target/a01-000u.txt")
CROPPED_IMAGES_PATH = os.path.join(os.getcwd(), "RecognitionHand/dir_input/images")
HAND_TRANSCRIPTION_SCRIPT= os.path.join(os.getcwd(), "RecognitionHand/docker_transcribe.sh")
HAND_TRANSCRIPTION_OUTPUT_PATH = os.path.join(os.getcwd(), "RecognitionHand/dir_output")
COMPLETE_TRANSCRIPTION_OUTPUT_PATH = os.path.join(os.getcwd(), "OutputCompleteDocument")

WORD_GRAM_MODEL_NAME_PATH = os.path.join(os.getcwd(), "HOCRParser/rsc/wiki_unigrams.bin")
# WORD_GRAM_MODEL_NAME_PATH = os.path.join(os.getcwd(), "HOCRParser/rsc/twitter_unigrams.bin")
# WORD_GRAM_MODEL_NAME_PATH = os.path.join(os.getcwd(), "HOCRParser/rsc/wiki_bigrams.bin")


