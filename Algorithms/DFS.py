import csv



class DFSHandler():

    def __init__(self, filename, id_tag='dokid', ref_tag='refunifids', num=None):
        self._paper_undirected_graph = {}
        n = 0
        self._start = None
        for data in csv.DictReader(open(filename)):
            n += 1

            if num != None and n==num:
                break

            # Build directed graph
            _id = eval(data['dokid'])[0]
            _adjset = {x for x in eval(data['refunifids'])}

            if self._start == None:
                self._start = _id
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
        self._cluster = {}

    def find(self, paperid):
        try:
            return _paper_undirected_graph[paperid]
        except:
            return "Nothing Found"
    def execute(self):
        self._num_cluster = 0
        self._visited = {paper:-1 for paper in self._paper_undirected_graph}
        self._cluster = {}
        for _paper in self._paper_undirected_graph:

            if self._visited[_paper] == -1:
                self._num_cluster += 1

                self._cluster[self._num_cluster] = {_paper}
                self.DFS(_paper)


    def DFS(self, _paper):
        self._visited[_paper] = 0
        for _ref in self._paper_undirected_graph[_paper]:
            if _ref == _paper:
                print _ref, " has a self citation, mlgb!"
            if self._visited[_ref] == -1:
                #print self._cluster
                self._cluster[self._num_cluster].add(_ref)
                self.DFS(_ref)
        self._visited[_paper] = 1

    def get_cluster(self):

        return self._cluster, self._visited, self._paper_undirected_graph

    def check(self):
        for x,v  in self._paper_undirected_graph.items():
            for r in v:
                if r in self._paper_undirected_graph:
                    print r, x 
