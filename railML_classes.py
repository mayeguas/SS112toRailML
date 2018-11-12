'''
Created on 5 jun. 2018

@author: Miguel Yeguas
'''
import xml.etree.ElementTree as ET

class IntrinsicCoor():
    '''
    This class represent a coordinate in railML format (x, y, kp)
    '''
    
    def __init__(self, x, y, kp=None, lps=None):
        self.x = x
        self.y = y
        
        if (kp == None):
            self.kp = ''
        else:
            self.kp = kp
            
        if (lps == None):
            self.lps = ''
        else:
            self.lps = lps
        
class NetElement():
    '''
    This class represent a netElement in railML format
    '''
    
    def __init__(self, uniqueId, intrinsicCoor_ini, intrinsicCoor_end):
        '''
        Constructor
        '''
        self.uniqueId = uniqueId
        self.lps_ini = intrinsicCoor_ini.lps
        self.kp_ini = str(intrinsicCoor_ini.kp)
        self.x_ini = intrinsicCoor_ini.x
        self.y_ini = intrinsicCoor_ini.y
        self.lps_end = intrinsicCoor_end.lps
        self.kp_end = str(intrinsicCoor_end.kp)
        self.x_end = intrinsicCoor_end.x
        self.y_end = intrinsicCoor_end.y
    
    def buildXMLElement(self, parentElement):
        '''
        Funcion that builds the current element and addes it to a parentElement
        '''
        a = ET.SubElement(parentElement, "netElement", {'id' : self.uniqueId})
        b = ET.SubElement(a, 'associatedPositioningSystem', {'id' : a.get('id') + '_aps01'})
        c = ET.SubElement(b, 'intrinsicCoordinate', {'id' : b.get('id') + '_ic00', 'intrinsicCoord' : '0.0'})
        ET.SubElement(c, 'linearCoordinate', {'positioningSystemRef' : self.lps_ini, 'measure' : self.kp_ini})
        ET.SubElement(c, 'geometricCoordinate', {'positioningSystemRef' : 'screenCoordinatesInPx', 'x' : self.x_ini, 'y' : self.y_ini, 'z' : '0'})
        f = ET.SubElement(b, 'intrinsicCoordinate', {'id' : b.get('id') + '_ic01', 'intrinsicCoord' : '1.0'})
        ET.SubElement(f, 'linearCoordinate', {'positioningSystemRef' : self.lps_end, 'measure' : self.kp_end})
        ET.SubElement(f, 'geometricCoordinate', {'positioningSystemRef' : 'screenCoordinatesInPx', 'x' : self.x_end, 'y' : self.y_end, 'z' : '0'})    

class NetRelation():
    '''
    This class represent a netRelation in railML format
    '''
    
    def __init__(self, netElem0, pos0, netElem1, pos1):
        self.uniqueId = 'nr_' + netElem0 + '_' + netElem1
        self.netElem0 = netElem0
        self.pos0 = pos0
        self.netElem1 = netElem1
        self.pos1 = pos1
    
    def buildXMLElement(self, parentElement):
        '''
        Funcion that builds the current element and addes it to a parentElement
        '''
        a = ET.SubElement(parentElement, "netRelation", {'id' : self.uniqueId, 'positionOnA' : self.pos0, 'positionOnB' : self.pos1})
        ET.SubElement(a, 'elementA', {'ref' : self.netElem0})
        ET.SubElement(a, 'elementB', {'ref' : self.netElem1})

class Track():
    '''
    This class represent a track in railML format
    '''
    
    def __init__(self, uniqueId, netElemRef, bend=None, trackBegin=None, trackEnd=None):
        '''
        Constructor
        '''
        self.uniqueId = uniqueId
        self.netElemRef = netElemRef
        
        if (bend == None):
            self.bend = ''
        else:
            self.bend = bend
            
        if (trackBegin == None):
            self.trackBegin = ''
        else:
            self.trackBegin = trackBegin
            
        if (trackEnd == None):
            self.trackEnd = ''
        else:
            self.trackEnd = trackEnd
        
    def buildXMLElement(self, parentElement):
        '''
        Funcion that builds the current element and addes it to a parentElement
        '''
        a = ET.SubElement(parentElement, "track", {'id' : self.uniqueId})
        b = ET.SubElement(a, 'linearLocation', {'id' : a.get('id') + '_linloc01'})
        ET.SubElement(b, 'associatedElement', {'netElementRef' : self.netElemRef, 'intrinsicCoordBegin' : '0.0', 'intrinsicCoordEnd': '1.0'})
        if (self.bend):
            for bend in self.bend:
                ET.SubElement(b, 'geometricCoordinate', {'positioningSystemRef' : 'screenCoordinatesInPx', 'x' : bend.x, 'y' : bend.y})
        ET.SubElement(a, 'trackBegin', {'ref' :  self.trackBegin})
        ET.SubElement(a, 'trackEnd', {'ref' :  self.trackEnd})
    
    def setTrackBegin(self, trackBegin):
        self.trackBegin = trackBegin
        
    def setTrackEnd(self, trackEnd):
        self.trackEnd = trackEnd  

class BufferStop():
    '''
    This class represent a buffer stop in railML format
    '''
    
    def __init__(self, uniqueId, position, netElemRef=None):
        '''
        Constructor
        '''
        self.uniqueId = uniqueId
        self.position = position
        
        if (netElemRef == None):
            self.netElemRef = ''
        else:
            self.netElemRef = netElemRef
        
    def buildXMLElement(self, parentElement):
        '''
        Funcion that builds the current element and addes it to a parentElement
        '''
        a = ET.SubElement(parentElement, "bufferStop", {'id' : self.uniqueId})
        ET.SubElement(a, 'spotLocation', {'id' : a.get('id') + '_spotloc01', 'netElementRef' : self.netElemRef, 'intrinsicCoord' : self.position}) 
        
            
    def setNetElemRef(self, netElemRef):
        self.netElemRef = netElemRef    
    
class Switch():
    '''
    This class represent a switch in railML format
    '''
    
    def __init__(self, uniqueId, position, netElemRef=None, leftNetRelation=None, rightNetRelation=None):
        '''
        Constructor
        '''
        self.uniqueId = uniqueId
        self.position = position
        
        if (netElemRef == None):
            self.netElemRef = ''
        else:
            self.netElemRef = netElemRef
            
        if (leftNetRelation == None):
            self.leftNetRelation = ''
        else:
            self.leftNetRelation = leftNetRelation
        if (rightNetRelation == None):
            self.rightNetRelation = ''
        else:
            self.rightNetRelation = rightNetRelation    
    
    def buildXMLElement(self, parentElement):
        '''
        Funcion that builds the current element and addes it to a parentElement
        '''
        a = ET.SubElement(parentElement, "switch", {'id' : self.uniqueId})
        ET.SubElement(a, 'spotLocation', {'id' : a.get('id') + '_spotloc01', 'netElementRef' : self.netElemRef, 'intrinsicCoord' : self.position})
        ET.SubElement(a, 'leftBranch', {'netRelationRef' : self.leftNetRelation})
        ET.SubElement(a, 'rightBranch', {'netRelationRef' : self.rightNetRelation})
    
    def setNetElemRef(self, netElemRef):
        self.netElemRef = netElemRef
    
    def setLeftNetRelation(self, netRelation):
        self.leftNetRelation = netRelation 
    
    def setRightNetRelation(self, netRelation):
        self.rightNetRelation = netRelation 