import re
from parsingXML import ParsingXML as PXML

class TrafficFlow(object):
    """docstring for TrafficFlow."""

    def __init__(self, nodes_id_NXnSUMO, edges):
        self.nodes_id_NXnSUMO = nodes_id_NXnSUMO
        self.edges = edges
        self.roadNet_parsed = {}
        self.F = {}

    def getTrafficFlow(self, fcdoutput_parsed):
        '''
        Returns traffic flow from a parsed fcdoutput.
        Variables:
            traffic_flow (dict): Traffic flow calculated from a parsed fcdoutput.
            duration (int): The duration to hold before the total traffic flow is stored. For example, when the duration is 1, traffic flow is calculated for every 1 time. When duration is 10, traffic flow is calculated for every 10 time.
        :param filename:
        :return: traffic_flow
        '''
        traffic_flow = {}
        duration = 600

        duration_index = 1
        lane = set()
        temp_traffic_flow = {}

        i = 0
        for time in fcdoutput_parsed:
            for vehicle in fcdoutput_parsed[time]:
                current_lane = str(fcdoutput_parsed[time][vehicle][1])
                lane_pattern = "[0-9]{2,5}[#|_]*[0-9]*"
                current_lane = re.findall(lane_pattern, current_lane)[0]
                if current_lane in lane:
                    temp_traffic_flow[current_lane] += 1
                else:
                    lane.add(current_lane)
                    temp_traffic_flow[current_lane] = 1

            if duration_index % duration == 0:
                traffic_flow[time] = temp_traffic_flow
                duration_index = 1
                lane = set()
                temp_traffic_flow = {}
            else:
                duration_index += 1

        return traffic_flow

    def setF(self, traffic_flow, PXML2):
        #print(self.nodes_id_NXnSUMO)
        filename = 'lust.net.xml'
        self.roadNet_parsed = PXML2.main(filename)
        #print(roadNet_parsed['edge'])
        for time in traffic_flow:
            F_tmp = {}
            #print(traffic_flow[time])
            for edgeID_SUMO, num_car in traffic_flow[time].items():
                #print(edgeID_SUMO)
                #print(num_car)
                nodeID_SUMO = self.search_nodeID_SUMO(edgeID_SUMO)
                if nodeID_SUMO:
                    #print(edgeID_SUMO, nodeID_SUMO, num_car)
                    e = self.search_nodeID_NX_fromSUMO(nodeID_SUMO)
                    F_tmp[e] = num_car
            for e_search in self.edges:
                if e_search in F_tmp:
                    pass
                else:
                    F_tmp[e_search] = 1
            self.F[time] = F_tmp
        #print(self.F)


                #print(nodeID_SUMO)
                #num_car = 1
                #self.F[e] = num_car
                #交通量のあるfだけ先に作成して後から交通量のないところに0をいれる
                #eと同じタプルを作成して入れなかればいけない
                #要素は台数
                #それかeとtraffic_flow[time]の二重for文
                #わかりやすいが計算量が何倍にもなりそう

    def search_nodeID_SUMO(self, edgeID_SUMO):
        #print(self.roadNet_parsed['edge'])
        for edgeID_SUMO_serch, nodeID_SUMO_serch in self.roadNet_parsed['edge'].items():
            if edgeID_SUMO == edgeID_SUMO_serch.replace('-', ''):
                nodeID_SUMO = nodeID_SUMO_serch
                return nodeID_SUMO

    def search_nodeID_NX_fromSUMO(self, nodeID_SUMO):
        tmpList = [0,0]
        flag = 0
        for nodeID_serch in self.nodes_id_NXnSUMO:
            if nodeID_serch[1] == int(nodeID_SUMO[0]):
                tmpList[0] = nodeID_serch[0]
                flag = flag + 1
            elif nodeID_serch[1] == int(nodeID_SUMO[1]):
                tmpList[1] = nodeID_serch[0]
                flag = flag + 1
        if tmpList[0] > tmpList[1]:
            tmpList[0], tmpList[1] = tmpList[1], tmpList[0]
        nodeID_NX = tuple(tmpList)
        return nodeID_NX



    def main(self):
        filename = 'fcdoutput_sample.xml'

        PXML2 = PXML()
        fcdoutput_parsed = PXML2.main(filename)

        traffic_flow = self.getTrafficFlow(fcdoutput_parsed)

        self.setF(traffic_flow, PXML2)

        '''
        for time in traffic_flow:
            print(time, traffic_flow[time])
        '''
        return self.F


if __name__ == '__main__':
    filename = 'fcdoutput_sample.xml'

    PXML = PXML(filename)
    fcdoutput_parsed = PXML.main()

    TF = TrafficFlow(fcdoutput_parsed)
    traffic_flow = TF.getTrafficFlow()

    for time in traffic_flow:
        print(time, traffic_flow[time])
