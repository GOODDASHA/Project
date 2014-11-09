__author__ = "Mao Li"

import re

class BagOfWords(object):
    def __init__(self, filename):
        self._filename = filename
        self._bag_of_words = {}
        self._number_of_words = 0

    def BuildBag(self,file):
        with open(self._filename, 'r') as f:
            for line in f:
                line = [w for w in re.split('\W', unicode(line, errors='ignore')) if w]
                self._number_of_words += len(line)
                for word in line:
                    word = word.lower()
                    if word in self._bag_of_words:
                        self._bag_of_words[word] = self._bag_of_words[word] + 1
                    else:
                        self._bag_of_words[word] = 1
    
    def vocabulary_length(self):
        """ Returning the length of the vocabulary """
        return len(_bag_of_words)
                
    def WordsDictionary(self):
        """ Returning the dictionary"""
        return self._bag_of_words
        
    def Words(self):
        """Returning the words of the Document object"""
        return self._bag_of_words.keys()
    
    def WordFreq(self,word):
        """ Returning the number of times the word "word" appeared in the document """
        if word in self._bag_of_words:
            return self._bag_of_words[word]
        else:
            return 0

    def __add__(self,anotherbag):
        """ Overloading the "+" operator. Adding two documents consists in adding the BagOfWords of the Documents """
        
        for x in anotherbag.WordsDictionary():
            if x in self._bag_of_words:
                self._bag_of_words[x] += anotherbag.WordsDictionary()[x]
            else:
                self._bag_of_words[x] = anotherbag.WordsDictionary()[x]
        return self

if __name__ == "__main__":
    b  = BagOfWords("wocao.txt")
    b.BuildBag()

    print b.WordFreq("limited")
'''       
    def __and__(self, other):
        """ Intersection of two documents. A list of words occuring in both documents is returned """
        intersection = []
        words1 = self.Words()
        for word in other.Words():
            if word in words1:
                intersection += [word]
        return intersection

    

'''