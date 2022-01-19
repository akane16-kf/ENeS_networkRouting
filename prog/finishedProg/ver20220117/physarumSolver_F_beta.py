import numpy as np
import networkx as nx
from trafficFlow import TrafficFlow as TF

class PhysarumSolver_F(object):
    """docstring for PhysarumSolver_F."""

    def __init__(self, G, nodes, edges, nodesID_NX_SUMO, nodesNum, source, sink, totalFlow, repeatNum, delta_t, mu):
        self.G = G
        self.nodes = nodes
        self.edges = edges
        self.nodesID_NX_SUMO = nodesID_NX_SUMO
        self.N = nodesNum
        self.source = source
        self.sink = sink
        self.I0 = totalFlow
        self.Repeat = repeatNum
        self.dt = delta_t
        self.mu = mu
        self.F = {}
        self.D = {}
        self.Q = {}
        self.x = [[] for i in range(len(edges))]
        self.y = [[] for i in range(len(edges))]


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
    def SetA(self):
        blacklist_e = []
        for e in self.D:
            revers_e = tuple([e[1], e[0]])
            if e not in blacklist_e:
                self.G.edges[e]['C'] = self.D[e]*self.F[e]
                blacklist_e.append(revers_e)
            else:
                self.G.edges[e]['C'] = self.D[revers_e]*self.F[revers_e]



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
                B[j][0] = -self.I0
            elif j1 == self.sink:
                B[j][0] = self.I0
            else:
                B[j][0] = 0

        return B


    def main(self):

        #エッジの交通量の設定。
        TF2 = TF(self.nodesID_NX_SUMO, self.edges)
        F_tmp = TF2.main()
        keysList_F = list(F_tmp.keys())
        self.F = F_tmp[keysList_F[0]]


        #Dの初期値を設定
        for e in nx.edges(self.G):
            self.D[e] = np.random.uniform(0.5, 1.0)

        # pの初期値を（適当に）設定
        P0 = np.zeros((self.N,1))

        #式6右辺
        B = self.SetB()

        for t in range(self.Repeat):
            print('t=%d'%(t))

            #式6左辺、Dをもとに更新
            A = self.SetA()
            #print(A)

            P = self.cgm(A, B, P0)
            #print(P)

            for i in range(len(self.edges)):
                e = self.edges[i]
                self.x[i].append(t)
                self.y[i].append(self.D[e])

            #DからQ計算
            for e in self.edges:
                i = e[0] - 1
                j = e[1] - 1
                self.Q[e] = self.G.edges[e]['C']*(P[i][0] - P[j][0])
                if t==0 or t==self.Repeat-1:
                    print("%s, Q:%.2f"%(e,self.Q[e]))

            #D更新
            for e in self.edges:
                #print("%s, D:%.2f -> "%(e,D[e]), end='')
                self.D[e] = ( self.D[e] + self.dt*(abs(self.Q[e])**self.mu) )/(1 + self.dt)
                #print('%.2f'%(D[e]))
