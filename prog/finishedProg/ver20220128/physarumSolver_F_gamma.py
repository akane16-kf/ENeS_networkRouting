import numpy as np
import networkx as nx
import os
import pickle
from tqdm import tqdm
from collections import Counter
from trafficFlow_gamma import TrafficFlow as TF

class PhysarumSolver_F(object):
    """docstring for PhysarumSolver_F."""

    def __init__(self, G, nodes, edges, nodesID_NX_SUMO, nodesNum, source, sink, route_border, route_candidate_border, totalFlow, repeatNum, delta_t, mu):
        self.G = G
        self.nodes = nodes
        self.edges = edges
        self.nodesID_NX_SUMO = nodesID_NX_SUMO
        self.N = nodesNum
        self.source = source
        self.sink = sink
        self.route_border = route_border
        self.route_candidate_border = route_candidate_border
        self.I0 = totalFlow
        self.Repeat = repeatNum
        self.dt = delta_t
        self.mu = mu


    #不完全コレスキー分解付き共役勾配法
    #http://www.slis.tsukuba.ac.jp/~fujisawa.makoto.fu/cgi-bin/wiki/index.php?%C1%B0%BD%E8%CD%FD%C9%D5%A4%AD%B6%A6%CC%F2%B8%FB%C7%DB%CB%A1

    #https://gist.github.com/EnsekiTT/7256654
    # 拝借させていただいた。感謝。
    ###
    # Solve Ax = b
    # A : real, symmetric, positive-definite matrix
    # b : A*x_init
    # x_init : Initial vector
    ###
    def cgm(self, A, b, x_init):
        x = x_init
        r0 = b - np.dot(A,x)
        p = r0
        k = 0
        for i in range(200):
            a = float( np.dot(r0.T,r0) / np.dot(np.dot(p.T, A),p) )
            x = x + p*a
            r1 = r0 - np.dot(A*a, p)
            #print(np.linalg.norm(r1))
            if np.linalg.norm(r1) < 1.0e-10:
                return x
            b = float( np.dot(r1.T, r1) / np.dot(r0.T, r0) )
            p = r1 + b * p
            r0 = r1
        return x

    # 文献式6、左辺
    def SetA(self, F, D):
        for e in D: self.G.edges[e]['C'] = D[e]*F[e]

        A = np.zeros((self.N,self.N))
        for j1 in range(1,self.N+1):
            j = j1 - 1
            for i1 in range(1,self.N+1):
                i = i1 - 1
                if i != j:
                    A[j][i] = self.G.edges.get((i1,j1),{'C':0})['C']
                else:
                    A[j][i] = self.G.edges.get((i1,j1),{'C':0})['C'] - sum([self.G.edges.get((k,j1),{'C':0})['C'] for k in range(1,self.N+1)])

                #if (i1,j1) == (1,1):
                #    print(G.edges.get((i1,j1),{'C':0})['C'])
                #    print(A[j][i])

        return A

    # 文献式6、右辺
    def SetB(self):
        B = np.zeros((self.N,1))
        for j1 in range(1,self.N+1):
            j = j1 - 1

            if j1 == self.source:
                B[j][0] = - self.I0
            elif j1 == self.sink:
                B[j][0] = self.I0
            else:
                B[j][0] = 0

        return B

    def calculateShapedTrafficFlow_avg(self, shapedTrafficFlow):
        shapedTF_avg = {}
        shapedTF_sum = {}
        shapedTF_keys = list(shapedTrafficFlow.keys())
        for i in range(len(shapedTF_keys)):
            shapedTF_sum = dict(Counter(shapedTF_sum) + Counter(shapedTrafficFlow[shapedTF_keys[i]]))
            print(i, shapedTF_keys[i])
        for e in shapedTF_sum.keys():
            shapedTF_avg[e] = shapedTF_sum[e] / len(shapedTF_keys)

        return shapedTF_avg

    def setF(self, filename_fcd_shaped, filename_shapedTF_log,  filename_fcd, filename_rnd, smallF):
        F = {}
        if os.path.isfile(filename_fcd_shaped):
            with open(filename_fcd_shaped, 'rb') as f:
                F = pickle.load(f)
        else:
            if os.path.isfile(filename_shapedTF_log):
                with open(filename_shapedTF_log, 'rb') as f:
                    shapedTrafficFlow = pickle.load(f)
            else:
                TF2 = TF(self.nodesID_NX_SUMO, self.edges)
                shapedTrafficFlow = TF2.main(filename_fcd, filename_rnd)
                with open(filename_shapedTF_log, "wb") as f_log:
                    pickle.dump(shapedTrafficFlow, f_log)
            F = self.calculateShapedTrafficFlow_avg(shapedTrafficFlow)
            for e in self.edges:
                if e in F:
                    pass
                else:
                    F[e] = smallF
            with open(filename_fcd_shaped,"wb") as f:
                pickle.dump(F, f)
        return F

    def calculateLength_path(self, L, route, shortest_path):
        length_path = 0
        length_shortestpath = 0
        edgeList_shortestpath = []
        for e in route:
            length_path = length_path + L[e]

        for i,content in enumerate(shortest_path):
            if i != len(shortest_path)-1:
                edgeList_shortestpath.append(tuple([shortest_path[i], shortest_path[i+1]]))
            else:
                for e in edgeList_shortestpath:
                    length_shortestpath = length_shortestpath + L[e]

        return length_path, length_shortestpath


    def printResult(self, filename_fcd_shaped, route):
        route_sorted = []
        target = self.source
        for index in range(len(route)):
            for e in route:
                if e[0] == target:
                        route_sorted.append(target)
                        target = e[1]
                elif e[1] == target:
                    route_sorted.append(target)
                    target = e[0]
            if len(route_sorted) == len(route):
                route_sorted.append(self.sink)


        return(route_sorted)



    def main(self, filename_fcd_shaped, filename_shapedTF_log, filename_fcd, filename_rnd, smallF):
        Q = {}
        F = {}
        D = {}
        x = [[] for i in range(len(self.edges))]
        y = [[] for i in range(len(self.edges))]


        F = self.setF(filename_fcd_shaped, filename_shapedTF_log,  filename_fcd, filename_rnd, smallF)

        #Dの初期値を設定
        for e in nx.edges(self.G):
            D[e] = np.random.uniform(0.5, 1.0)
        # pの初期値を（適当に）設定
        P0 = np.zeros((self.N,1))

        #式6右辺
        B = self.SetB()

        for t in tqdm(range(self.Repeat)):
            #print('t=%d'%(t))

            #式6左辺、Dをもとに更新
            A = self.SetA(F, D)

            P = self.cgm(A, B, P0)
            #print(P)

            for i in range(len(self.edges)):
                e = self.edges[i]
                x[i].append(t)
                y[i].append(D[e])

            #DからQ計算

            for e in self.edges:
                i = e[0] - 1
                j = e[1] - 1
                Q[e] = self.G.edges[e]['C']*(P[i][0] - P[j][0])
                if t==0 or t==self.Repeat-1:
                    print("%s, Q:%.2f"%(e,Q[e]))

            #D更新
            for e in self.edges:
                #print("%s, D:%.2f -> "%(e,D[e]), end='')
                D[e] = ( D[e] + self.dt*(abs(Q[e])**self.mu) )/(1 + self.dt)
                #print('%.2f'%(D[e]))

        route = []
        route_candidate = []
        for e in self.edges:
            if abs(Q[e]) > self.route_border:
                route.append(e)
                route_candidate.append(e)
            elif abs(Q[e]) > self.route_candidate_border:
                route_candidate.append(e)

        print(self.printResult(filename_fcd_shaped, route))
        print(route)
        #print(self.calculateLength_path(L, route, nx.shortest_path(self.G, source=self.source, target=self.sink)))

        return Q, route, route_candidate, x, y
