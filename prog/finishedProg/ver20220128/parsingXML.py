import xml.etree.ElementTree as ET

class ParsingXML(object):
    """docstring for PhysarumSolver."""

    def parsingFcdXML(self, filename):

        tree = ET.parse(filename)
        root = tree.getroot()

        fcdoutput_parsed = {}
        for timestep in root:
            tmpDict_necessaryVehicleInfo = {}
            for vehicle in timestep:
                if ('Added' not in vehicle.attrib['lane']):
                    tmpList = [vehicle.attrib['speed'], vehicle.attrib['lane']]
                    tmpDict_necessaryVehicleInfo[vehicle.attrib['id']] = tmpList
            fcdoutput_parsed[timestep.attrib['time']] = tmpDict_necessaryVehicleInfo

        return fcdoutput_parsed


    def parsingNetXML(self, filename):

        tree = ET.parse(filename)
        root = tree.getroot()

        roadNetData_parsed = {}
        tmpDict_necessaryRoadInfo = {}
        for edge in root.iter('edge'):
            if ('function' not in edge.attrib) and ('Added' not in edge.attrib['id']) and ('Added' not in edge.attrib['from']) and ('Added' not in edge.attrib['to']):
                tmpList = [edge.attrib['from'], edge.attrib['to']]
                tmpDict_necessaryRoadInfo[edge.attrib['id']] = tmpList
        roadNetData_parsed['edge'] = tmpDict_necessaryRoadInfo

        tmpDict_necessaryRoadInfo = {}
        for junction in root.iter('junction'):
            if ('internal' not in junction.attrib['type']) and ('Added' not in junction.attrib['id']):
                tmpList = [junction.attrib['x'], junction.attrib['y']]
                tmpDict_necessaryRoadInfo[junction.attrib['id']] = tmpList
        roadNetData_parsed['junction'] = tmpDict_necessaryRoadInfo

        tmpDict_necessaryRoadInfo = {}
        index = 1
        for connection in root.iter('connection'):
            if ('Added' not in connection.attrib['from']) and ('Added' not in connection.attrib['to']):
                tmpList = [connection.attrib['from'], connection.attrib['to']]
                tmpDict_necessaryRoadInfo[index] = tmpList
                index = index + 1
        roadNetData_parsed['connection'] = tmpDict_necessaryRoadInfo

        return roadNetData_parsed



    def main(self, filename):
        if 'net' in filename:
            resultDict = self.parsingNetXML(filename)
            return resultDict
        else:
            resultDict = self.parsingFcdXML(filename)
            return resultDict


if __name__ == '__main__':
    print('Please enter filename')
    filename = input()
    PXML =  ParsingXML(filename)

    if 'net' in filename:
        resultDict = PXML.parsingNetXML(filename)
        print(resultDict)
    else:
        resultDict = PXML.parsingFcdXML(filename)
        print(resultDict)
