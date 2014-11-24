import csv
import networkx as nx
import matplotlib.pyplot as plt
import pickle

class DFSHandler():
    def __init__(self, filename, id_tag='dokid', ref_tag='refunifids', num=None):
        self._undirected_graph =nx.Graph()

        n = 0
        for data in csv.DictReader(open(filename)):
            n += 1
            if n==num:
                break
            _id = eval(data['dokid'])[0]
            _adjset = eval(data['refunifids'])

            self._undirected_graph.add_node(_id)
            for _other_id in _adjset:
                self._undirected_graph.add_edge(_id, _other_id)
        self._components = sorted(nx.connected_components(self._undirected_graph), key = len, reverse=True)


    def get_components(self):
        return self._components

    def write_to_file(self, filename):
        pickle.dump(self._components,open(filename,'wb'))

    def load_from_file(self, filename):
        return pickle.load( open( filename, "rb" ) )


