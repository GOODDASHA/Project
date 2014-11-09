
class Document(object):
    """ Used both for learning (training) documents 
    and for testing documents. The optional parameter 
    lear has to be set to True, if a classificator 
    should be trained. If it is a test document 
    learn has to be set to False. """
    _vocabulary = BagOfWords()
 
    def __init__(self, vocabulary):
        self.__name = ""
        self.__document_class = None
        self._words_and_freq = BagOfWords()
        Document._vocabulary = vocabulary
    
    def read_document(self,filename, learn=False):
        """ A document is read. It is assumed, 
        that the document is either encoded 
        in utf-8 or in iso-8859... (latin-1).
        The words of the document are stored in 
        a Bag of Words, i.e. self._words_and_freq = BagOfWords() """
        try:
            text = open(filename,"r", encoding='utf-8').read()
        except UnicodeDecodeError:
            text = open(filename,"r", encoding='latin-1').read()
        text = text.lower()
        words = re.split("[^\wäöüÄÖÜß]*",text)

        self._number_of_words = 0
        for word in words:
            self._words_and_freq.add_word(word)
            if learn:
                Document._vocabulary.add_word(word)


    def __add__(self,other):
        """ Overloading the "+" operator. Adding two documents consists in adding the BagOfWords of the Documents """
        res = Document(Document._vocabulary)
        res._words_and_freq = self._words_and_freq + other._words_and_freq    
        return res
    
    def vocabulary_length(self):
        """ Returning the length of the vocabulary """
        return len(Document._vocabulary)
                
    def WordsAndFreq(self):
        """ Returning the dictionary, containing the words (keys) with their frequency (values) as contained
        in the BagOfWords attribute of the document"""
        return self._words_and_freq.BagOfWords()
        
    def Words(self):
        """ Returning the words of the Document object """
        d =  self._words_and_freq.BagOfWords()
        return d.keys()
    
    def WordFreq(self,word):
        """ Returning the number of times the word "word" appeared in the document """
        bow =  self._words_and_freq.BagOfWords()
        if word in bow:
            return bow[word]
        else:
            return 0
                
    def __and__(self, other):
        """ Intersection of two documents. A list of words occuring in both documents is returned """
        intersection = []
        words1 = self.Words()
        for word in other.Words():
            if word in words1:
                intersection += [word]
        return intersection
