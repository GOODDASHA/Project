class BagOfWords(object):
    """ Implementing a bag of words, words corresponding with their frequency of usages in a "document"
    for usage by the Document class, DocumentClass class and the Pool class."""
    
    def __init__(self):
        self.__number_of_words = 0
        self.__bag_of_words = {}
        
    def __add__(self,other):
        """ Overloading of the "+" operator to join two BagOfWords """
        erg = BagOfWords()
        sum = erg.__bag_of_words
        for key in self.__bag_of_words:
            sum[key] = self.__bag_of_words[key]
            if key in other.__bag_of_words:
                sum[key] += other.__bag_of_words[key]
        for key in other.__bag_of_words:
            if key not in sum:
                sum[key] = other.__bag_of_words[key]
        return erg
        
    def add_word(self,word):
        """ A word is added in the dictionary __bag_of_words"""
        self.__number_of_words += 1
        if word in self.__bag_of_words:
            self.__bag_of_words[word] += 1
        else:
            self.__bag_of_words[word] = 1
    
    def len(self):
        """ Returning the number of different words of an object """
        return len(self.__bag_of_words)
    
    def Words(self):
        """ Returning a list of the words contained in the object """
        return self.__bag_of_words.keys()
    
        
    def BagOfWords(self):
        """ Returning the dictionary, containing the words (keys) with their frequency (values)"""
        return self.__bag_of_words
        
    def WordFreq(self,word):
        """ Returning the frequency of a word """
        if word in self.__bag_of_words:
            return self.__bag_of_words[word]
        else:
            return 0


def main():
	filename = "wocao.txt"

	print '\\'
		



if __name__ == "__main__":
	main()

