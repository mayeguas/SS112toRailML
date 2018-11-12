'''
Created on 5 jun. 2018

@author: Miguel Yeguas
'''

class Coordinate():
    '''
    This class represent a (x,y) coordinate
    '''
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Connection():
    '''
    This class represent a connection in SS112 format
    '''


    def __init__(self, uniqueId, coordinate, kp1, kp2, trackPartId1, trackPartId2, trackPart1=None, trackPart2=None):
        '''
        Constructor
        '''
        self.type = 'connection'
        self.uniqueId = uniqueId
        self.x = coordinate.x
        self.y = coordinate.y
        self.kp1 = int(kp1)
        self.kp2 = int(kp2)
        self.trackPartId1 = trackPartId1
        self.trackPartId2 = trackPartId2
        if (trackPart1 == None):
            self.trackPart1 = ''
        else:
            self.trackPart1 = trackPart1
             
        if (trackPart2 == None):
            self.trackPart2 = ''
        else:
            self.trackPart2 = trackPart2
    
    def setTrackPart1(self, trackPart1):
        self.trackPart1 = trackPart1
    
    def setTrackPart2(self, trackPart2):
        self.trackPart2 = trackPart2
    
    def __lt__(self, other):
        if (self.kp1 == self.kp2 and other.kp1 == other.kp2):
            return self.kp1 < other.kp1 and self.y < other.y
    
    def __eq__(self, other):
        if (self.kp1 == self.kp2 and other.kp1 == other.kp2):
            return self.uniqueId == other.uniqueId
    
class Segment():
    '''
    This class represent a segment element in SS112 format
    '''
    
    def __init__(self, uniqueId, connection1, connection2):
        '''
        Constructor
        '''
        self.type = 'segment'
        self.uniqueId = uniqueId
        self.connection1 = connection1
        self.connection2 = connection2

class End():
    '''
    This class represent a end element in SS112 format
    '''
    
    def __init__(self, uniqueId, connection1):
        '''
        Constructor
        '''
        self.type = 'end'
        self.uniqueId = uniqueId
        self.connection1 = connection1

class Point():
    '''
    This class represent a point element in SS112 format
    '''
    
    def __init__(self, uniqueId, connection1, connection2, connection3):
        '''
        Constructor
        '''
        self.type = 'point'
        self.uniqueId = uniqueId
        self.connection1 = connection1
        self.connection2 = connection2   
        self.connection3 = connection3
