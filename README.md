# TMIXT: An architecture for Transcribing MIXed handwritten and machine-printed Text #

Machine printed or handwritten text transcription is challenging each on its own and it becomes even more challenging when
both of them are on the same page, e.g. forms. Through TMIXT, we present a framework to tackle this problem through using
several opensource libraries.

# Flow Overview
The proposed system is composed of several sub-systems and several conditional decisions, which decide the direction of execution
within the whole pipeline. So let's discuss a general overview of the system and get more into the details.

The system expects the input to be an input page that may contain a mix between machine and hand text. Below are the general steps
in order a page has to go through to create the final transcription. 
Note: package names used for each step is included between [brackets]

1. deskew [deskew] the page to revert any anglular tilt in the page. it doesn't matter if the page is bottom-up or horizontal. 
we only want to remove any tilt in the page
2. Enhance [imgtxtenh] the page to remove any noise and increase the contrast between the text and the background of the page. 
3. Rotate [convert] the deskewed version 3 times in addition to the previously deskewed version.
4. For each of the 4 rotations (0, 90, 180, 270) apply Printed Text transcription to generate a .txt transcription.
5. score [Custom Module] each of the .txt file to check which one has the highest availability of words aganist a dictionary.
6. Generate an hOCR [Tesseract] file for the page with the highest score.
7. parse [Custom Module - HOCRParser] the hOCR file.
8. for each word in the hOCR file, create a list of possible options to be filled following the below conditions:

      a. apply a spellchecking aganist a dictionary
		* [Option 1] if the word exists the use this word as it is in the output. 
		* [Option 2] if it doesn't exist then crop the unrecognized word from the page and call the Handwritten Transcriber [Laia] for it. 
       
      b. apply spellchecking again on the output of the Handwritting Transcriber
		* [Option 3] if it exists in the dictionary, add it to the list 
		* [Option 4] if it doesn't exist add the dictionary's correction to the list. 
     
9. Nominate [Custom Module - HOCRParser] the most possible choice from the list of possible options for each word either through a
rule based method or using a trained model e.g. SKIP-Gram or CBOW
10. Evaluate [Custom Module - TranscriptionEvaluation] the system predicted transcription aganist the target transcription. 
    

## Getting Started

