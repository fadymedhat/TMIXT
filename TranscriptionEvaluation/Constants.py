import os

PREDICTED_TRANSCRIPTION_PATH = os.path.join(os.getcwd(),'OutputCompleteDocument')#_23_05
TARGET_TRANSCRIPTION_PATH = os.path.join(os.getcwd(),'IMDBLabelGeneration/iamdb_generated_target')
TARGET_COPY_PATH = os.path.join(os.getcwd(),'OutputCompleteDocument_range')
WORD_GRAM_MODEL_NAME_PATH = os.path.join(os.getcwd(), "HOCRParser/rsc/wiki_unigrams.bin")
# WORD_GRAM_MODEL_NAME_PATH = os.path.join(os.getcwd(), "HOCRParser/rsc/GoogleNews-vectors-negative300.bin")

# TARGET_TRANSCRIPTION_PATH = sys.argv[1]
# PREDICTED_TRANSCRIPTION_PATH = sys.argv[2]
# TRG_TRANSCRIPTION_PATH = os.path.join(os.getcwd(), "IAMDBLabelGeneration/iamdb_generated_target/a01-000u.txt")
