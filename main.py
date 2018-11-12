import xml.etree.ElementTree as ET

from ss112_classes import Connection, Coordinate, Segment, End, Point

from railML_classes import NetElement, IntrinsicCoor, Track, BufferStop, Switch, NetRelation
from _sqlite3 import connect

ss112File = "TopologyBMB_v360.xml"

ss112_tree = ET.parse(ss112File)
ss112_tag = ss112_tree.getroot()

# Diccionario que contiene el id de los elementos como clave y la instancia de la clase como valor
elements = {}

# Lista de instancias de conectores creados
connections = []
    
for connector in ss112_tag.iter('connections'):
    for child in connector.iter():
        if child.tag == 'id':
            uniqueId = child.text
        if child.tag == 'kp1':
            kp1 = child.text
        if child.tag == 'kp2':
            kp2 = child.text
        if child.tag == 'trackPartId1':
            trackPartId1 = child.text
        if child.tag == 'trackPartId2':
            trackPartId2 = child.text
        if child.tag == 'coordinate':
            for grandchild in child.iter():
                if grandchild.tag == 'x':
                    #connection['x'] = (int(grandchild.text) - 230100) / 2.5
                    x = grandchild.text
                if grandchild.tag == 'y':
                    #connection['y'] = int(grandchild.text)
                    y = grandchild.text
            coordinate = Coordinate(x, y)
    connection = Connection(uniqueId, coordinate, kp1, kp2, trackPartId1, trackPartId2)
    elements[uniqueId] = connection
    connections.append(connection)

# Lista de instancias de segmentos leidos y creados
segments = []

for segmento in ss112_tag.iter('segments'):
    for child in segmento.iter():
        if child.tag == 'id':
            uniqueId = child.text
        if child.tag == 'connection1':
            connection1 = elements[child.text]
        if child.tag == 'connection2':
            connection2 = elements[child.text]
    segment = Segment(uniqueId, connection1, connection2) 
    elements[uniqueId] = segment
    segments.append(segment)

# Lista de instancias de toperas leidos y creados
ends = []

for topera in ss112_tag.iter('ends'):
    for child in topera.iter():
        if child.tag == 'id':
            uniqueId = child.text
        if child.tag == 'connection1':
            connection1 = elements[child.text]
    end = End(uniqueId, connection1) 
    elements[uniqueId] = end
    ends.append(end)

# Lista de instancias de agujas leidos y creados
points = []

for desvio in ss112_tag.iter('points'):
    for child in desvio.iter():
        if child.tag == 'id':
            uniqueId = child.text
        if child.tag == 'connection1':
            connection1 = elements[child.text]
        if child.tag == 'connection2':
            connection2 = elements[child.text]
        if child.tag == 'connection3':
            connection3 = elements[child.text]
    point = Point(uniqueId, connection1, connection2, connection3) 
    elements[uniqueId] = point
    points.append(point)

# Anadimos a las instancias de conectores la instancia del elemento referenciado en el conector
for connection in connections:
    connection.setTrackPart1(elements[connection.trackPartId1])
    connection.setTrackPart2(elements[connection.trackPartId2])
    if (connection.kp1 != connection.kp2):
        print("cambio de kp en conector" + connection.uniqueId)
        
connections.sort()

# Usando la informacion de los conectores creamos netElements en formato railML
lps = 'lps01'

#newFile = './newFile.xml'
newFile = ss112File[:-4]+'_railML3.xml'
railML_tag = ET.Element('railML')
railML_tree = ET.ElementTree(railML_tag)

infrastructure_tag = ET.SubElement(railML_tag, 'infrastructure')
topology_tag = ET.SubElement(infrastructure_tag, 'topology')
netElements_tag = ET.SubElement(topology_tag, 'netElements')
netRelations_tag = ET.SubElement(topology_tag, 'netRelations')
functionalInfrastructure_tag = ET.SubElement(infrastructure_tag, 'functionalInfrastructure')
tracks_tag = ET.SubElement(functionalInfrastructure_tag, 'tracks')
bufferStop_tag = ET.SubElement(functionalInfrastructure_tag, 'bufferStops')
switch_tag = ET.SubElement(functionalInfrastructure_tag, 'switches')

netElements = []
tracks = []
switches = []
bufferStops = []

getBufferStopById = {}
getSwitchById = {}
getNetElementById = {}
getTrackById = {}

