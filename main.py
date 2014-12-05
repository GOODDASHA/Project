from Algorithms.PageRank import PageRankHandler
from Algorithms.DFS import DFSHandler
from Parser.datasetparser import DataSetParser
import os
import csv
import sys


def main_parser_test():
	input_name 				= "wocao.txt"
	input_file 				= os.path.join(input_directory, input_name)

	print "Input data file name is :", input_name
	print "Reading HTML file to string"
	dsParser                = DataSetParser(input_file)
	print "String has been read, parsing HTML to data set"
	dsParser.parse_HTML()
	print "Data set parsed, filtering tags"
	ds                      = dsParser.filtertags()


	attlist                 = ['dokid', 'editions', 'sortdate', 'asca', 'doctype',
                                'issn', 'authors', 'jabbrev', 'publisher', 'refunifids']
	
	output_name 			= 'filtered_output_of_' + input_name[:-4]+'.csv'
	output_file 			= os.path.join(output_directory, output_name)
	print "Writing output file to :", output_name

	dsParser.writeCsv(attlist, output_file)

	print "****************************"

	classification_output_name 	= 'classification_output_of_' + input_name[:-4]+'.csv'
	classification_output_file 	= os.path.join(output_directory, classification_output_name)
	dsParser.classifydata(classification_output_file)



	ss_output_name 			= 'subject_output_of_' + input_name[:-4]+'.txt'
	ss_output_file 			= os.path.join(output_directory, ss_output_name)
	print "Writing out all the subject"
	dsParser.writesubject(ss_output_file)

	
def main_pagerank_test():
	pr_input_name 			= 'filtered_output_of_' + input_name[:-4]+'.csv'
	pr_input_file 			= os.path.join(output_directory, pr_input_name)

	pr_output_name 			= 'pagerank_of_' + input_name[:-4]+'.csv'
	pr_output_file 			= os.path.join(output_directory, pr_output_name)

	pr = PageRankHandler(pr_input_file)
	ranks = pr.compute_ranks()
	pr.writeCsv(pr_output_file)

def main_dfs_test():

	dfs_input_name 			= 'pruned_filtered_output_of_all.csv'
	dfs_input_file 			= os.path.join(input_directory, dfs_input_name)
	sys.argv
	arg = sys.argv[1]
	num_of_paper_read = None if arg == 'all' else int(arg)
	#num_of_paper_read = None
	
	dfshandler = DFSHandler(dfs_input_file, num = num_of_paper_read)
	components = dfshandler.get_components()

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
	dfs_output_name 			= 'components.p'
	dfs_output_file 			= os.path.join(input_directory, dfs_output_name)	
	dfshandler.write_to_file(dfs_output_file)

	c = dfshandler.load_from_file(dfs_output_file)


def test():

	raw_data_filename = 'filtered_output_of_all.csv'
	dfshandler = DFSHandler(raw_data_filename)
	dfshandler.build_paper_graph()
	dfshandler.write_paper_components()

def test2():

	prhandler = PageRankHandler()
	prhandler.build_journal_graph()
	prhandler.compute_journal_pageranks()
	prhandler.write_journal_pageranks()


if __name__ == "__main__":
	

	test2()
    