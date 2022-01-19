import re
import sys
import matplotlib.pyplot as plt #to plot graphs
import networkx as nx #to make the road network

class ProcessingRoadData_test(object):
    """docstring for ProcessingRoadData_test."""

    def __init__(self, nodes, edges, f_path, source, sink):
        self.nodes = nodes
        self.edges = edges
        self.f_path = f_path
        self.source = source
        self.sink = sink
        self.nodes_id_NXnSUMO = []
        self.lines_necessary_forNode = []
        self.lines_necessary_forEdge = []

    def has_duplicates(self, seq):
        seen = []
        unique_list = [x for x in seq if x not in seen and not seen.append(x)]
        return len(seq) != len(unique_list)

    def delete_unnecessaryEdge(self, edges):
        resultList = []
        blackList = []

        for line in edges:
            if (line not in resultList) and (line not in blackList):
                resultList.append(line)
                blackList.append(tuple([line[1], line[0]]))

        return resultList


    def replaceNodeID_toNXfromSUMO(self, SUMOList):
        NXList = []
        counter = 0

        for i, contents_i in enumerate(SUMOList):
            tmpList = []
            for j, contents_j in enumerate(self.nodes_id_NXnSUMO):
                for k, contents_k in enumerate(contents_i):
                    if contents_k == contents_j[1]:
                        tmpList.append(contents_j[0])
                    else:
                        continue

            NXList.append(tuple(tmpList))

        return NXList


    def readFile(self):
        keyword_forNode = '<junction id'
        keyword_forEdge = '<edge id'

        #data input from the file
        with open(self.f_path) as f:
            #read line for nodes
            lines = f.readlines()
            lines_strip = [line.strip() for line in lines] #delete indention
            lines_SWkeyword_forNode = [line for line in lines_strip if line.startswith(keyword_forNode)] #extraction of some lines with keyword_forNode
            self.lines_necessary_forNode = [line for line in lines_SWkeyword_forNode if ('internal' not in line) and ('AddedOnRampNode' not in line) and ('AddedOffRampNode' not in line)]
            lines_SWkeyword_forEdge = [line for line in lines_strip if line.startswith(keyword_forEdge)] #extraction of some lines with keyword_forEdge
            self.lines_necessary_forEdge = [line for line in lines_SWkeyword_forEdge if ('internal' not in line) and ('AddedOnRampNode' not in line) and ('AddedOffRampNode' not in line)]


    def setSourcenSink(self, tmpList_setSourcenSink):
        pass
        '''
        for i, contents in enumerate(tmpList_setSourcenSink):
            if (contents[0] == self.source) and (i != 0):
                tmpList_setSourcenSink[0], tmpList_setSourcenSink[i] = tmpList_setSourcenSink[i], tmpList_setSourcenSink[0]
                print('swaped: source')
            if (contents[0] == self.sink) and (i != 1):
                tmpList_setSourcenSink[1], tmpList_setSourcenSink[i] = tmpList_setSourcenSink[i], tmpList_setSourcenSink[1]
                print('swaped: sink')
        '''
    def processingFileData(self):
        #process
        self.nodes = {}
        tmpList_setSourcenSink = []
        for i, contents in enumerate(self.lines_necessary_forNode):
            tmp_list_allNumInfo = re.findall(r'[+-]?\d+(?:\.\d+)?', contents)
            tmpList_setSourcenSink.append(tmp_list_allNumInfo)
        self.setSourcenSink(tmpList_setSourcenSink)


        for i, contents in enumerate(tmpList_setSourcenSink):
            self.nodes[i+1] = (float(contents[1]), float(contents[2]))
            self.nodes_id_NXnSUMO.append((i+1, int(contents[0])))


        self.edges = []
        tmpEdgeList = []
        for i, contents in enumerate(self.lines_necessary_forEdge):
            tmp_list_allNumInfo = re.findall(r'[+-]?\d+#?(?:\.\d+)?\d*', contents)
            tmpEdgeList.append((int(tmp_list_allNumInfo[1]), int(tmp_list_allNumInfo[2])))

        self.edges = self.delete_unnecessaryEdge(self.replaceNodeID_toNXfromSUMO(tmpEdgeList))

        for tuple_nxNodeID in self.edges:
            revers_tuple_nxNodeID = tuple([tuple_nxNodeID[1], tuple_nxNodeID[0]])
            if revers_tuple_nxNodeID not in self.edges:
                self.edges.append(revers_tuple_nxNodeID)
        print(len(self.edges))

    def main(self):
        self.readFile()
        self.processingFileData()

if __name__ == '__main__':
    nodes = {}
    edges = []
    print('Please enter filename')
    filename = input()
    print('Please enter source node number')
    source = input()
    print('Please enter sink node number')
    sink = input()
    PRD =  ProcessingRoadData_test(nodes, edges, filename, source, sink)

    PRD.readFile()
    PRD.processingFileData()

    print('show graph? y or n')
    flag = input()
    if flag == 'y':
        G = nx.DiGraph()
        G.add_nodes_from(PRD.nodes.keys())
        G.add_edges_from(PRD.edges)
        nx.draw(G, pos=PRD.nodes, with_labels=True)
        plt.show()
