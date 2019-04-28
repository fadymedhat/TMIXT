# Transcriber #

This plugin is for transcribing images of text lines. The pre-processor plugin should be called before using this plugin 
to slince an image of text of lines and apply the required image enhancements.

## Hint of flow
This section is only to give a hint of the flow of the Transcriber

The goal of this plugin is to transcribe text lines (slices of text), where each line is in a separate image. 
The generated output is a text file with the image name as the line label and the actual transcribed text in the rest of the line.


## Getting Started
The transcriber is based on the <a href="https://github.com/jpuigcerver/Laia">Laia library</a> for handwritten character 
recognition. The library uses Long Short-Term Memory (LSTM) [1], Connectionist Temporal Classification (CTC) [2] and Convolutional 
Neural Networks (CNN)[3].  

### Prerequisit
This module is tested on an Ubuntu 16.04 machine, Titan 1080ti with driver v378.13
   
   * GPU installed on the executing server.
   * Cuda 8.0
   * [docker](https://www.docker.com/)
   * [nvidia-docker](https://github.com/NVIDIA/nvidia-docker/releases)
   

###### Input data folder
This folder should have the following hierarchy inside:
 * images: this folder holds images of text lines
 * filelist: this folder should be empty and it will be used by the running script to store a text file holding the names of
             all the files in the images folder.
 * model: holds a pretrained model.
 * symbtable: contains a file with all the possible characters that could be detected.
                

###### Output data folder name

Holds a text files with the output transcribed text.


### Packaging and Execution

This module is packed as a Docker image (a virtual machine type of packing) on the docker public repository.
The provided script will pull and execute it given that the input and output directory are present in the working directory.


To start the whole process:
```
./transcribe.sh
```





### Expected Input
 * A collection of image files in the __"Input data folder"__/images .
### Expected Output
 * A text file in the __"Output data folder"__ containing the file name as a line label and the text transcription for that line .

## Authors
 * **Fady Medhat**
 
 
## Acknowlegdements
This module is based on the work of the developers of [Laia](https://github.com/jpuigcerver/Laia/tree/master/egs/iam)

## References

[1] S. Hochreiter and J. Schmidhuber, “Long Short-Term Memory,” Neural Computation, vol. 9, no. 8, pp. 1735-1780, 1997

[2] A.Graves,S.Fernández, F. Gomez, and J. Schmidhuber, “Connectionist Temporal Classification: Labelling Unsegmented
Sequence Data with Recurrent Neural Networks,” Proc. 23rd Int’l Conf. Machine Learning, pp. 369-376, 2006

[3] Y. LeCun, L. Bottou, Y. Bengio and P. Haffner: Gradient-Based Learning Applied to Document Recognition, Proceedings of the IEEE, 86(11):2278-2324, November 1998,
