import re
import nltk
from nltk import PunktSentenceTokenizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize


class Tokenizer():

    def tokenize_to_sentences(self, paragraph):
        tokenizer = PunktSentenceTokenizer()
        sentences = tokenizer.tokenize(paragraph)
        return sentences

    def tokenize_to_sentences_punk(self, paragraph):
        tokenizer = PunktSentenceTokenizer()
        sentences = tokenizer.tokenize(paragraph)
        return sentences

    def tokenize_to_sentences_nltk(self, paragraph):
        sentences = sent_tokenize(paragraph)
        return sentences


    def tokenize_to_sentences_regex(self, paragraph):
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
        return sentences


    def tokenize_to_words(self, paragraph):
        tokenizer = RegexpTokenizer(r'\w+')
        words= tokenizer.tokenize(paragraph)
        return words


    def tokenize_to_words_nltk(self, paragraph):
        words=  nltk.word_tokenize(paragraph.decode('utf-8'))
        return words


