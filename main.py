from PageRank.pagerank import PageRankComputer
from DsReader.dsReader import DataSetParser
import os

if __name__ == "__main__":
	input_directory         = "/Users/elvin/Desktop/Project_iofiles/Input"
	input_name 				= "wocao.txt"
	input_file 				= os.path.join(input_directory, input_name)

	output_directory        = "/Users/elvin/Desktop/Project_iofiles/Output"
	output_name 			= 'filtered_output_of_' + input_name[:-4]+'.csv'
	output_file 			= os.path.join(output_directory, output_name)


	pr_output_name 			= 'pagerank_of_' + input_name[:-4]+'.csv'
	pr_output_file 			= os.path.join(output_directory, pr_output_name)


	print "Input data file name is :", input_name
	print "Reading HTML file to string"
	dsParser                = DataSetParser(input_file)
	print "String has been read, parsing HTML to data set"
	dsParser.parse_HTML()
	print "Data set parsed, filtering tags"
	ds                      = dsParser.filtertags()

	attlist                 = ['dokid', 'editions', 'sortdate', 'asca', 'doctype',
                                'issn', 'authors', 'jabbrev', 'publisher', 'refunifids']
	
	print "Writing output file to :", output_name
	dsParser.writeCsv(attlist, output_file)

	pr = PageRankComputer(output_file)
	ranks = pr.compute_ranks()
	pr.writeCsv(pr_output_file)


    