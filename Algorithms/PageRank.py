import csv
import os
import networkx as nx

class PageRankHandler():
    def __init__(self, 
                id_tag='dokid', 
                ref_tag='refunifids', 
                journal_tag = 'jabbrev',
                num=None,
                pruned_filename = 'pruned_filtered_output_of_all.txt',
                journal_relation_filename = '_jounal_relation.txt',
                journal_pagerank_filename = 'journal_pageranks.txt',
                directory = '/Users/elvin/Desktop/Project_iofiles'):

        '''
        Constructor:initialize the object
        '''
        # Attributes of the data file
        self._id_tag = id_tag
        self._ref_tag = ref_tag
        self._journal_tag = journal_tag
        self._maxmum = num

        # page ranks
        self._journal_pagerank = None

        # graph structure
        self._paper_undirected_graph = None
        self._journal_undirected_graph = None
        self._subject_undirected_graph = None

        # input & intermediate & output filename
        self._pruned_filename = pruned_filename
        self._journal_relation_filename = journal_relation_filename
        self._journal_pagerank_filename = journal_pagerank_filename

        # input & intermediate & output file directory
        self._directory = directory
        self._input_directory = self._directory + '/Input'
        self._output_directory = self._directory + '/Output'
        self._other_directory = self._directory + '/Other'

        # input & intermediate & output file 
        self._pruned_file = os.path.join(self._other_directory, self._pruned_filename)
        self._journal_relation_file = os.path.join(self._other_directory, self._journal_relation_filename)
        self._journal_pagerank_file = os.path.join(self._other_directory, self._journal_pagerank_filename)



    
    def build_journal_graph(self):
        self._journal_undirected_graph = nx.DiGraph()
        print 'building graph'
        with open(self._journal_relation_file, 'rb') as input_txtfile:
            n = 0
            for data in input_txtfile:
                n += 1
                if not n%100000:
                    print n
                data = data.strip().split('\t')
                _id_journal = data[0]
                _ref_journal = data[1].split('|')
                self._journal_undirected_graph.add_node(_id_journal)
                for _other_id in _ref_journal:
                    if _other_id not in self._journal_undirected_graph[_id_journal]:
                        self._journal_undirected_graph.add_edge(_id_journal, _other_id)
        print 'num of edges : 'self._journal_undirected_graph.number_of_edges()
        print 'num of nodes : 'len(self._journal_undirected_graph)

    def compute_journal_pageranks(self):
        print 'computing page rank'
        self._journal_pagerank = nx.pagerank(self._journal_undirected_graph, alpha=0.9, max_iter = 5)

    def write_journal_pageranks(self):
        print 'writing page rank'
        with open(self._journal_pagerank_file, 'wb') as output_txtfile:
            for _journal in self._journal_pagerank:
                _line = _journal + '\t' + self._journal_pagerank[_journal] + '\n'
                output_txtfile.write(_line)

            output_txtfile.close()

'''    

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

'''