segmentId2netElement = {}
point2switch = {}
segment2track = {}
segment2netElem = {}


for connection in connections:
    
    if (connection.trackPart1.type == 'end'):
        uniqueId = connection.trackPartId1
        position = '0.0'
        netElemRef = 'ne_' + connection.trackPartId2 if (connection.trackPart2.type == 'segment') else None
        bufferStop = BufferStop(uniqueId, position, netElemRef)
        getBufferStopById[uniqueId] = bufferStop
        bufferStops.append(bufferStop)
        bufferStop.buildXMLElement(bufferStop_tag)
        
    elif (connection.trackPart1.type == 'point' and connection.uniqueId == connection.trackPart1.connection1.uniqueId):
        point = connection.trackPart1
        uniqueId = connection.trackPartId1
        position = '0.0'
        netElemRef = 'ne_' + connection.trackPartId2 if (connection.trackPart2.type == 'segment') else None
        switch = Switch(uniqueId, position, netElemRef)
        getSwitchById[uniqueId] = switch
        switches.append(switch)
        switch.buildXMLElement(switch_tag)
    
    # elif(connection.trackPart1.type == 'segment'):
    
    if (connection.trackPart2.type == 'end'):
        uniqueId = connection.trackPartId2
        position = '1.0'
        netElemRef = 'ne_' + connection.trackPartId1 if (connection.trackPart1.type == 'segment') else None
        bufferStop = BufferStop(uniqueId, position, netElemRef)
        getBufferStopById[uniqueId] = bufferStop
        bufferStops.append(bufferStop)
        bufferStop.buildXMLElement(bufferStop_tag)
        
    elif (connection.trackPart2.type == 'point' and connection.uniqueId == connection.trackPart2.connection1.uniqueId):
        uniqueId = connection.trackPartId2
        position = '1.0'
        netElemRef = 'ne_' + connection.trackPartId1 if (connection.trackPart1.type == 'segment') else None
        switch = Switch(uniqueId, position, netElemRef)
        getSwitchById[uniqueId] = switch
        switches.append(switch)
        switch.buildXMLElement(switch_tag)
        
    elif(connection.trackPart2.type == 'segment'):
        
        segment = connection.trackPart2
        
        uniqueId = 'ne_' + connection.trackPartId2
        
        intrinsicCoor_ini = IntrinsicCoor(connection.x, 
                                      connection.y,
                                      connection.kp2,
                                      lps)
        
        
        intrinsicCoor_end = IntrinsicCoor(segment.connection2.x, 
                                      segment.connection2.y,
                                      segment.connection2.kp1,
                                      lps)
        
        netElement = NetElement(uniqueId, intrinsicCoor_ini, intrinsicCoor_end)
        getNetElementById[uniqueId] = netElement
        netElements.append(netElement)
        netElement.buildXMLElement(netElements_tag)
        
        track = Track(segment.uniqueId, netElement.uniqueId, bend=None, trackBegin=segment.connection1.trackPartId1, trackEnd=segment.connection1.trackPartId2)
        getTrackById[track.uniqueId] = track
        tracks.append(track)
        track.buildXMLElement(tracks_tag)


