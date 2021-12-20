'''
import packages and classes
'''
import matplotlib.pyplot as plt #to plot graphs
import networkx as nx #to make the road network
from physarumSolver import PhysarumSolver as PS #to search the route
from processingRoadData import ProcessingRoadData as PRD #to process road data

'''
set parameters
'''
nodes = {}
edges = [] #make a dictionary and a list for storing network information
source = '-1010'
sink = '-9996' #set start and goal of the route
totalFlow = 1
mu = 1.3
delta_t = 1
repeatNum = 30 #set parameters for the searching the route
f_path = './../sumoScenarios/LuSTScenario-master/scenario/lust.net.xml'

'''
read the road data file and process it
'''
PRD = PRD(nodes, edges, f_path, source, sink)
PRD.main()
nodesNum = len(PRD.nodes)
'''
make the network from the lists
'''
G = nx.Graph()
G.add_nodes_from(PRD.nodes.keys())
G.add_edges_from(PRD.edges)

'''
plot the network before searching route
'''
nx.draw(G, pos=PRD.nodes, with_labels=True)
plt.show()
'''
rearch the route
'''
PS = PS(G, PRD.nodes, PRD.edges, nodesNum, totalFlow, repeatNum, delta_t, mu)
PS.main()
'''
plot the network with the route
'''
Q1 = {e:abs(PS.Q[e]) for e in PS.Q}
nx.draw(G, pos=PRD.nodes,style=':', with_labels=True)
for e in Q1:
    nx.draw(G, pos=PRD.nodes,edgelist=[e,], width=Q1[e]*10)
plt.show()
'''
plot the graph of xxxxxxxx
'''
fig, ax = plt.subplots()
for i in range(len(PRD.edges)):
    ax.plot(PS.x[i],PS.y[i])
ax.set_xlabel("$t$")
ax.set_ylabel("$D_{ij}$")
plt.show()