### Prerequisit
The system was tested on Ubuntu 16.0.4

   * Software and packages:
    
      * [Deskew](https://bitbucket.org/galfar/app-deskew/src/default/) 
      * [imgtxtenh](https://github.com/mauvilsa/imgtxtenh)
      * [Parallel](http://manpages.ubuntu.com/manpages/bionic/man1/parallel.1.html) 
      * [Tesseract](https://github.com/tesseract-ocr/)
      * [Laia](https://github.com/jpuigcerver/Laia)
      * [docker](https://www.docker.com/)
      * [nvidia-docker](https://github.com/NVIDIA/nvidia-docker)

   * Python environment and packages:
   
      * Python 2.7.12
      * scipy 1.0.0
      * numpy 1.11.0
      * fuzzywuzzy 0.16.0
      * nltk 3.2.5
      * sent2vec 0.0.0
      * gensim 3.3.0
      * Pillow 5.1.0
      * pyenchant 2.0.0
      * scikit_learn 0.19.1
      
   * Pretrained Sent2vec
      
   you will need to download a pretrained [sent2vec](https://github.com/epfml/sent2vec) model and place it in the HOCRParser/rsc folder
    
   * We used the [wiki-unigram](https://drive.google.com/file/d/0B6VhzidiLvjSa19uYWlLUEkzX3c/view) model
   
   
### Configuration


   Make sure the previous packages and software is installed correctly. Some are already there in the RecognitionPrinted/bin folder
   e.g. deskew and imgtxtenh. So you do not need to install these two.
   
   There is no specific configuration required the code should run as soon as you clone it to your local system.
   

# Modules

  * IMDBLabelGeneration: to generate the target labels required for evaluation by extending the [IAMDB dataset](http://www.fki.inf.unibe.ch/databases/iam-handwriting-database)
  * RecognitionPrinted: scripts and binaries for deskewing, rotating, scoring and transcriping printed text [Tesseract](https://github.com/tesseract-ocr/)  
  * RecognitionHand: contains script required for pulling the Laia docker from [dockerhub](https://hub.docker.com/) and
  installing it. 
  * HOCRParser: python scripts for parsing hocr files and calling the Laia (the handwriting framework)  
  * TranscriptionEvaluation: scripts for evaluating the transcription aganist the target labels.



#### IAMDB Label Generation

The IAMDB handwritten dataset is composed of 1539 pages written by 600 writers. Each page is made up of a printed text
in the top half of the page and the handwritten transcription by the writers in the lower half of the page.
We throught this is a good candidate dataset to evaluate our proposed system as it contains both the printed and handwritten text
on the same page. Accordingly, we implemented this module to generate a single json file per document containing the word key
and the word itself irrespective of the type of the word (printed or handwritten). 
An example of the generated target transcription is:

    {"00_00": "A", "00_01": "MOVE", "00_02": "to", "00_03": "stop", ... , "10_05": "Exchange", "10_06": "."}

The word key "00_01" means line one (00) and second word in the line (01)

Most important folders in IMDBLabelGeneration:

* iamdb_generated_target - this is the target transcription in json for each document in the dataset.



#### Printed Recognition

Most important folders in RecognitionPrinted:

* bin - binaries required for deskewing, enhancing and scoring a page.
* dir_input - this where you have to place the pages to be transcribed
* dir_output - this will hold the generated hOCR (from Tesseract) and the enhanced version of each page in the input directory.

#### Hand Recognition 

Most important folders in RecognitionHand:

* dir_input - this where you have to place the pages to be transcribed
    * filelist - this folder is required by Laia to hold the file names to be hand transcribed. 
    The filenames.lst is automatically generated through the main script. 
    * images - holds the handwritten images to be transcribed
    * model - a pretrained model (the available model has been trained on the IAMDB dataset. It took 3 days of training on a Geforce 1080TI. 
    Refer to Laia training documentation on GitHub for more details.)
    * symbtable - literals used by Laia
* dir_output - this will hold the generated handwritten transcription generated by Laia.


#### HOCR Parser

The main processing module that links printed transcription and calls the handwritten transcriber to take over.
The module is also responsible for spellchecking and croping of text and most importantly nominating the most possible 
word option for words that are mistakenly transcribed by either printed or the handwriting module.

* TranscriberMain is the entry point for this module. 
* If you want to call this module manually on a specific document, you have to specify the hOCR file path in the Constants.py
otherwise, this script is to be called from the main transcription shell script in the parent directory of the pipeline.


#### Transcription Evaluation

This is the evaluation module. It loads the generated transcription in the "OutputCompleteDocument" folder and its corresponding
target transcription from the IAMDB label generation module.

The evaluation module has several evaluation metrics and others could be included.
   

### In Action
* Expected Input
    * A collection of images of documents containing text in "RecognitionPrinted/dir_input directory"
        
* Expected Output
    * A collection of json files in the "OutputCompleteDocument".
    
* To clean the directories call

    ```
   ./clean_directories.sh
    ```
    
* To start transcribing call any of the following scripts

    ```
    ./extract_text.sh # includes applying rotations
    ./no_preprocessing_extract_text.sh # no rotation included
    ./debug_document.sh # clean directories, call the no_preprocessing script and the evaluation script 
    
    ```

* To evaluate the transcription call

   ```
    ./evaluate_transcription.sh
  ```
    
## Results

The results achieved with the system using the two nomination methods implemeted at the moment for 1539 documents

#### Rule based Nomination 

| Metric | Value % |
|:---|:---:|
| Levenshtein | 79.4 % |
| Precision | 70.2 % |
| Recall | 68.1 % |
| F1Score | 68.7 % |
| Fuzzy | 85.0 % |
| Fuzzy Token Sort | 81.4 % |


#### Sent2vec based Nomination 

| Metric | Value % |
|:---|:---:|
| Levenshtein | 77.2 % |
| Precision | 66.0 % |
| Recall | 67.3 % |
| F1Score | 66.5 % |
| Fuzzy | 83.0 % |
| Fuzzy Token Sort | 80.7 % | 
   
   
   


 
 # Citing TMIXT
 if you are using TMIXT or the MIXed-IAMDB labels please cite the following work:
 
> Fady Medhat, Mahnaz Mohammadi, Sardar Jaf, Chris G. Willcocks, Toby P. Breckon, Peter Matthews, Andrew Stephen McGough, Georgios Theodoropoulos and Boguslaw Obara
>
> **TMIXT: A process flow for Transcribing MIXed handwritten and machine-printed Text**, *IEEE International Conference on Big Data*, Big Data, 2018.
>
> <a href="https://arxiv.org/ftp/arxiv/papers/.pdf"><img src="https://img.shields.io/badge/download-.pdf-blue.svg" alt="download paper" title="download paper" align="right" /></a>
> [DOI: https://doi.org/10.1109/BigData.2018.8622136]
   


