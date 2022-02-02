'''
import packages and classes
'''
import matplotlib.pyplot as plt #to plot graphs
import networkx as nx #to make the road network
import sys
import pickle
from physarumSolver_gamma import PhysarumSolver as PS #to search the route
from physarumSolver_F_gamma import PhysarumSolver_F as PSF #to search the route
from processingRoadData_gamma import ProcessingRoadData as PRD #to process road data

'''
set parameters
'''
nodes = {}
edges = [] #make a dictionary and a list for storing network information
nodesID_NX_SUMO = {}
source = 587
sink = 1824 #set start and goal of the route
nodes_sourceSink = [source, sink]
route_border = 0.8
route_candidate_border = 0.1
totalFlow = 1
mu = 1.3
delta_t = 1
repeatNum = 30 #set parameters for the searching the route
smallF = 1
trafficFlow_time = 1830
filename_fcd = f'./../trafficFlowData/fcdOutput_extracted_{trafficFlow_time}.xml'
filename_rnd = './lust.net.xml'
filename_fcd_shaped = f'./../trafficFlowData/fcdoutput_shaped_{trafficFlow_time}.pkl'
filename_shapedTF_log = f'./../trafficFlowData/shapedTF_log_{trafficFlow_time}.pkl'
filename_result_log = f'./../resultData/resultQ_{trafficFlow_time}.pkl'

'''
read the road data file and process it
'''
PRD = PRD(filename_rnd)
nodes, edges, nodesID_NX_SUMO = PRD.main()
nodesNum = len(nodes)
'''
make the network from the lists
'''
G = nx.Graph()
G.add_nodes_from(nodes.keys())
G.add_edges_from(edges)


'''
plot the network before searching route
'''
input_char = input("Showing the graph? Please type y or n.")
while input_char != 'y' and input_char != 'n':
    input_char = input("Showing the graph? Please type y or n.")
nodes_color = ['red' if e in nodes_sourceSink else 'blue' for e in G.nodes()]
nodes_size = [50 if e in nodes_sourceSink else 10 for e in G.nodes()]
if input_char == 'y':
    nx.draw(G, pos=nodes, node_size=nodes_size, node_color=nodes_color, with_labels=True)
    plt.show()
'''
rearch the route
'''
input_char = input("Which parameter do you want to use for searching? Please type L or F or T.")
while input_char != 'L' and input_char != 'F' and input_char != 'T':
    input_char = input("Which parameter do you want to use for searching? Please type L or F or T.")
if  input_char == 'L':
    PS = PS(G, nodes, edges, nodesNum, source, sink, route_border, route_candidate_border, totalFlow, repeatNum, delta_t, mu)
    Q, route, route_candidate, x, y = PS.main(filename_fcd_shaped)
    input_char = input("Save the log? Please type y or n.")
    while input_char != 'y' and input_char != 'n':
        input_char = input("Save the log? Please type y or n.")
    if input_char == 'y':
        with open(filename_result_log, 'wb') as f:
            pickle.dump(Q, f)
elif input_char == 'F':
    PSF = PSF(G, nodes, edges, nodesID_NX_SUMO, nodesNum, source, sink, route_border, route_candidate_border, totalFlow, repeatNum, delta_t, mu)
    Q, route, route_candidate, x, y = PSF.main(filename_fcd_shaped, filename_shapedTF_log, filename_fcd, filename_rnd, smallF)
    input_char = input("Save the log? Please type y or n.")
    while input_char != 'y' and input_char != 'n':
        input_char = input("Save the log? Please type y or n.")
    if input_char == 'y':
        with open(filename_result_log, 'wb') as f:
            pickle.dump(Q, f)
elif input_char == 'T':
    print('Have not prepared')
    sys.exit()

'''
plot the network with the route
'''
input_char = input("Showing the graph or saving the graph? Please type show or save.")
while input_char != 'show' and input_char != 'save':
    input_char = input("Showing the graph or saving the graph? Please type show or save.")
edges_color = ['red' if e in route else 'black' for e in G.edges()]
edges_width = {e:abs(Q[e])*10 for e in Q}
nx.draw(G, pos=nodes, node_size=nodes_size, node_color=nodes_color, style=':', with_labels=True)
for e in route_candidate:
    nx.draw_networkx_edges(G, pos=nodes, edgelist=[e], edge_color=edges_color, width=edges_width[e])
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
for i in range(len(edges)):
    ax.plot(x[i], y[i])
ax.set_xlabel("$t$")
ax.set_ylabel("$D_{ij}$")
plt.show()
