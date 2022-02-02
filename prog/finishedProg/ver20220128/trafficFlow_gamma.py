import re
from tqdm import tqdm
from parsingXML import ParsingXML as PXML

class TrafficFlow(object):
    """docstring for TrafficFlow."""

    def __init__(self, nodesID_NX_SUMO, edges):
        self.nodesID_NX_SUMO = nodesID_NX_SUMO
        self.edges = edges
        self.roadNet_parsed = {}

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


    def search_nodeID_SUMO(self, PXML_inst, filename_rnd, edgeID_SUMO):
        roadNet_parsed = PXML_inst.main(filename_rnd)
        for edgeID_SUMO_search, nodeID_SUMO_search in roadNet_parsed['edge'].items():
            if edgeID_SUMO == edgeID_SUMO_search.replace('-', ''):
                nodeID_SUMO = nodeID_SUMO_search
                return nodeID_SUMO

    def search_nodeID_NX_fromSUMO(self, nodeID_SUMO):
        tmpList = [0,0]
        flag = 0
        for nodeID_NX_search, nodeID_SUMO_search in self.nodesID_NX_SUMO.items():
            if nodeID_SUMO_search == int(nodeID_SUMO[0]):
                tmpList[0] = nodeID_NX_search
                flag = flag + 1
            elif nodeID_SUMO_search == int(nodeID_SUMO[1]):
                tmpList[1] = nodeID_NX_search
                flag = flag + 1
        if tmpList[0] > tmpList[1]:
            tmpList[0], tmpList[1] = tmpList[1], tmpList[0]
        nodeID_NX = tuple(tmpList)
        return nodeID_NX

    def shapingTrafficFlow(self, traffic_flow, PXML_inst, filename_rnd):
        shapedTrafficFlow = {}
        for time in traffic_flow:
            shapedTrafficFlow_time = {}
            for edgeID_SUMO, num_car in tqdm(traffic_flow[time].items()):
                nodeID_SUMO = self.search_nodeID_SUMO(PXML_inst, filename_rnd, edgeID_SUMO)
                if nodeID_SUMO:
                    e = self.search_nodeID_NX_fromSUMO(nodeID_SUMO)
                    shapedTrafficFlow_time[e] = num_car
            shapedTrafficFlow[time] = shapedTrafficFlow_time
        return shapedTrafficFlow


    def main(self, filename_fcd, filename_rnd):
        PXML_inst = PXML()
        fcdoutput_parsed = PXML_inst.main(filename_fcd)
        #print(fcdoutput_parsed)
        traffic_flow = self.getTrafficFlow(fcdoutput_parsed)
        return(self.shapingTrafficFlow(traffic_flow, PXML_inst, filename_rnd))


if __name__ == '__main__':
    filename = 'fcdoutput_sample.xml'

    PXML = PXML(filename)
    fcdoutput_parsed = PXML.main()

    TF = TrafficFlow(fcdoutput_parsed)
    traffic_flow = TF.getTrafficFlow()

    for time in traffic_flow:
        print(time, traffic_flow[time])
