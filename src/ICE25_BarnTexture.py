from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, time
import PIL.Image as Image

windowSize = 8

theta = 55
phi = 2
distance = 3
bladeTurn = 0.0
tickTime = 0

objectArray = []
allWindmills = []

mX = 0
mY = 0
mBtn = False
cameraFocus = 0

class Scene:
    posX = 0.0
    posY = 0.0
    posZ = 0.0
    
    axisColor = (0.5, 0.5, 0.5, 0.5)
    axisLength = 6   # Extends to positive and negative on all axes
    landColor = (0.1, 0.5, 0.1, 0.5)
    landLength = 10  # Extends to positive and negative on x and y axis

    def draw(self):
        self.drawAxis()
        self.drawLand()

    def drawAxis(self):
        glColor4f(self.axisColor[0], self.axisColor[1], self.axisColor[2], self.axisColor[3])
        glBegin(GL_LINES)
        glVertex(-self.axisLength, 0, 0)
        glVertex(self.axisLength, 0, 0)
        glVertex(0, -self.axisLength, 0)
        glVertex(0, self.axisLength, 0)
        glVertex(0, 0, -self.axisLength)
        glVertex(0, 0, self.axisLength)
        glEnd()

    def drawLand(self):
        glEnable(GL_TEXTURE_2D)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glBindTexture(GL_TEXTURE_2D, grassTextureID)
        
        glBegin(GL_POLYGON)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(self.landLength, 0, self.landLength)

        glTexCoord2f(0.0, 10.0)
        glVertex3f(self.landLength, 0, -self.landLength)

        glTexCoord2f(10.0, 10.0)
        glVertex3f(-self.landLength, 0, -self.landLength)

        glTexCoord2f(10.0, 0.0)
        glVertex3f(-self.landLength, 0, self.landLength)
        glEnd()

        glDisable(GL_TEXTURE_2D)

    def getPos(self):
        return (self.posX, self.posY, self.posZ)        

class Windmill:
    posX = 0.0
    posY = 0.0
    posZ = 0.0

    sX = 1.0
    sY = 1.0
    sZ = 1.0

    rotate = 0.0

    height = 1.5

    fanBlades = 8
    fanBladeTurn = 0.0

    def __init__(self, startX, startY, startZ, rotateTheta=0.0, scaleX=1.0, scaleY=1.0, scaleZ=1.0):
        global allWindmills        
        
        self.posX = startX
        self.posY = startY
        self.posZ = startZ

        self.rotate = rotateTheta

        self.sX = scaleX
        self.sY = scaleY
        self.sZ = scaleZ

        allWindmills.append(self)
        

    def draw(self):
        glPushMatrix()
        glTranslatef(self.posX + 0.15 * self.sX, self.posY, self.posZ + 0.15 * self.sZ)
        glRotatef(self.rotate, 0, 1, 0)
        glScalef(self.sX, self.sY, self.sZ)

        glColor(1.0, 0.0, 0.0, 0.5)
        glBegin(GL_POLYGON)
        glVertex3f(-0.3, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(-0.1, self.height, -0.1)
        glVertex3f(-0.2, self.height, -0.1)
        glEnd()
        
        glBegin(GL_POLYGON)
        glColor(1, 1, 0, 0.5)
        glVertex3f(-0.3, 0, 0)
        glVertex3f(-0.2, self.height, -0.1)
        glVertex3f(-0.2, self.height, -0.2)
        glVertex3f(-0.3, 0, -0.3)    
        glEnd()

        glBegin(GL_POLYGON)
        glColor(0, 1, 0, 0.5)
        glVertex3f(-0.3, 0, -0.3)
        glVertex3f(-0.2, self.height, -0.2)
        glVertex3f(-0.1, self.height, -0.2)
        glVertex3f(0, 0, -0.3)  
        glEnd()

        glBegin(GL_POLYGON)
        glColor(0, 1, 1, 0.5)
        glVertex3f(0, 0, -0.3)
        glVertex3f(-0.1, self.height, -0.2)  
        glVertex3f(-0.1, self.height, -0.1)  
        glVertex3f(0, 0, 0)  
        glEnd()

        self.drawWindmillFan()
        glPopMatrix()

    def drawWindmillFan(self):
        global bladeTurn
        for i in range(self.fanBlades):
            glPushMatrix()
            glTranslatef(-0.15, self.height, 0)
            glRotatef(i * 360 / self.fanBlades + self.fanBladeTurn, 0, 0, 1)
            self.drawWindmillBlade()
            glPopMatrix()

    def drawWindmillBlade(self):
        glBegin(GL_TRIANGLES)
        glColor(1, 0, 1, 0.5)
        glVertex3f(0, 0, 0)
        glVertex3f(0.3, 0.05, 0)
        glVertex3f(0.3, -0.05, 0)    
        glEnd()

    def rotateBlade(self, newTheta):
        self.fanBladeTurn = self.fanBladeTurn + newTheta
        self.fanBladeTurn = self.fanBladeTurn % 360

    def getPos(self):
        return (self.posX, self.posY, self.posZ)        
        

class Barn:
    posX = 0.0
    posY = 0.0
    posZ = 0.0

    sX = 1.0
    sY = 1.0
    sZ = 1.0

    rotate = 0.0    

    def __init__(self, startX, startY, startZ, rotateTheta=0.0, scaleX=1.0, scaleY=1.0, scaleZ=1.0):
        self.posX = startX
        self.posY = startY
        self.posZ = startZ

        self.rotate = rotateTheta

        self.sX = scaleX
        self.sY = scaleY
        self.sZ = scaleZ    

    def draw(self):
        glPushMatrix()
        glTranslatef(self.posX - 0.5, self.posY, self.posZ - 0.5)
        glRotatef(self.rotate, 0, 1, 0)
        glScalef(self.sX, self.sY, self.sZ)

        # Sides of the barn
        
        glBegin(GL_POLYGON)
        glColor4f(1, 0, 0, 0.5)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 0.5, 1)
        glVertex3f(0, 0.5, 0)
        glEnd()

  
        glBegin(GL_POLYGON)
        glColor(1, 1, 0, 0.5)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0.5, 0)
        glVertex3f(1, 0.5, 1)
        glVertex3f(1, 0, 1)    
        glEnd()
        
        # Front and back of the barn
        
        glBegin(GL_POLYGON)
        glColor4f(0, 1, 0, 0.5)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0.5, 0)
        glVertex3f(0.5, 1, 0)
        glVertex3f(1, 0.5, 0)
        glVertex3f(1, 0, 0)
        glEnd()

        glBegin(GL_POLYGON)
        glColor4f(0, 0, 1, 0.5)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 0.5, 1)
        glVertex3f(0.5, 1, 1)
        glVertex3f(1, 0.5, 1)
        glVertex3f(1, 0, 1)
        glEnd()

        
        # Barn roof
        glBegin(GL_POLYGON)
        glColor(1, 0, 1, 0.5)
        glVertex3f(0, 0.5, 0)
        glVertex3f(0, 0.5, 1)
        glVertex3f(0.5, 1, 1)
        glVertex3f(0.5, 1, 0)    
        glEnd()

        glBegin(GL_POLYGON)        
        glColor(0, 1, 1, 0.5)
        glVertex3f(1, 0.5, 0)
        glVertex3f(1, 0.5, 1)
        glVertex3f(0.5, 1, 1)
        glVertex3f(0.5, 1, 0)    
        glEnd()      

        glPopMatrix()

    def getPos(self):
        return (self.posX, self.posY, self.posZ)        

