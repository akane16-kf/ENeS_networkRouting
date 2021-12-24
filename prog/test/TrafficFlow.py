import ParsingXML as PXML
import re


class TrafficFlow():

    def __init__(self, fcdoutput_parsed):
        fcdoutput_parsed = fcdoutput_parsed

    def getTrafficFlow(self):
        '''
        Returns traffic flow from a parsed fcdoutput.

        Variables:
            traffic_flow (dict): Traffic flow calculated from a parsed fcdoutput.
            duration (int): The duration to hold before the total traffic flow is stored. For example, when the duration is 1, traffic flow is calculated for every 1 time. When duration is 10, traffic flow is calculated for every 10 time.

        :param filename:
        :return: traffic_flow
        '''
        traffic_flow = {}
        duration = 10

        duration_index = 1
        lane = set()
        temp_traffic_flow = {}

        i = 0
        for time in fcdoutput_parsed:
            for vehicle in fcdoutput_parsed[time]:
                current_lane = str(fcdoutput_parsed[time][vehicle][1])[:-2]
                lane_pattern = "[0-9]{2,5}[#|_]*[0-9]*eishim"
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


if __name__ == '__main__':
    filename = 'due-actuated.xml'

    PXML = PXML.ParsingXML(filename)
    fcdoutput_parsed = PXML.main()

    TF = TrafficFlow(fcdoutput_parsed)
    traffic_flow = TF.getTrafficFlow()

    for time in traffic_flow:
        print(time, traffic_flow[time])
