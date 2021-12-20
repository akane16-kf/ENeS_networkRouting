#!/usr/bin/env python
import sys
from xml.etree.ElementTree import iterparse

def SomeFunction_at_the_end_of_each_timestep(veh_buf):
    return len(veh_buf) # number of vehicles

def SUMOTraceParser(FCDOutput):
    doc = iterparse(FCDOutput, events=('start', 'end'))
    # Skip the root element
    event, root =  next(doc)
    for event, elem in doc:
        if event == 'start':
            if elem.tag == 'timestep':
                t = float(elem.attrib['time'])
                veh_buf = []
                
            elif elem.tag == 'vehicle':
                id = int(elem.attrib['id'])
                x = float(elem.attrib['x'])
                y = float(elem.attrib['y'])                
                # angle = float(elem.attrib['angle'])
                # v = float(elem.attrib['speed'])                

                # print("vehicle id:%d, pos(%f,%f)"%(id,x,y))
                veh_buf.append((x,y))
                
        elif event == 'end':
            if elem.tag == 'timestep':
                elem.clear()
                root.clear()

                n = SomeFunction_at_the_end_of_each_timestep(veh_buf)
                print("time:%d, number of vehicles:%d"%(t,n))

###
if __name__=='__main__':

    FCDOutput = 'sumoTrace.txt'
    SUMOTraceParser(FCDOutput)
        