def populateScene():
    global objectArray

    objectArray.append(Scene())
    objectArray.append(Windmill(-2.0, 0.0, 1.0, 90))
    objectArray.append(Barn(0.0, 0.0, 0.0, 0))

def display():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for obj in objectArray:
        obj.draw()

    glutSwapBuffers()


def idle():
    global tickTime, prevTime
    for windmill in allWindmills:
        windmill.rotateBlade(-0.1 * tickTime)
    
    glutPostRedisplay()

    curTime = glutGet(GLUT_ELAPSED_TIME)
    tickTime =  curTime - prevTime
    prevTime = curTime
    

def setView():
    if len(objectArray) != 0:
        lookingAt = objectArray[cameraFocus].getPos()
    else:
        lookingAt = (0, 0, 0)

    newX = distance * math.sin(math.radians(theta)) + lookingAt[0]
    newZ = distance * math.cos(math.radians(theta)) + lookingAt[2]
	
    newY = phi
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.1, 100)
    gluLookAt(newX, newY, newZ, lookingAt[0], lookingAt[1], lookingAt[2], 0, 1, 0)    
    

    glMatrixMode(GL_MODELVIEW)
    
    glutPostRedisplay()

def mouser(btn, state, x, y):
    global mBtn, cameraFocus
    if btn == GLUT_LEFT_BUTTON and state == GLUT_UP:
        cameraFocus += 1
        if cameraFocus == len(objectArray):
            cameraFocus = 0
    if btn == GLUT_RIGHT_BUTTON and state == GLUT_UP:
        cameraFocus -= 1
        if cameraFocus < 0:
            cameraFocus = len(objectArray) - 1
    if btn == GLUT_MIDDLE_BUTTON and state == GLUT_DOWN:
        mBtn = True
    if btn == GLUT_MIDDLE_BUTTON and state == GLUT_UP:
        mBtn = False
    

    setView()

def mouseMotion(x, y):
    global mX, mY, theta, phi, distance
    if mBtn == True:
        dX = x - mX
        dY = y - mY
        theta += dX
        phi += dY * 0.01       
        mX = x
        mY = y      
    else:
        mX = x
        mY = y
    setView()

def mousePassive(x, y):
    global mX, mY
    mX = x
    mY = y

def mouseWheel(button, direction, x, y):
    global mX, mY, distance
    mX = x
    mY = y
    if direction > 0:   # Zoom in
        distance -= 0.1
    else:
        distance += 0.1

    setView()    

### This is a new function to load textures using the PIL (Python Image Library)
def loadTexture(imageName):
    texturedImage = Image.open(imageName)
    try:
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw", "RGBX", 0, -1)
    except Exception, e:
        print "Error:", e
        print "Switching to RGBA mode."
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw", "RGBA", 0, -1)

    tempID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tempID)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, imgX, imgY, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
    return tempID

def loadSceneTextures():
    global grassTextureID
    grassTextureID = loadTexture("road.png")


def main():
    glutInit()

    global prevTime
    prevTime = glutGet(GLUT_ELAPSED_TIME)
    
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(100, 150)
    glutCreateWindow('ICE25: Barn Texture')
    glutDisplayFunc(display)
    glutIdleFunc(idle)

    glutMouseFunc(mouser)
    glutMotionFunc(mouseMotion)
    glutPassiveMotionFunc(mousePassive)
    glutMouseWheelFunc(mouseWheel)

    loadSceneTextures()

    setView()
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)

    #glEnable(GL_BLEND)
    #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    #glBlendFunc(GL_ONE_MINUS_DST_ALPHA,GL_DST_ALPHA)
    #glBlendFuncSeparate(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE_MINUS_SRC_ALPHA)
    populateScene()
    glutMainLoop()
    
main()