railML_tree.write(newFile)
    
        
"""
counter = 1

for segment in segments:
    
    # Creamos una lista de puntos para el caso de que el segmento contenga curvas
    bends = []
    
    # Comprobamos que los elementos que rodean al segmento son un desvio o una topera
    if (
        (segment.connection1.trackPart1.type == 'point' or segment.connection1.trackPart1.type == 'end') and
        (segment.connection2.trackPart2.type == 'point' or segment.connection2.trackPart2.type == 'end')):
        
        # En este caso creamos el netElement coincidente con el segmento
        
        uniqueId = 'ne%0*d' % (3, counter) # Formato ne001
        
        intrinsicCoor_ini = IntrinsicCoor(segment.connection1.x, 
                                      segment.connection1.y,
                                      segment.connection1.kp2,
                                      lps)
        intrinsicCoor_end = IntrinsicCoor(segment.connection2.x, 
                                      segment.connection2.y,
                                      segment.connection2.kp1,
                                      lps)
        
        netElement = NetElement(uniqueId, intrinsicCoor_ini, intrinsicCoor_end)
        
        segmentId2netElement[segment.uniqueId] = netElement
        
        netElements.append(netElement)
        
    # Si el elemento a la izquierda del segmento actual es un segmento
    elif (segment.connection1.trackPart1.type == 'segment'):
        
        # insertamos como curva el punto de la conexion 1
        bend = IntrinsicCoor(segment.connection1.x, segment.connection1.y)
        bends.append(bend)
        
        
        
        
       
        uniqueId = segment.connection1.trackPart1.uniqueId
        netElemRef = netElement.uniqueId
        position = '0.0'
        switch = Switch(uniqueId, netElemRef, position)
        point2switch[uniqueId] = elements[uniqueId]
        switches.append(switch)
        
    elif (segment.connection1.trackPart1.type == 'end'):
        uniqueId = segment.connection1.trackPart1.uniqueId
        netElemRef = netElement.uniqueId
        position = '0.0'
        bufferStop = BufferStop(uniqueId, netElemRef, position)
        end2bufferStop[uniqueId] = bufferStop
        bufferStop.buildXMLElement(bufferStop_tag)
        bufferStops.append(bufferStop)
        
    # Comprobamos que tipo de elemento es el trackpart2 de la connection2
    # y lo creamos en el caso de ser topera o desvio
    
    if (segment.connection2.trackPart2.type == 'point'):
        uniqueId = segment.connection2.trackPart2.uniqueId
        netElemRef = netElement.uniqueId
        position = '1.0'
        switch = Switch(uniqueId, netElemRef, position)
        point2switch[uniqueId] = elements[uniqueId]
        switches.append(switch)
        
    elif (segment.connection2.trackPart2.type == 'end'):
        uniqueId = segment.connection2.trackPart2.uniqueId
        netElemRef = netElement.uniqueId
        position = '1.0'
        bufferStop = BufferStop(uniqueId, netElemRef, position)
        end2bufferStop[uniqueId] = bufferStop
        bufferStop.buildXMLElement(bufferStop_tag)
        bufferStops.append(bufferStop)

    
    # Creamos el elemento track equivalente al track
    
    uniqueId = segment.uniqueId
    netElemRef = netElement.uniqueId
    trackBegin = segment.connection1.trackPartId1
    trackEnd = segment.connection2.trackPartId2
    track = Track(uniqueId, netElemRef, trackBegin, trackEnd)
    segment2track[uniqueId] = track
    track.buildXMLElement(tracks_tag)
    tracks.append(track)
    
for switch in switches:
    
    desvio = point2switch[switch.uniqueId]
    print(desvio.uniqueId)
    
    if (switch.position == '0.0'):
        
        print(desvio.connection1.trackPartId2)
        
        connection2_netElem = segment2netElem[desvio.connection2.trackPartId1].uniqueId
        connection3_netElem = segment2netElem[desvio.connection3.trackPartId1].uniqueId
        
        netRelation1 = NetRelation(connection2_netElem, '1', switch.netElemRef, '0')
        netRelation1.buildXMLElement(netRelations_tag)
        switch.setLeftNetRelation(netRelation1.uniqueId)
        
        netRelation2 = NetRelation(connection3_netElem, '1', switch.netElemRef, '0')
        netRelation2.buildXMLElement(netRelations_tag)
        switch.setRightNetRelation(netRelation2.uniqueId)
        
        netRelation3 = NetRelation(connection2_netElem, '1', connection3_netElem, '1')
        netRelation3.buildXMLElement(netRelations_tag)
        
        switch.buildXMLElement(switch_tag)
        
    elif (switch.position == '1.0'):
        
        connection2_netElem = segment2netElem[desvio.connection2.trackPartId2].uniqueId
        connection3_netElem = segment2netElem[desvio.connection3.trackPartId2].uniqueId
        
        netRelation1 = NetRelation(switch.netElemRef, '1', connection2_netElem, '0')
        netRelation1.buildXMLElement(netRelations_tag)
        switch.setLeftNetRelation(netRelation1.uniqueId)
        
        netRelation2 = NetRelation(switch.netElemRef, '1', connection3_netElem, '0')
        netRelation2.buildXMLElement(netRelations_tag)
        switch.setRightNetRelation(netRelation2.uniqueId)
        
        netRelation3 = NetRelation(connection2_netElem, '0', connection3_netElem, '0')
        netRelation3.buildXMLElement(netRelations_tag)
        
        switch.buildXMLElement(switch_tag)
""" 
    
    
    
    
    
    

