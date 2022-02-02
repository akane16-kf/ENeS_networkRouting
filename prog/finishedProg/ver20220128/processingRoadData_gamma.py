import matplotlib.pyplot as plt #to plot graphs
import networkx as nx #to make the road network
import re
import sys
from parsingXML import ParsingXML as PXML

class ProcessingRoadData(object):
    """docstring for ProcessingRoadData."""

    def __init__(self, filename_rnd):
        self.filename_rnd = filename_rnd

    def delete_unnecessaryEdge(self, edges):
        resultList = []
        blackList = []

        for line in edges:
            if (line not in resultList) and (line not in blackList):
                resultList.append(line)
                blackList.append(tuple([line[1], line[0]]))

        return resultList

    def sort_edgeList(self, edges):
        resultList = []

        for e in edges:
            if e[0] > e[1]:
                resultList.append(tuple([e[1], e[0]]))
            else:
                resultList.append(e)
        resultList.sort(key = lambda e: e[0])
        return resultList


    def replaceNodeID_NXSUMO(self, nodeID_SUMO, nodesID_NX_SUMO):
        edges_info = []
        for tuple_sumoNodeID in nodeID_SUMO:
            tmpList_replacedNodeID = [0]*2
            for nxNodeID in nodesID_NX_SUMO:
                if nodesID_NX_SUMO[nxNodeID] == tuple_sumoNodeID[0]:
                    tmpList_replacedNodeID[0] = nxNodeID
                elif nodesID_NX_SUMO[nxNodeID] == tuple_sumoNodeID[1]:
                    tmpList_replacedNodeID[1] = nxNodeID
            edges_info.append(tuple(tmpList_replacedNodeID))
        return edges_info

    def processing_parsedRoadData(self, roadNetData_parsed):
        nodes_info = {}
        nodesID_NX_SUMO = {}
        for index, nodes_id in enumerate(roadNetData_parsed['junction'].keys()):
            nodes_info[index+1] = tuple([float(roadNetData_parsed['junction'][nodes_id][0]), float(roadNetData_parsed['junction'][nodes_id][1])])
            nodesID_NX_SUMO[index+1] = int(nodes_id.replace(':', ''))

        edges_info_bidirectional = []
        for edges_id in roadNetData_parsed['edge'].keys():
            edges_info_bidirectional.append(tuple([int(roadNetData_parsed['edge'][edges_id][0]), int(roadNetData_parsed['edge'][edges_id][1])]))
        edges_info_bidirectional = list(dict.fromkeys(self.replaceNodeID_NXSUMO(edges_info_bidirectional, nodesID_NX_SUMO)))

        edges_info = self.sort_edgeList(self.delete_unnecessaryEdge(edges_info_bidirectional))

        return nodes_info, edges_info, nodesID_NX_SUMO

    def main(self):
        PXML_inst = PXML()
        roadNetData_parsed = PXML_inst.main(self.filename_rnd)
        return self.processing_parsedRoadData(roadNetData_parsed)

if __name__ == '__main__':
    print('Please enter filename')
    filename = input()
    PRD =  ProcessingRoadData(filename)
    nodes = {}
    edegs = []
    nodesID_NX_SUMO = {}

    nodes, edges, nodesID_NX_SUMO = PRD.main()


    print('show graph? y or n')
    flag = input()
    if flag == 'y':
        G = nx.Graph()
        G.add_nodes_from(nodes.keys())
        G.add_edges_from(edges)
        nx.draw(G, pos=nodes, with_labels=True)
        plt.show()
