from htmlparser import MyHTMLParser
import csv
class DataSetParser(MyHTMLParser):
    def __init__(self, filename):
        self.parser = MyHTMLParser()

        self.HTMLdata=open (filename, "rb").read().replace('\n', '')

    def parse_HTML(self):
        self.parser.feed(self.HTMLdata)
        self.dataset = self.parser.getdataset()

    def getdataset(self):
        return self.dataset

    def gettags(self):
        return self.parser.gettags()

    def classifydata(self, filename):
        self.buildsubjectset()

        with open(filename, "w") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['subject', 'dokid'])
            for subject in self.subjectset:
                for data in self.filtered_dataset:
                    temp = [x.strip() for x in data['asca']]
                    if subject in temp:
                        writer.writerow([subject, data['dokid'][0]])


    def buildsubjectset(self):
        self.subjectset = [x.strip() for x in self.parser.getsubject()]
        self.subjectset.sort()


    def writesubject(self, filename):
        self.buildsubjectset()
        with open(filename, "w") as text_file:
            for x in self.subjectset:
                text_file.write(x + '\n')

            text_file.close()

    def filtertags(self, tagname = 'refunifids'):
        self.filtered_dataset = [data for data in self.dataset if tagname in data]
        return self.filtered_dataset

    def writeCsv(self, attlist, output_filename):
        
        with open(output_filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(attlist)
            for line in self.filtered_dataset:
                data = []
                for att in attlist:
                    if att in line:
                        data.append(line[att])
                    else:
                        data.append('')
                writer.writerow(data)