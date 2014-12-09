import csv
import os
import networkx as nx
import operator


class PageRankHandler():
    def __init__(self, 
                input_filename = '_jounal_relation.txt',
                output_filename = 'journal_pageranks.txt',
                directory = '/Users/elvin/Desktop/Project_iofiles'):

        '''
        Constructor:initialize the object
        '''

        # input & intermediate & output filename
        self._input_filename = input_filename
        self._output_filename = output_filename

        # input & intermediate & output file directory
        self._directory = directory
        self._input_directory = self._directory + '/Input'
        self._output_directory = self._directory + '/Output'
        self._intermediate_directory = self._directory + '/Intermediate'

        # input & intermediate & output file 
        self._input_file = os.path.join(self._input_directory, self._input_filename)
        self._output_file = os.path.join(self._output_directory, self._output_filename)



    def build_graph(self, inverse=False):
        _graph = nx.DiGraph()
        with open(self._input_file, 'rb') as input_txtfile:
            for n, data in enumerate(input_txtfile):
                if not n%100000:
                    print "%d data read"%n
                data = data.strip().split('\t')
                _id_journal = data[0]
                _ref_journal = data[1].split('|')
                _graph.add_node(_id_journal)
                for _other_id in _ref_journal:
                    if _other_id not in _graph[_id_journal]:
                        if inverse:
                            _graph.add_edge(_other_id, _id_journal)
                        else:
                            _graph.add_edge(_id_journal, _other_id)
        print 'num of edges : ', _graph.number_of_edges()
        print 'num of nodes : ', len(_graph)
        return _graph

    def compute_pagerank(self, _graph, alpha, _personalization=None):
        print "computing"
        _pagerank = nx.pagerank_numpy(_graph, alpha=alpha, personalization=_personalization)
        _sorted_pagerank = sorted(_pagerank.items(), key=operator.itemgetter(1), reverse=True)
        _max = _sorted_pagerank[0][1]
        return _sorted_pagerank, _max

    def writing_pagerank(self, _file, _sorted_pagerank, _max):
        print "writing"
        with open(_file, 'wb') as output_txtfile:
            for _journal, _val in _sorted_pagerank:
                _line = _journal + '\t' + str(_val/_max) + '\n'
                output_txtfile.write(_line)
            output_txtfile.close()

    def page_rank(self):
        _graph = self.build_graph()
        _sorted_pagerank, _max = self.compute_pagerank(_graph, alpha)
        self.writing_pagerank(self._output_file, _sorted_pagerank, _max)        


class TrustRankHandler(PageRankHandler):

    def __init__(self,
                input_filename = 'journal_relation_from_2011_to_2013.csv',
                output_filename = 'journal_trustranks_from_2011_to_2013.txt',
                bad_paper_filename = 'Bad_paper_from_2011_to_2013.txt',
                intermediate_filename = 'seed_desirability_from_2011_to_2013.txt',
                directory = '/Users/elvin/Desktop/Project_iofiles'):

        PageRankHandler.__init__(self,
                                input_filename = input_filename,
                                output_filename = output_filename,
                                directory = directory)

        self._bad_paper_file = os.path.join(self._input_directory, bad_paper_filename)
        self._intermediate_file = os.path.join(self._intermediate_directory, intermediate_filename)

    def select_seed(self, alpha=0.9):
        '''
        Computer the desirability of paper to be selected. 
        Algorithm: Inverse PageRank
        '''
        self.inverse_pagerank(alpha)

    def inverse_pagerank(self, alpha):

        _graph = self.build_graph(inverse=True)
        _sorted_pagerank, _max = self.compute_pagerank(_graph, alpha)
        self.writing_pagerank(self._intermediate_file, _sorted_pagerank, _max)

    def initialize_vector(self, L):
        print "initializing"
        _bad_list = []
        _bad_set = set([x for x in open(self._bad_paper_file, 'r').read().split('\r')])
        _journal_list = [x.strip().split('\t')[0] for x in open(self._intermediate_file, 'r')]
        _truncated_journal_list = _journal_list[:L]
        _journal_dict = {x:0 for x in _journal_list}
        n = 0.
        for i in range(L):
            _journal = _truncated_journal_list[i]
            if  _journal not in _bad_set:
                n += 1
                _journal_dict[_journal] = 1
        for _journal in _journal_dict:
            _journal_dict[_journal] /= n
        return _journal_dict

    def trust_rank(self, L=1000, alpha=0.9):
        _journal_dict = self.initialize_vector(1000)
        _graph = self.build_graph()
        _sorted_pagerank, _max = self.compute_pagerank(_graph, 0.9, _personalization=_journal_dict)
        self.writing_pagerank(self._output_file, _sorted_pagerank, _max)





 

        



