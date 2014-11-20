import csv
from HTMLParser import HTMLParser
from sets import Set



class MyHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.size = 0
        self.taglset = Set()
        self.dataset = []
        self.currenttag = None
        self.editionset = Set()
        self.doctypeset = Set()
        self.ascaset = Set()
    def handle_starttag(self, tag, attrs):
        if tag == 'REC':
            print self.size
            self.size += 1
        self.taglset.add(tag)
        self.currenttag = tag
    def handle_endtag(self, tag):
        self.taglset.add(tag)
    def handle_data(self, data):
        if self.currenttag == 'dokid':

            self.dataset.append({'dokid':data})
        elif self.currenttag == 'doctype':
            if '|' in data:
                for x in data.split('|'):
                    self.doctypeset.add(x)
        elif self.currenttag == 'asca':
            if '|' in data:
                for x in data.split('|'):
                    self.ascaset.add(x)       
        elif self.currenttag == 'editions':
            if '|' in data:
                for x in data.split('|'):
                    self.editionset.add(x)          

        if self.currenttag == 'rec':
            return 
        
        data = data.strip()
        self.dataset[len(self.dataset)-1][self.currenttag] = data.split('|')# if '|' in data else data


    def getsize(self):
        return self.size
    def getsubject(self):
        return self.ascaset
    def gettags(self):
        return self.taglset
    def getdataset(self):
        #print self.doctypeset
        #print self.editionset
        return self.dataset