import re
import sys

class ProcessingRoadData(object):
    """docstring for ProcessingRoadData."""

    def __init__(self, nodes, edges, f_path, source, sink):
        self.nodes = nodes
        self.edges = edges
        self.f_path = f_path
        self.source = source
        self.sink = sink
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


    def replaceNodeID_toNXfromSUMO(self, SUMOList, nodes_id_NXnSUMO):
        NXList = []
        counter = 0

        for i, contents_i in enumerate(SUMOList):
            tmpList = []
            for j, contents_j in enumerate(nodes_id_NXnSUMO):
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
        for i, contents in enumerate(tmpList_setSourcenSink):
            if (contents[0] == self.source) and (i != 0):
                tmpList_setSourcenSink[0], tmpList_setSourcenSink[i] = tmpList_setSourcenSink[i], tmpList_setSourcenSink[0]
                print('swaped: source')
            if (contents[0] == self.sink) and (i != 1):
                tmpList_setSourcenSink[1], tmpList_setSourcenSink[i] = tmpList_setSourcenSink[i], tmpList_setSourcenSink[1]
                print('swaped: sink')

    def processingFileData(self):
        #process
        self.nodes = {}
        nodes_id_NXnSUMO = []
        tmpList_setSourcenSink = []
        for i, contents in enumerate(self.lines_necessary_forNode):
            tmp_list_allNumInfo = re.findall(r'[+-]?\d+(?:\.\d+)?', contents)
            tmpList_setSourcenSink.append(tmp_list_allNumInfo)
        self.setSourcenSink(tmpList_setSourcenSink)
        print(tmpList_setSourcenSink)

        for i, contents in enumerate(tmpList_setSourcenSink):
            self.nodes[i+1] = (float(contents[1]), float(contents[2]))
            nodes_id_NXnSUMO.append((i+1, int(contents[0])))


        self.edges = []
        tmpEdgeList = []
        for i, contents in enumerate(self.lines_necessary_forEdge):
            tmp_list_allNumInfo = re.findall(r'[+-]?\d+#?(?:\.\d+)?\d*', contents)
            tmpEdgeList.append((int(tmp_list_allNumInfo[1]), int(tmp_list_allNumInfo[2])))

        self.edges = self.delete_unnecessaryEdge(self.replaceNodeID_toNXfromSUMO(tmpEdgeList, nodes_id_NXnSUMO))


    def main(self):
        self.readFile()
        self.processingFileData()
