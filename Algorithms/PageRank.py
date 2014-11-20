import csv
class PageRankHandler():

    def __init__(self, filename, id_tag='dokid', ref_tag='refunifids'):
        self._paperset = {eval(data[id_tag])[0]:eval(data[ref_tag])
        				for data in csv.DictReader(open(filename))}

        self._num = len(self._paperset)

    def initialize_ranks(self):

    	self._ranks = {}
    	for paper in self._paperset:
    		self._ranks[paper] = 1.0/self._num



    def compute_ranks(self, num_loops = 10, damping_factor = 0.8):

    	self.initialize_ranks()
    	for i in range(num_loops):
    		newranks = {}

    		for paper in self._paperset:
    			newrank = (1 - damping_factor)/self._num

    			for other_paper in self._paperset:
    				if paper in self._paperset[other_paper]:
    					newrank = newrank + damping_factor * (self._ranks[other_paper]/len(self._paperset[other_paper]))

    			newranks[paper] = newrank


    		self._ranks = newranks
    	return self._ranks
   
    def writeCsv(self, output_filename):
        with open(output_filename, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['dokid', 'rank'])
            for paper, rank in self._ranks.items():
                writer.writerow([paper, rank]) 
