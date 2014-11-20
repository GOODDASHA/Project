from Algorithms.PageRank import PageRankHandler
from Algorithms.DFS import DFSHandler
from Parser.datasetparser import DataSetParser
import os
import csv



def main():
	input_name 				= "wocao.txt"

	output_directory        = "/Users/elvin/Desktop/Project_iofiles/Output"
	output_name 			= 'filtered_output_of_' + input_name[:-4]+'.csv'
	output_file 			= os.path.join(output_directory, output_name)


	dfshandler = DFSHandler(output_file)
	dfshandler.execute()
	dfshandler.get_cluster()
	dfshandler.check()






def main2():
	input_directory         = "/Users/elvin/Desktop/Project_iofiles/Input"
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
	
	output_directory        = "/Users/elvin/Desktop/Project_iofiles/Output"
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

	pr_output_name 			= 'pagerank_of_' + input_name[:-4]+'.csv'
	pr_output_file 			= os.path.join(output_directory, pr_output_name)

	pr = PageRankHandler(output_file)
	ranks = pr.compute_ranks()
	pr.writeCsv(pr_output_file)

if __name__ == "__main__":
	main2()
    