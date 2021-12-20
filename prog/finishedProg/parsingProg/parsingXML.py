import xml.etree.ElementTree as ET

class ParsingXML(object):
    """docstring for PhysarumSolver."""

    def __init__(self, filename):
        self.filename = filename

    def parsingFcdXML(self):

        tree = ET.parse(self.filename)
        root = tree.getroot()

        fcdoutput_parsed = {}
        for timestep in root:
            tmpDict_necessaryVehicleInfo = {}
            for vehicle in timestep:
                tmpList = [vehicle.attrib['speed'], vehicle.attrib['lane']]
                tmpDict_necessaryVehicleInfo[vehicle.attrib['id']] = tmpList
            fcdoutput_parsed[timestep.attrib['time']] = tmpDict_necessaryVehicleInfo

        return fcdoutput_parsed


    def main(self):
        if 'net' in self.filename:
            print('not prepared for this file')
        else:
            resultDict = self.parsingFcdXML()
            return resultDict
