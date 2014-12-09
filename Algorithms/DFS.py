import csv
import networkx as nx
import matplotlib.pyplot as plt
import pickle
import os


class DFSHandler():
    def __init__(self, filename, 
                id_tag='dokid', 
                ref_tag='refunifids', 
                journal_tag = 'jabbrev',
                date_tag = 'sortdate',
                num=None,
                rawdata_filename = 'filtered_output_of_all.csv',
                idset_filename = 'id.txt',
                header_filename = 'header.txt',
                id_jounal_filename = 'id_journal.txt',
                data_splited_filename = '_date_splited_data.csv',
                journal_relation_filename = '_jounal_relation.txt',
                directory = '/Users/elvin/Desktop/Project_iofiles'):

        '''
        Constructor:initialize the object
        '''
        # Attributes of the data file
        self._filename = filename
        self._maxmum = num

        # tags
        self._id_tag = id_tag
        self._ref_tag = ref_tag
        self._journal_tag = journal_tag
        self._date_tag = date_tag

        # unconnected components
        self._paper_components = None
        self._journal_components = None
        self._subject_components = None

        # graph structure
        self._paper_undirected_graph = None
        self._journal_undirected_graph = None
        self._subject_undirected_graph = None

        # input & intermediate & output filename
        self._rawdata_filename = rawdata_filename
        self._idset_filename = idset_filename
        self._header_filename = header_filename
        self._id_jounal_filename = id_jounal_filename
        self._pruned_filename = 'pruned_' + self._rawdata_filename[:-4] + '.txt'
        self._journal_relation_filename = journal_relation_filename
        self._data_splited_filename = data_splited_filename

        # input & intermediate & output file directory
        self._directory = directory
        self._input_directory = self._directory + '/Input'
        self._output_directory = self._directory + '/Output'
        self._other_directory = self._directory + '/Intermediate'
        self._journal_components_directory = self._output_directory+'/Components/Journal_components'
        self._paper_components_directory = self._output_directory+'/Components/Paper_components'
        self._data_splited_directory = self._output_directory+'/Date_splited_data'

        # input & intermediate & output file 
        self._idset_file = os.path.join(self._other_directory, self._idset_filename)
        self._rawinput_file = os.path.join(self._input_directory, self._rawdata_filename)
        self._header_file = os.path.join(self._other_directory, self._header_filename)
        self._pruned_file = os.path.join(self._other_directory, self._pruned_filename)
        self._id_jounal_file = os.path.join(self._other_directory, self._id_jounal_filename)
        self._journal_relation_file = os.path.join(self._other_directory, self._journal_relation_filename)

        self._header = [h.strip() for h in open(self._header_file, 'rb')]
        print self._header
    def split_by_date(self):
        '''
        split the data w.r.t. dates and write to separate files every two years 
        '''

        _splited_data = {i:[] for i in range(2008,2014)}
        with open(self._rawinput_file, 'rb') as input_csvfile:
                _dr = csv.DictReader(input_csvfile)
                n = 0
                for data in _dr:
                    n += 1
                    if not n%100000:
                        print n
                    _year = int(eval(data[self._date_tag])[0][:4])

                    _splited_data[_year].append(data)
        print "writing" 
        N = 0
        for i in _splited_data:
            _data_splited_filename = str(i) + self._data_splited_filename
            _data_splited_file = os.path.join(self._data_splited_directory, 
                                                   _data_splited_filename)
            with open(_data_splited_file, 'wb') as output_csvfile:
                writer = csv.writer(output_csvfile, delimiter=',')
                writer.writerow(self._header)
                for _data in _splited_data[i]:
                    N+=1
                    if not N%100000:
                        print N
                    _line = [_data[f] for f in self._header]
                    writer.writerow(_line)



    def write_paper_id(self):
        '''
        Output all the paper id and write them to a txt file.
        '''
        print 'writing id set to a txt file'
        with open(self._idset_file, 'wb') as output_txtfile:
            with open(self._rawinput_file, 'rb') as input_csvfile:
                _dr = csv.DictReader(input_csvfile)
                for data in _dr:
                    _id = eval(data[self._id_tag])[0]
                    output_txtfile.write(_id + '\n')
            output_txtfile.close()

    def prune_dataset(self):
        '''
        prune all the refs paper which are not in the paper set
        '''
        _idset = set(open(self._idset_file, 'rb').read().split('\n'))

        print "start pruning data"
        with open(self._pruned_file, 'wb') as output_txtfile:
            with open(self._rawinput_file, 'rb') as input_csvfile:
                _dr = csv.DictReader(input_csvfile)
                for data in _dr:
                    _id = eval(data[self._id_tag])[0]
                    _adjset = eval(data[self._ref_tag])
                    _new_adjset = [x for x in _adjset if x in _idset]
                    if not len(_new_adjset):
                        continue
                    line = _id + '\t' + '|'.join(_new_adjset) + '\n'
                    output_txtfile.write(line)
            output_txtfile.close()

    def write_paper_journal(self):
        '''
        write id and the journal it belongs to a txt file
        '''
        with open(self._id_jounal_file, 'wb') as output_txtfile:
            with open(self._rawinput_file, 'rb') as input_csvfile:
                _dr = csv.DictReader(input_csvfile)
                for data in _dr:
                    _id = eval(data[self._id_tag])[0]
                    _journal = eval(data[self._journal_tag])[0]
                    output_txtfile.write(str(_id) + '\t' + _journal + '\n')
            output_txtfile.close()
    
    def merge_journal(self):
        '''
        merge papers into journals and keep their relation
        '''
        print "building journal dict"
        _id_journal_dict = {}
        with open(self._id_jounal_file, 'rb') as input_txtfile:
            for data in input_txtfile:
                data = data.strip().split('\t')
                _id = data[0]
                _journal = data[1]
                _id_journal_dict[_id] = _journal

        print "merging journal"
        with open(self._journal_relation_file, 'wb') as output_txtfile:
            with open(self._pruned_file, 'rb') as input_txtfile:
                for data in input_txtfile:
                    data = data.strip().split('\t')
                    _id = data[0]
                    _refs = data[1].split('|')
                    _id_journal = _id_journal_dict[_id]
                    _refs_jounal = list(set([_id_journal_dict[ref] for ref in _refs if ref in _id_journal_dict]))
                    line = _id_journal + '\t' + '|'.join(_refs_jounal) + '\n'
                    output_txtfile.write(line)
            output_txtfile.close()

    

    def build_journal_graph(self):
        '''
        get connected components wrt journal
        '''
        self._journal_undirected_graph = nx.Graph()

        n = 0
        with open(self._journal_relation_file, 'rb') as input_txtfile:
            for data in input_txtfile:
                n += 1
                if n == self._maxmum:
                    break
                if n % 100000 == 0:
                    print "%d data read"%n
                data = data.strip().split('\t')
                _id_journal = data[0]
                _ref_journal = data[1].split('|')
                for _other_id in _ref_journal:
                    self._journal_undirected_graph.add_edge(_id_journal, _other_id)

        self._journal_components = sorted(nx.connected_components(self._journal_undirected_graph), key = len, reverse=True)


    def write_journal_components(self):
        '''
        write different components to different txt file
        '''
        _components_file_name = '_jounal_component.txt'
        for i, _component in enumerate(self._journal_components):
            _journal_component_file = os.path.join(self._journal_components_directory, 
                                                    str(i) + _components_file_name)
            with open(_journal_component_file, 'wb') as output_txtfile:
                for data in _component:
                    output_txtfile.write(data+'\n')
                output_txtfile.close()

    def build_paper_graph(self):
        '''
        get connected components wrt paper
        '''
        self._paper_undirected_graph = nx.Graph()
        n = 0
        with open(self._pruned_file, 'rb') as input_txtfile:
            for data in input_txtfile:
                n += 1
                if n==self._maxmum:
                    break
                if n % 100000 == 0:
                    print "%d data read"%n
                data = data.strip().split('\t')
                _id = data[0]
                _adjset = data[1].split('|')
                if _id not in self._paper_undirected_graph:
                    self._paper_undirected_graph.add_node(_id)
                for _other_id in _adjset:
                    if _other_id not in self._paper_undirected_graph[_id]:
                        self._paper_undirected_graph.add_edge(_id, _other_id)
        self._paper_components = sorted(nx.connected_components(self._paper_undirected_graph), key = len, reverse=True)
    
    def write_paper_components(self):
        '''
        write different components to different txt file
        '''
        _components_file_name = '_paper_component.txt'
        for i, _component in enumerate(self._paper_components):

            _paper_component_file = os.path.join(self._paper_components_directory, 
                                                    str(i) + _components_file_name)
            with open(_paper_component_file, 'wb') as output_txtfile:
                for data in _component:
                    output_txtfile.write(data+'\n')
                output_txtfile.close()

    def get_journal_components(self):
        return self._journal_components



    def build_subject_graph(self):
        pass


    def build_subject_graph(self):
        '''
        get connected components wrt subject
        '''
        pass


'''
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_edges_from(
    [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
     ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])

val_map = {'A': 1.0,
           'D': 0.5714285714285714,
           'H': 0.0}

values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
red_edges = [('A', 'C'), ('E', 'C')]
edge_colours = ['black' if not edge in red_edges else 'red'
                for edge in G.edges()]
black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color = values)
nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
plt.show()
'''