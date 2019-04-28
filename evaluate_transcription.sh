#!/bin/bash

#TARGET_DIR=`pwd`/IMDBLabelGeneration/iamdb_generated_target
#PREDICTED_DIR=`pwd`/OutputCompleteDocumentWholeDataset

python `pwd`/TranscriptionEvaluation/Evaluator.py

#find "$PREDICTED_DIR" -type f | \
#while read PREDICTED_TRANS
#do 
#	if [[ $PREDICTED_TRANS == *".txt"* || $PREDICTED_TRANS == *".json"* ]]; then
#		echo "Processing predicted : $PREDICTED_TRANS"
#		TARGET_TRANS=$TARGET_DIR"/"$(basename "$PREDICTED_TRANS")
#		echo "Target file:"$TARGET_TRANS
		# Process image types
#		python `pwd`/TranscriptionEvaluation/Evaluator.py $TARGET_TRANS $PREDICTED_TRANS;	
		
#	fi

#done
