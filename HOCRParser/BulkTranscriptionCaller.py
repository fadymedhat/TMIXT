import os
import glob
import Constants
from TranscriberMain import Transcriber
import subprocess
import shutil
file_list = glob.glob(os.path.join(os.getcwd(),'RecognitionPrinted/dir_output_whole_69_cent/*.hocr'))


for file_path in file_list:
    transcriber = Transcriber()
    shutil.rmtree(os.path.join(os.getcwd(), 'RecognitionHand/dir_input/images/'))
    os.mkdir(os.path.join(os.getcwd(), 'RecognitionHand/dir_input/images/'))

    shutil.rmtree(os.path.join(os.getcwd(), 'RecognitionHand/dir_output/'))
    os.mkdir(os.path.join(os.getcwd(), 'RecognitionHand/dir_output/'))

    Constants.SRC_HOCR_PATH = file_path
    Constants.SRC_PAGE_PATH = Constants.SRC_HOCR_PATH.replace('.hocr', '.tif')
    print file_path
    transcriber.transcribe()
