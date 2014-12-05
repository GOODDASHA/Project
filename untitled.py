from Algorithms.PageRank import PageRankHandler
from Parser.datasetparser import DataSetParser
import os
import csv
import sys


def write_clean_file():
	dfs_input_name 			= 'filtered_output_of_all.csv'
	dfs_input_file 			= os.path.join(input_directory, dfs_input_name)
	wocao = set(open('idset.txt', 'rb').read().split('\n'))
	n = 0
	nima = open('wonima.txt', 'wb')

	for data in csv.DictReader(open(dfs_input_file)):
		n += 1

		if not n % 100000:
			print n
		_id = eval(data['dokid'])[0]
		_adjset = eval(data['refunifids'])

		_new_adjset = [x for x in _adjset if x in wocao]
		if not len(_new_adjset):
			continue
		nima.write(_id + '\t' + '-'.join(_new_adjset) + '\n')
	nima.close()





class DFSHandler():

    def __init__(self, filename, id_tag='dokid', ref_tag='refunifids', num=None):

    	
    	n = 0
        self._paper_undirected_graph = {}
        for data in open(filename):
            n += 1
            if not n%1000000:
                print n
            if n==100000:
				break
            # Build directed graph
            data = data.strip().split()
            _id = data[0]
            _adjset = {x for x in data[1].split('-')}
            for _other_id in _adjset:
                if _other_id in self._paper_undirected_graph:
                    self._paper_undirected_graph[_other_id].add(_id)
                else:
                    self._paper_undirected_graph[_other_id] = {_id}
            if _id in self._paper_undirected_graph:
                self._paper_undirected_graph[_id] = self._paper_undirected_graph[_id].union(_adjset)
            else:
                self._paper_undirected_graph[_id] = _adjset
        self._num = len(self._paper_undirected_graph)
        print self._num
        self._cluster = {}


    def execute(self):
        self._num_cluster = 0
        self._visited = {paper:-1 for paper in self._paper_undirected_graph}
        self._cluster = {}
        for _paper in self._paper_undirected_graph:
            if self._visited[_paper] == -1:
                self._num_cluster += 1
                self._cluster[self._num_cluster] = {_paper}
                self.DFS(_paper)
      	n = 0
        for x in self._cluster:
        	n += 1
        	if n < 10:
        		print x, self._cluster[x]
        	else:
        		break


    def DFS(self, _paper):
        self._visited[_paper] = 0
        for _ref in self._paper_undirected_graph[_paper]:
            if _ref == _paper:
                print _ref, " has a self citation, mlgb!"
                continue
            if self._visited[_ref] == -1:
                #print self._cluster
                self._cluster[self._num_cluster].add(_ref)
                self.DFS(_ref)
        self._visited[_paper] = 1


if __name__ == "__main__":
	input_name 				= "wocao.txt"
	input_directory         = "/Users/elvin/Desktop/Project_iofiles/Input"
	output_directory        = "/Users/elvin/Desktop/Project_iofiles/Output"

	#write_clean_file()
	#build_graph()

	dh = DFSHandler('wonima.txt')
	dh.execute()
	'''
	l = len(components)
	num_paper = 0
	largest_size = 0

	for sub in components:
		num_paper += len(sub)
		largest_size = max(len(sub), largest_size)

	print "total number of data read is :", num_of_paper_read
	print "number of unconnected cluster is :", l
	print "total number of paper involved( can be paper outside the data set ) is :", num_paper
	print "largest cluster size :", largest_size
	'''
    