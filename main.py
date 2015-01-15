from Algorithms.RankBox import PageRankHandler, TrustRankHandler
from Algorithms.DFS import DFSHandler
from Parser.datasetparser import DataSetParser
import os
import csv
import sys
import gc







class Data_Preprocess():

    def build_dataset(self, start, end):
		_time_splited_filename = '_date_splited_data.csv'
		_directory = '/Users/elvin/Desktop/Project_iofiles/Output/Date_splited_data'
		_output_filename = 'date_from_%d_to_%d.csv'%(start, end)
		_output_file = os.path.join(_directory, _output_filename)
		header = open('header.txt', 'rb').read().split('\n')
		with open(_output_file, 'wb') as output_csvfile:

			writer = csv.writer(output_csvfile, delimiter=',')
			writer.writerow(header)
			for _year in range(start, end+1):
				_filename = str(_year)+_time_splited_filename
				_file = os.path.join(_directory, _filename)
				print _filename
				with open(_file, 'rb') as input_txtfile:

					dr = csv.DictReader(input_txtfile)
					for line in dr:
						writer.writerow([line[f] for f in header])


    def write_paper_id(self, _idset_file, _rawinput_file):

    	_id_tag='dokid'
        print 'writing id set to a txt file'
        N = 0
        with open(_idset_file, 'wb') as output_txtfile:
            with open(_rawinput_file, 'rb') as input_csvfile:
                _dr = csv.DictReader(input_csvfile)
                for data in _dr:
                    N += 1
                    if not N%100000:
                		print N
                    _id = eval(data[_id_tag])[0]
                    output_txtfile.write(_id + '\n')
            output_txtfile.close()

    def prune_dataset(self, _idset_file, _pruned_file, _rawinput_file):
        '''
        prune all the refs paper which are not in the paper set
        '''
        _id_tag='dokid'
        _ref_tag='refunifids' 
        _idset = set(open(_idset_file, 'rb').read().split('\n'))

        print "start pruning data"
        with open(_pruned_file, 'wb') as output_txtfile:
            with open(_rawinput_file, 'rb') as input_csvfile:
                _dr = csv.DictReader(input_csvfile)
                N = 0
                for data in _dr:
                    N += 1
                    if not N%100000:
                        print N
                    _id = eval(data[_id_tag])[0]
                    _adjset = eval(data[_ref_tag])
                    _new_adjset = [x for x in _adjset if x in _idset]
                    if not len(_new_adjset):
                        continue
                    line = _id + '\t' + '|'.join(_new_adjset) + '\n'
                    output_txtfile.write(line)
            output_txtfile.close()


    def write_paper_journal(self, _id_jounal_file, _rawinput_file):
        '''
        write id and the journal it belongs to a txt file
        '''
        _id_tag='dokid'
        _ref_tag='refunifids'
        _journal_tag = 'jabbrev'
        with open(_id_jounal_file, 'wb') as output_txtfile:
            with open(_rawinput_file, 'rb') as input_csvfile:
            	n = 0
                _dr = csv.DictReader(input_csvfile)
                for data in _dr:
                    n += 1
                    if not n%100000:
                		print n
                    _id = eval(data[_id_tag])[0]
                    _journal = eval(data[_journal_tag])[0]
                    output_txtfile.write(str(_id) + '\t' + _journal + '\n')
            output_txtfile.close()
    
    def merge_journal(self, _id_jounal_file, _journal_relation_file, _pruned_file):
        '''
        merge papers into journals and keep their relation
        '''
        print "building journal dict"
        _id_journal_dict = {}
        with open(_id_jounal_file, 'rb') as input_txtfile:
            for data in input_txtfile:
                data = data.strip().split('\t')
                _id = data[0]
                _journal = data[1]
                _id_journal_dict[_id] = _journal

        print "merging journal"
        with open(_journal_relation_file, 'wb') as output_txtfile:
            with open(_pruned_file, 'rb') as input_txtfile:
                for data in input_txtfile:
                    data = data.strip().split('\t')
                    _id = data[0]
                    _refs = data[1].split('|')
                    _id_journal = _id_journal_dict[_id]
                    _refs_jounal = list(set([_id_journal_dict[ref] for ref in _refs if ref in _id_journal_dict]))
                    line = _id_journal + '\t' + '|'.join(_refs_jounal) + '\n'
                    output_txtfile.write(line)
            output_txtfile.close()

	



def test_trustrank():

	trhandler = TrustRankHandler()
#	trhandler.select_seed()
	trhandler.trust_rank()

def preprocess(start, end):
    dp = Data_Preprocess()
    #dp.build_dataset(start, end)
    
    _idset_filename = 'idset_from_%d_to_%d.txt'%(start, end)
    _intermediate_directory = '/Users/elvin/Desktop/Project_iofiles/Intermediate'
    _idset_file = os.path.join(_intermediate_directory, _idset_filename)


    _rawinput_filename = 'date_from_%d_to_%d.csv'%(start, end)
    _output_directory = '/Users/elvin/Desktop/Project_iofiles/Output/Date_splited_data'

    _rawinput_file = os.path.join(_output_directory, _rawinput_filename)

    _pruned_filename = 'pruned_date_from_%d_to_%d.csv'%(start, end)
    _pruned_file = os.path.join(_intermediate_directory, _pruned_filename)

#    dp.write_paper_id(_idset_file, _rawinput_file)
#    dp.prune_dataset(_idset_file, _pruned_file, _rawinput_file)

    _id_jounal_file = 'id_journal_from_%d_to_%d.csv'%(start, end)
    _intermediate_directory = '/Users/elvin/Desktop/Project_iofiles/Intermediate'
    _idset_file = os.path.join(_intermediate_directory, _id_jounal_file)

    _journal_relation_filename = 'journal_relation_from_%d_to_%d.csv'%(start, end)
    _journal_relation_file = os.path.join(_intermediate_directory, _journal_relation_filename)

    dp.write_paper_journal(_idset_file, _rawinput_file)
    dp.merge_journal(_idset_file, _journal_relation_file, _pruned_file)



def split():

    raw_data_filename = 'filtered_output_of_all.csv'
    dfshandler = DFSHandler(raw_data_filename)
    dfshandler.build_journal_graph()

def dfs():
    dfshandler = DFSHandler()
    dfshandler.build_journal_graph()

if __name__ == "__main__":
    
    dfs()
    '''
    print "Spliting data"
    #dfshandler = DFSHandler()
    #dfshandler.split_by_date()
    for year in range(2008, 2011):
        print "Preprocessing data"
    	#preprocess(year, year+2)


    print "computing trust_rank"
    for year in range(2010, 2011):
        print 'year from %d to %d'%(year, year+2)
        trhandler = TrustRankHandler(year, year+2)
        trhandler.trust_rank()
    '''










'''

'''
    