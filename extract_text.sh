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

# dictionary used for scoring
WORDS_DICTIONARY=$PRINT_PARENT_DIR"/rsc/words-master.txt"

#___________________________________
# 1. copy the original image to the temp output dir, let it be temp_image
# 2. deskew temp_image 
# 3. enhance temp_image
# 4. for 4 times do:rotate - call tesseract - calculate score, pick the document with max_score for the next steps
# 5. copy temp_image to the parent output dir with its original name
# 6. call tesseract to generate the hocr
# 7. call the HOCRParser 
#___________________________________

mkdir -p $TEMP_DIRECTORY
find "$INPUT_DIRECTORY" -type f | \
while read FILENAME_FULL_PATH
do

	echo "Processing: $FILENAME_FULL_PATH"
	FILENAME_FULL_PATH_NO_EXT=$OUTPUT_DIRECTORY"/"$(basename $FILENAME_FULL_PATH | cut -d. -f1)
	echo "Fullname no extension: "$FILENAME_FULL_PATH_NO_EXT


	if [[ $FILENAME_FULL_PATH == *".jpg"* || $FILENAME_FULL_PATH == *".png"*  || $FILENAME_FULL_PATH == *".tif"* ]]; then
		echo -e "Image Deskewing...\n"

		TEMP_IMAGE=$TEMP_DIRECTORY"r0.tif"
		echo $TEMP_IMAGE
		cp "$FILENAME_FULL_PATH" $TEMP_IMAGE
		$PRINT_PARENT_DIR/bin/deskew64 "$TEMP_IMAGE" -o "$TEMP_IMAGE" -b ffffff
		$PRINT_PARENT_DIR/bin/imgtxtenh -u mm -d 118.1102362205 $TEMP_IMAGE $TEMP_IMAGE;

		echo -e "Rotating\n"
		echo $
		# Generate 4-rotations
		echo -e "90.\c"
		convert $TEMP_IMAGE -rotate 90  $TEMP_DIRECTORY"r1.tif"
		echo -e "180.\c"
		convert $TEMP_IMAGE -rotate 180 $TEMP_DIRECTORY"r2.tif"
		echo -e "270.\n"
		convert $TEMP_IMAGE -rotate 270 $TEMP_DIRECTORY"r3.tif"		


		# Run Tesseract in parallel
		wait
		echo -e "Parallel Tesseract...\n"
		
		{
		echo "before the jobs ..."
		find $TEMP_DIRECTORY -name '*.tif' | parallel  -j 4 tesseract {} {}
		} #&> /dev/null # redirects the output to the null device	
		echo -e ""

		# Evaluate each result and choose "best" based on my fast C++ dictonary score
		echo -e "            Scores: [\c"
		maxscore=0
		maxfilen=""
		for i in `seq 0 3`;
		do
			TEXT_FILE=$TEMP_DIRECTORY"r"$i".tif.txt"
			score=$($PRINT_PARENT_DIR/bin/dict-search $TEXT_FILE $WORDS_DICTIONARY)
			echo -e $score",\c"
			if [[ $score -gt $maxscore ]]; then
				maxscore=$score
				maxfilen=$TEXT_FILE
				cp $TEMP_IMAGE $FILENAME_FULL_PATH_NO_EXT".tif"
				tesseract $FILENAME_FULL_PATH_NO_EXT".tif" $FILENAME_FULL_PATH_NO_EXT -l eng -psm 1 hocr
				rm `pwd`/RecognitionHand/dir_input/images/*
				rm `pwd`/RecognitionHand/dir_output/*
				python `pwd`/HOCRParser/TranscriberMain.py $FILENAME_FULL_PATH_NO_EXT".hocr"
				
			fi
		done
		
		echo -e "\b] Max: "$maxscore" ("$maxfilen")"



	else
		# Process known-markup types
		echo -e "            Tika Extracting...\c"
		{
			java -jar tools/tika-app.jar -d -T "$FILENAME_FULL_PATH" | tee "$FILENAME_FULL_PATH_NO_EXT"".txt"
		} &> /dev/null
		echo -e "Done"
	fi



	# Remove newline characters (replace them with a space) and remove trailing spaces
	#tr '\n' ' ' < "$FILENAME_FULL_PATH"".txt" | tr -s " " > "$FILENAME_FULL_PATH"".tmp.txt"
	#mv "$fout"".tmp.txt" "$fout"".txt"
	##chmod 755 "$FILENAME_FULL_PATH"".txt" 
	##chmod 755 "$TEMP_DIRECTORY" 

	# clearout the temporary directory
	##rm -r "$TEMP_DIRECTORY"


	# Delete file if its empty
	#if [ ! -s "$FILENAME_FULL_PATH"".txt" ] ; then
	##rm "$FILENAME_FULL_PATH"".txt"
	#fi

done

