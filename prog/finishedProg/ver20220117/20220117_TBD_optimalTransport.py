'''
import packages and classes
'''
import matplotlib.pyplot as plt #to plot graphs
import networkx as nx #to make the road network
import sys
from physarumSolver_beta import PhysarumSolver as PS #to search the route
from physarumSolver_F_beta import PhysarumSolver_F as PSF #to search the route
from processingRoadData_beta import ProcessingRoadData as PRD #to process road data

'''
set parameters
'''
nodes = {}
edges = [] #make a dictionary and a list for storing network information
nodesID_NX_SUMO = {}
source = 1669
sink = 1637 #set start and goal of the route
nodes_sourceSink = [source, sink]
totalFlow = 1
mu = 1.3
delta_t = 1
repeatNum = 30 #set parameters for the searching the route
f_path = './lust.net.xml'

'''
read the road data file and process it
'''
PRD = PRD(f_path)
nodes, edges, nodesID_NX_SUMO = PRD.main()
nodesNum = len(nodes)
'''
make the network from the lists
'''
G = nx.DiGraph()
G.add_nodes_from(nodes.keys())
G.add_edges_from(edges)


'''
plot the network before searching route
'''
print('Showing the graph? Please type y or n.')
input_char = input()
if input_char == 'y':
    nx.draw(G, pos=nodes, node_size=10)
    nx.draw_networkx_nodes(G, pos=nodes, node_size=50, nodelist=nodes_sourceSink, node_color="r")
    plt.show()
'''
rearch the route
'''
print('Which parameter do you want to use for searching? Please type L or F or T.')
input_char = input()
flag = 'N'
if  input_char == 'L':
    PS = PS(G, nodes, edges, nodesNum, source, sink, totalFlow, repeatNum, delta_t, mu)
    PS.main()
    flag = 'L'
elif input_char == 'F':
    PSF = PSF(G, nodes, edges, nodesID_NX_SUMO, nodesNum, totalFlow, repeatNum, delta_t, mu)
    PSF.main()
    flag = 'F'
elif input_char == 'T':
    print('Have not prepared')
    sys.exit()
    flag = 'T'
else:
    print('???????????')
    sys.exit()


'''
plot the network with the route
'''
if flag == 'L':
    Q1 = {e:abs(PS.Q[e]) for e in PS.Q}
elif flag == 'F':
    Q1 = {e:abs(PSF.Q[e]) for e in PSF.Q}
elif flag == 'T':
    Q1 = {e:abs(PST.Q[e]) for e in PST.Q}
nx.draw(G, pos=nodes, node_size=10, style=':')
for e in Q1:
    nx.draw_networkx_edges(G, pos=nodes, edgelist=[e,], width=Q1[e]*10)
nx.draw_networkx_nodes(G, pos=nodes, node_size=50, nodelist=nodes_sourceSink, node_color="r")
print('Showing the graph or saving the graph? Please type show or save.')
input_char = input()
if input_char == 'show':
    plt.show()
elif input_char == 'save':
    plt.savefig('result_figure.png')
else:
    sys.exit()
'''
plot the graph of xxxxxxxx
'''
fig, ax = plt.subplots()
if flag == 'L':
    for i in range(len(edges)):
        ax.plot(PS.x[i],PS.y[i])
elif flag == 'F':
    for i in range(len(edges)):
        ax.plot(PSF.x[i],PSF.y[i])
elif flag == 'T':
    for i in range(len(edges)):
        ax.plot(PST.x[i],PST.y[i])
ax.set_xlabel("$t$")
ax.set_ylabel("$D_{ij}$")
plt.show()
