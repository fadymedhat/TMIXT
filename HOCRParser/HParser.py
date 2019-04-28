import codecs

from HTMLParser import HTMLParser


# the following class parses the HOCR html file
# there are three functions that are called whenever an opening/closing/data tags are captured.

class HParser(HTMLParser):
    """
    HOCR file parser, generartes a dictionary of lines and their words together with the
    Bounding box used.
    """


    def __init__(self):
        HTMLParser.__init__(self)
        self.line_index = -1
        self.line_word_map = {}

        # a flag to show that a word has been captured
        self.is_word_flag = False


    def handle_starttag(self, tag, attrs):
        """

        :param tag:
        :param attrs:
        :return:
        """
        if tag == "span":
            attrs_dictionary = dict(attrs)
            if attrs_dictionary['class'] == 'ocr_line':
                #print("line        ", self.line_index)
                self.line_index += 1

            if attrs_dictionary['class'] == 'ocrx_word':
                self.is_word_flag = True
                bounding_box = str(attrs_dictionary['title']).split(';')[0].replace('bbox ', '')
                # initialize the first element of the list if the key is not there yet
                if self.line_index not in self.line_word_map.keys():
                    self.line_word_map[self.line_index] = []

                self.line_word_map[self.line_index].append(bounding_box)# = [self.line_box_map[self.line_index],]
    def handle_endtag(self, tag):
        """

        :param tag:
        :return:
        """
        end_tag = "implement this function to handle closing tags"

    def handle_data(self, data):
        """

        :param data:
        :return:
        """
        if bool(self.line_word_map) and self.is_word_flag == True:
            self.is_word_flag = False

            line_words = self.line_word_map[self.line_index]
            last_element = line_words[-1]
            line_words[-1] = {data.decode('utf-8') : last_element}
            #print("last element ",last_element, "   ", data)

    def retrieve_printed_transcription_map(self, file_path):
        """

        :param file_path:
        :return:
        """
        f = codecs.open(file_path, 'r')
        html_page = f.read()
        # remove any useless symbols
        html_page = html_page.replace('<strong>', '').replace('</strong>', '').replace('<em>', '').replace('</em>', '')
        # start parsing the page
        self.feed(html_page)

        self.remove_empty_lines()


    def remove_empty_lines(self):
        """
        remove empty lines from the dictionary of line-word map
        :param line_word_map:
        :return:
        """
        new_line_word_map = {}
        new_line_index = -1
        for line_id, words in self.line_word_map.iteritems():
            # print(line_id, words)
            new_line = []
            for word_box_item in words:
                if not word_box_item.keys()[0].strip() == '':
                    new_line.append(word_box_item)

            if len(new_line) > 0:
                new_line_word_map[new_line_index] = new_line
                new_line_index += 1

        # remove the first line of the page containing the word sentence, Database and writer id
        del (new_line_word_map[-1])
        self.line_word_map = new_line_word_map
        #return new_line_word_map