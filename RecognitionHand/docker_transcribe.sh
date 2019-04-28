#!/bin/bash

#INPUT_DIR=/home/fady/hcr_ocr/one_page_pipeline/hand_recognition/dir_input
#OUTPUT_DIR=/home/fady/hcr_ocr/one_page_pipeline/hand_recognition/dir_output

INPUT_DIR=`pwd`/RecognitionHand/dir_input
OUTPUT_DIR=`pwd`/RecognitionHand/dir_output
CHAR_TRANSCRIBE_FILE=char.txt
WORD_TRANSCRIBE_FILE=word.txt


# download the dataset
#FKI_USER=user0
#FKI_PASSWORD=123456
#wget -P data --user="$FKI_USER" --password="$FKI_PASSWORD" http://www.fki.inf.unibe.ch/DBs/iamDB/data/lines/lines.tgz;

#mkdir -p data/imgs;
#tar zxf data/lines.tgz -C data/imgs && \
#find data/imgs -name "*.png" | xargs -I{} mv {} data/imgs && \
#find data/imgs -name "???" | xargs rm -r;

# pull the docker image
#docker pull mauvilsa/laia:2017.09.14-cuda8.0-ubuntu16.04
# retag the docker image pulled 
#docker tag mauvilsa/laia:2017.09.14-cuda8.0-ubuntu16.04 laia:active

# run the docker image (this step is used to copy the script file to call the docker from inside the docker to you home)
#docker run --rm -it -u $(id -u):$(id -g) -v $HOME:$HOME laia:active bash -c "cp /usr/local/bin/laia-docker $HOME/bin"

# create a text file with a list of files that will be transcribed

rm $INPUT_DIR/filelist/filenames.lst

ls -d -1 $INPUT_DIR/images/* > $INPUT_DIR/filelist/filenames.lst

COMMAND="decode --batch_size 20  --log_level info   --symbols_table \
	$INPUT_DIR/symbtable/symbs.txt \
	$INPUT_DIR/model/model_htr.t7 \
	$INPUT_DIR/filelist/filenames.lst> $OUTPUT_DIR/$CHAR_TRANSCRIBE_FILE";


# local volumes mapped to the docker volumes
OPTS=( -u $(id -u):$(id -g) );
[ -d "/home" ]  && OPTS+=( -v /home:/home );
[ -d "/mnt" ]   && OPTS+=( -v /mnt:/mnt );
[ -d "/media" ] && OPTS+=( -v /media:/media );
[ -d "/tmp" ]   && OPTS+=( -v /tmp:/tmp );


# call the GPU docker for transcribing
nvidia-docker run --rm -t "${OPTS[@]}" laia:active \
  bash -c "cd $(pwd) && PATH=\" .:$PATH:\$PATH\" laia-$COMMAND";

# change the character transcription to words
awk '{
  printf("%s ", $1);
  for (i=2;i<=NF;++i) {
    if ($i == "<space>")
      printf(" ");
    else
      printf("%s", $i);
  }
  printf("\n");
}' $OUTPUT_DIR/$CHAR_TRANSCRIBE_FILE > $OUTPUT_DIR/$WORD_TRANSCRIBE_FILE;

# delete the character level transcription
# rm $OUTPUT_DIR/$CHAR_TRANSCRIBE_FILE
