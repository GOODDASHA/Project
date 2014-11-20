import csv




class DFSHandler():

    def __init__(self, filename, id_tag='dokid', ref_tag='refunifids'):
        self._paperset = {eval(data[id_tag])[0]:eval(data[ref_tag]) 
                            for data in csv.DictReader(open(filename))}
        self._num = len(self._paperset)
        self._discovered = {}

    def execute(self):
        self._visited = {}
        for paper in self._paperset:
            if paper not in self._visited:
                self.DFS(paper)


    def DFS(self, paper, parent=None):
        if paper not in self._paperset:
            return

        if parent == None:
            self._discovered[paper] = {paper:1}
        else:
            print paper, parent
            self._discovered[parent][paper] = 1

        self._visited[paper] = 1

        for ref in self._paperset[paper]:
            if ref not in self._discovered:
                self.DFS(ref, paper)

    def get_cluster(self):

        print len(self._paperset), len(self._discovered.keys()), len(self._discovered.values())


    def check(self):
        for x,v  in self._paperset.items():
            for r in v:
                if r in self._paperset:
                    print r, x 
