from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time
import ImportObject


class jeep:
    obj = 0
    displayList = 0
    wheel1DL = 0
    wheel2DL = 0
    dimDL = 0
    litDL = 0

    dimL = 0
    litL = 0
    lightOn = False
    
    wheel1 = 0
    wheel2 = 0

    wheelTurn = 0.0
    revWheelTurn = 360.0
    #allWheels=[wheel1,wheel2]

    wheelDir = 'stop'
    
    posX = 0.0
    posY = 1.75
    posZ = 0.0

##    wheel1LocX =0 
##    wheel1LocZ = 0
##    wheel2LocX = 0
##    wheel2LocZ = 0 

    sizeX = 1.0
    sizeY = 1.0
    sizeZ = 1.0

    rotation = 0.0
    
    def __init__(self, color):
        if (color == 'p'):
            self.obj = ImportObject.ImportedObject("../objects/jeepbare")
        elif (color == 'g'):
            self.obj = ImportObject.ImportedObject("../objects/jeepbare2")
        elif (color == 'r'):
            self.obj = ImportObject.ImportedObject("../objects/jeepbare3")
        self.wheel1 = ImportObject.ImportedObject("../objects/frontwheel")
        self.wheel2 = ImportObject.ImportedObject("../objects/backwheel")
        self.dimL = ImportObject.ImportedObject("../objects/dimlight")
        self.litL = ImportObject.ImportedObject("../objects/litlight")
    
    def makeDisplayLists(self):
        self.obj.loadOBJ()
        self.wheel1.loadOBJ()
        self.wheel2.loadOBJ()
        self.dimL.loadOBJ()
        self.litL.loadOBJ()

        self.displayList = glGenLists(1)
        glNewList(self.displayList, GL_COMPILE)
        self.obj.drawObject()
        glEndList()

        self.wheel1DL = glGenLists(1)
        glNewList(self.wheel1DL, GL_COMPILE)
        self.wheel1.drawObject()
        glEndList()

        self.wheel2DL = glGenLists(1)
        glNewList(self.wheel2DL, GL_COMPILE)
        self.wheel2.drawObject()
        glEndList()

        self.dimDL = glGenLists(1)
        glNewList(self.dimDL, GL_COMPILE)
        self.dimL.drawObject()
        glEndList()

        self.litDL = glGenLists(1)
        glNewList(self.litDL, GL_COMPILE)
        self.litL.drawObject()
        glEndList()
        
    
    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.posX,self.posY,self.posZ)
        glRotatef(self.rotation,0.0,1.0,0.0)
        glScalef(self.sizeX,self.sizeY,self.sizeZ)

        glCallList(self.displayList)
        glPopMatrix()

    def drawW1(self):
        glPushMatrix()

        glTranslatef(self.posX, self.posY-1.3146, self.posZ)
        glRotatef(self.rotation,0.0,1.0,0.0)
        glTranslatef(0.0, self.posY-1.3146, 2.9845)
        glScalef(self.sizeX, self.sizeY, self.sizeZ)
        
        if self.wheelDir == 'fwd': 
            glRotatef(self.revWheelTurn,1.0,0.0,0.0)
        elif self.wheelDir == 'back':
            glRotatef(self.wheelTurn,1.0,0.0,0.0)
    
        glTranslatef(0.0,1.3146,-2.9845)
        
        glCallList(self.wheel1DL)
        glPopMatrix()

    def drawW2(self):
        glPushMatrix()
        
        glTranslatef(self.posX, self.posY-1.3146, self.posZ)
        glRotatef(self.rotation,0.0,1.0,0.0)
        glTranslatef(0.0, self.posY-1.3146, -2.9845)
        glScalef(self.sizeX, self.sizeY, self.sizeZ)
        
        if self.wheelDir == 'fwd': 
            glRotatef(self.revWheelTurn,1.0,0.0,0.0)
        elif self.wheelDir == 'back':
            glRotatef(self.wheelTurn,1.0,0.0,0.0)
    
        glTranslatef(0.0,1.3146,3.3)

        glCallList(self.wheel2DL)
        glPopMatrix()

    def rotateWheel(self, newTheta):
        global wheelTurn
        self.wheelTurn = self.wheelTurn + newTheta
        self.wheelTurn = self.wheelTurn % 360
        self.revWheelTurn = 360 - self.wheelTurn

    def drawLight(self):
        glPushMatrix()

        glTranslatef(self.posX, self.posY, self.posZ)
        glRotatef(self.rotation,0.0,1.0,0.0)
        glScalef(self.sizeX, self.sizeY, self.sizeZ)

        if self.lightOn == True:
            glCallList(self.litDL)
        elif self.lightOn == False:
            glCallList(self.dimDL)

        glPopMatrix()
  
    def move(self, rot, val): 
        if rot == False: 
            self.posZ += val * math.cos(math.radians(self.rotation)) #must make more sophisticated to go in direction
            self.posX += val * math.sin(math.radians(self.rotation))
##            self.wheel1LocZ += val * math.cos(math.radians(self.rotation))
##            self.wheel1LocX += val * math.sin(math.radians(self.rotation))
##            self.wheel2LocZ += val * math.cos(math.radians(self.rotation))
##            self.wheel2LocX += val * math.sin(math.radians(self.rotation))
        elif rot == True: 
            self.rotation+= val


        
        
