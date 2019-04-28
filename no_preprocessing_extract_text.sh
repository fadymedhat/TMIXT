#!/bin/bash

# High-level OCR preprocessing
# Chris G. Willcocks

# Specify paths for current data processing
# laste patent: dataset="USP2014w26"
height=64
dataset="data" 


PRINT_PARENT_DIR=`pwd`/RecognitionPrinted
HAND_PARENT_DIR=`pwd`/RecognitionHand

INPUT_DIRECTORY=$PRINT_PARENT_DIR/dir_input
OUTPUT_DIRECTORY=$PRINT_PARENT_DIR/dir_output

TEMP_DIRECTORY=$OUTPUT_DIRECTORY"/temp/"


#___________________________________
# 1. copy the original image to the temp output dir, let it be temp_image
# 2. deskew temp_image 
# 3. enhance temp_image
# 4. copy temp_image to the parent output dir with its original name
# 5. call tesseract to generate the hocr
# 6. call the HOCRParser 
#___________________________________

mkdir -p $TEMP_DIRECTORY

find "$INPUT_DIRECTORY" -type f | \
while read FILENAME_FULL_PATH
do
	echo "Processing: $FILENAME_FULL_PATH"
	FILENAME_FULL_PATH_NO_EXT=$OUTPUT_DIRECTORY"/"$(basename $FILENAME_FULL_PATH | cut -d. -f1)
	echo "Fullname no extension: "$FILENAME_FULL_PATH_NO_EXT


	if [[ $FILENAME_FULL_PATH == *".jpg"* || $FILENAME_FULL_PATH == *".png"*  || $FILENAME_FULL_PATH == *".tif"* ]]; then

		TEMP_IMAGE=$TEMP_DIRECTORY"r0.tif"
		echo $TEMP_IMAGE
		cp "$FILENAME_FULL_PATH" $TEMP_IMAGE
		$PRINT_PARENT_DIR/bin/deskew64 "$TEMP_IMAGE" -o "$TEMP_IMAGE" -b ffffff
		$PRINT_PARENT_DIR/bin/imgtxtenh -u mm -d 118.1102362205 $TEMP_IMAGE $TEMP_IMAGE;
		#convert $TEMP_IMAGE -resize 150x100%! $TEMP_IMAGE
		cp $TEMP_IMAGE $FILENAME_FULL_PATH_NO_EXT".tif"
		tesseract $FILENAME_FULL_PATH_NO_EXT".tif" $FILENAME_FULL_PATH_NO_EXT -l eng -psm 1 hocr
		rm `pwd`/RecognitionHand/dir_input/images/*
		rm `pwd`/RecognitionHand/dir_output/*
		python `pwd`/HOCRParser/TranscriberMain.py $FILENAME_FULL_PATH_NO_EXT".hocr"
			
	fi

done
