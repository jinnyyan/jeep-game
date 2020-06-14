import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
## Avoid conflict with Python open
from PIL.Image import open as imageOpen

## This class is used to create an object from geometry and materials
##  saved to a file in WaveFront object format.  The object exported
##  from Blender must have the normals included.  
class ImportedObject:
    ## Constructor that includes storage for geometry and materials
    ##  for an object.
    def __init__(self, fileName, setAmbient = 0.9, verbose = False):        
        self.faces = []
        self.verts = []
        self.norms = []
        self.texCoords = []
        self.materials = []
        self.fileName = fileName        
        self.setAmbient = False
        self.hasTex = False
        ## Set this value to False before loading if the model is flat
        self.isSmooth = True
        self.verbose = verbose

    ## Load the material properties from the file
    def loadMat(self):
        ## Open the material file
        with open((self.fileName + ".mtl"), "r") as matFile:
            ## Load the material properties into tempMat
            tempMat = []
            for line in matFile:
                ## Break the line into its components
                vals = line.split()
                ## Make sure there's something in the line (not blank)
                if len(vals) > 0 :
                    ## Record that a new material is being applied
                    if vals[0] == "newmtl":
                        n = vals[1]
                        tempMat.append(n)
                    ## Load the specular exponent
                    elif vals[0] == "Ns":                        
                        n = vals[1]  
                        tempMat.append(float(n))
                    ## Load the diffuse values
                    elif vals[0] == "Kd":  
                        n = map(float, vals[1:4])  
                        tempMat.append(n)
                        ## if self.setAmbient is False, ignore ambient values
                        ## and load diffuse values twice to set the ambient
                        ## equal to diffuse
                        if self.setAmbient:
                            tempMat.append(n)
                    ## load the ambient values (if not overridden)
                    elif vals[0] == "Ka" and not self.setAmbient:  
                        n = map(float, vals[1:4])  
                        tempMat.append(n)
                    ## load the specular values
                    elif vals[0] == "Ks":  
                        n = map(float, vals[1:4])  
                        tempMat.append(n)
                        tempMat.append(None)
                        ## specular is the last line loaded for the material
                        self.materials.append(tempMat)
                        tempMat = []
                    ## load texture file info
                    elif vals[0] == "map_Kd":
                        ## record the texture file name
                        fileName = vals[1]                        
                        self.materials[-1][5]=(self.loadTexture(fileName))                        
                        self.hasTex = True
                        
        if self.verbose:             
            print("Loaded " + self.fileName + \
                  ".mtl with " + str(len(self.materials)) + " materials")

    ## Load the object geometry.
    def loadOBJ(self):
        ## parse the materials file first so we know when to apply materials
        ## and textures
        self.loadMat()
        numFaces = 0
        with open((self.fileName + ".obj"), "r") as objFile:
            for line in objFile:
                ## Break the line into its components
                vals = line.split()
                if len(vals) > 0:
                    ## Load vertices
                    if vals[0] == "v":  
                        v = map(float, vals[1:4])  
                        self.verts.append(v)
                    ## Load normals
                    elif vals[0] == "vn":  
                        n = map(float, vals[1:4])  
                        self.norms.append(n)
                    ## Load texture coordinates
                    elif vals[0] == "vt":
                        t = map(float, vals[1:3])
                        self.texCoords.append(t)
                    ## Load materials. Set index to -1!
                    elif vals[0] == "usemtl":
                        m = vals[1]
                        self.faces.append([-1, m, numFaces])
                    ## Load the faces
                    elif vals[0] == "f":
                        tempFace = []
                        for f in vals[1:]:
                            ## face entries have vertex/tex coord/normal
                            w = f.split("/")
                            ## Vertex required, but should work if texture or
                            ## normal is missing 
                            if w[1] != '' and w[2] != '':
                                tempFace.append([int(w[0])-1,
                                                 int(w[1])-1,
                                                 int(w[2])-1])
                            elif w[1] != '':
                                tempFace.append([int(w[0])-1,
                                                 int(w[1])-1], -1)                                
                            elif w[2] != '':                            
                                tempFace.append([int(w[0])-1, -1,
                                                 int(w[2])-1])
                            else :
                                tempFace.append([int(w[0])-1,-1, -1])

                        self.faces.append(tempFace)                        

        if self.verbose:
            print("Loaded " + self.fileName + ".obj with " + \
                  str(len(self.verts)) + " vertices, " + \
                  str(len(self.norms)) + " normals, and " + \
                  str(len(self.faces)) + " faces")                


    ## Draws the object
    def drawObject(self):
        if self.hasTex:
            GL.glEnable(GL.GL_TEXTURE_2D) 
            ## Use GL.GL_MODULATE instead of GL.GL_DECAL to retain lighting
            GL.glTexEnvf(GL.GL_TEXTURE_ENV,
                         GL.GL_TEXTURE_ENV_MODE,
                         GL.GL_MODULATE)
            
        ## *****************************************************************
        ## Change GL.GL_FRONT to GL.GL_FRONT_AND_BACK if faces are missing
        ## (or fix the normals in the model so they point in the correct
        ## direction)
        ## *****************************************************************
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)                    
        for face in self.faces:
            ## Check if a material
            if face[0] == -1:
               self.setModelColor(face[1])
            else:
               
               GL.glBegin(GL.GL_POLYGON)
               ## drawing normal, then texture, then vertice coords.  
               for f in face:
                   if f[2] != -1:
                       GL.glNormal3f(self.norms[f[2]][0],
                                     self.norms[f[2]][1],
                                     self.norms[f[2]][2])
                   if f[1] != -1:
                       GL.glTexCoord2f(self.texCoords[f[1]][0],
                                       self.texCoords[f[1]][1])              
                   GL.glVertex3f(self.verts[f[0]][0],
                                 self.verts[f[0]][1],
                                 self.verts[f[0]][2])
               GL.glEnd()
        ## Turn off texturing (global state variable again)
        GL.glDisable(GL.GL_TEXTURE_2D)        

    ## Finds the matching material properties and sets them.  
    def setModelColor(self, material):
        mat = []
        for tempMat in self.materials:
            if tempMat[0] == material:
                mat = tempMat
                ## found it, break out.
                break

        ## Set the color for the case when lighting is turned off.  Using 
        ##  the diffuse color, since the diffuse component best describes
        ##  the object color.
        GL.glColor3f(mat[3][0], mat[3][1],mat[3][2])    
        ## Set the model to smooth or flat depending on the attribute setting
        if self.isSmooth:
            GL.glShadeModel(GL.GL_SMOOTH)
        else:
            GL.glShadeModel(GL.GL_FLAT)
        ## The RGBA values for the specular light intesity.  The alpha value
        ## (1.0) is ignored unless blending is enabled.   
        mat_specular = [mat[4][0], mat[4][1], mat[4][2], 1.0]
        ## The RGBA values for the diffuse light intesity.  The alpha value
        ## (1.0) is ignored unless blending is enabled.   
        mat_diffuse = [mat[3][0], mat[3][1],mat[3][2], 1.0]
        ## The value for the specular exponent.  The higher the value, the
        ## "tighter" the specular highlight.  Valid values are [0.0, 128.0]   
        mat_ambient = [mat[2][0], mat[2][1], mat[2][2],1.0]
        ## The value for the specular exponent.  The higher the value, the
        ## "tighter" the specular highlight.  Valid values are [0.0, 128.0]   
        mat_shininess = 0.128*mat[1]
        ## Set the material specular values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_specular)
        ## Set the material shininess values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess)
        ## Set the material diffuse values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, mat_diffuse)
        ## Set the material ambient values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, mat_ambient)
        ## See if there is a texture and bind it if it's there
        if mat[5] != None:
            GL.glBindTexture(GL.GL_TEXTURE_2D, mat[5])
                        

    ## Load a texture from the provided image file name
    def loadTexture(self, texFile):
        if self.verbose:
            print("Loading " + texFile)
        ## Open the image file
        texImage = imageOpen(texFile)        
        try:
            ix, iy, image = texImage.size[0], \
                            texImage.size[1], \
                            texImage.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = texImage.size[0], \
                            texImage.size[1], \
                            texImage.tobytes("raw", "RGBX", 0, -1)
        ## GL.glGenTextures() and GL.glBindTexture() name and create a texture
        ## object for a texture image
        tempID = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, tempID)
        ## The four calls to GL.glTexParameter*() specify how the texture is to
        ## be wrapped and how the colors are to be filtered if there isn't an
        ## exact match between pixels in the texture and pixels on the screen
        ## Values for GL.GL_TEXTURE_WRAP_S and GL.GL_TEXTURE_WRAP_T are
        ## GL.GL_REPEAT and GL.GL_CLAMP
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_WRAP_S,
                           GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_WRAP_T,
                           GL.GL_REPEAT)
        ## The MAG_FILTER has values of GL.GL_NEAREST and GL.GL_LINEAR.  There
        ## are many choices for values for the MIN_FILTER.  GL.GL_NEAREST has
        ## more pixelation, but is the fastest
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_MAG_FILTER,
                           GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_MIN_FILTER,
                           GL.GL_NEAREST)
        ## Store the pixel data
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT,1)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                        GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image)
        return tempID                    
         
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
## Avoid conflict with Python open
from PIL.Image import open as imageOpen

## This class is used to create an object from geometry and materials
##  saved to a file in WaveFront object format.  The object exported
##  from Blender must have the normals included.  
class ImportedObject:
    ## Constructor that includes storage for geometry and materials
    ##  for an object.
    def __init__(self, fileName, setAmbient = 0.9, verbose = False):        
        self.faces = []
        self.verts = []
        self.norms = []
        self.texCoords = []
        self.materials = []
        self.fileName = fileName        
        self.setAmbient = False
        self.hasTex = False
        ## Set this value to False before loading if the model is flat
        self.isSmooth = True
        self.verbose = verbose

    ## Load the material properties from the file
    def loadMat(self):
        ## Open the material file
        with open((self.fileName + ".mtl"), "r") as matFile:
            ## Load the material properties into tempMat
            tempMat = []
            for line in matFile:
                ## Break the line into its components
                vals = line.split()
                ## Make sure there's something in the line (not blank)
                if len(vals) > 0 :
                    ## Record that a new material is being applied
                    if vals[0] == "newmtl":
                        n = vals[1]
                        tempMat.append(n)
                    ## Load the specular exponent
                    elif vals[0] == "Ns":                        
                        n = vals[1]  
                        tempMat.append(float(n))
                    ## Load the diffuse values
                    elif vals[0] == "Kd":  
                        n = map(float, vals[1:4])  
                        tempMat.append(n)
                        ## if self.setAmbient is False, ignore ambient values
                        ## and load diffuse values twice to set the ambient
                        ## equal to diffuse
                        if self.setAmbient:
                            tempMat.append(n)
                    ## load the ambient values (if not overridden)
                    elif vals[0] == "Ka" and not self.setAmbient:  
                        n = map(float, vals[1:4])  
                        tempMat.append(n)
                    ## load the specular values
                    elif vals[0] == "Ks":  
                        n = map(float, vals[1:4])  
                        tempMat.append(n)
                        tempMat.append(None)
                        ## specular is the last line loaded for the material
                        self.materials.append(tempMat)
                        tempMat = []
                    ## load texture file info
                    elif vals[0] == "map_Kd":
                        ## record the texture file name
                        fileName = vals[1]                        
                        self.materials[-1][5]=(self.loadTexture(fileName))                        
                        self.hasTex = True
                        
        if self.verbose:             
            print("Loaded " + self.fileName + \
                  ".mtl with " + str(len(self.materials)) + " materials")

    ## Load the object geometry.
    def loadOBJ(self):
        ## parse the materials file first so we know when to apply materials
        ## and textures
        self.loadMat()
        numFaces = 0
        with open((self.fileName + ".obj"), "r") as objFile:
            for line in objFile:
                ## Break the line into its components
                vals = line.split()
                if len(vals) > 0:
                    ## Load vertices
                    if vals[0] == "v":  
                        v = map(float, vals[1:4])  
                        self.verts.append(v)
                    ## Load normals
                    elif vals[0] == "vn":  
                        n = map(float, vals[1:4])  
                        self.norms.append(n)
                    ## Load texture coordinates
                    elif vals[0] == "vt":
                        t = map(float, vals[1:3])
                        self.texCoords.append(t)
                    ## Load materials. Set index to -1!
                    elif vals[0] == "usemtl":
                        m = vals[1]
                        self.faces.append([-1, m, numFaces])
                    ## Load the faces
                    elif vals[0] == "f":
                        tempFace = []
                        for f in vals[1:]:
                            ## face entries have vertex/tex coord/normal
                            w = f.split("/")
                            ## Vertex required, but should work if texture or
                            ## normal is missing 
                            if w[1] != '' and w[2] != '':
                                tempFace.append([int(w[0])-1,
                                                 int(w[1])-1,
                                                 int(w[2])-1])
                            elif w[1] != '':
                                tempFace.append([int(w[0])-1,
                                                 int(w[1])-1], -1)                                
                            elif w[2] != '':                            
                                tempFace.append([int(w[0])-1, -1,
                                                 int(w[2])-1])
                            else :
                                tempFace.append([int(w[0])-1,-1, -1])

                        self.faces.append(tempFace)                        

        if self.verbose:
            print("Loaded " + self.fileName + ".obj with " + \
                  str(len(self.verts)) + " vertices, " + \
                  str(len(self.norms)) + " normals, and " + \
                  str(len(self.faces)) + " faces")                


    ## Draws the object
    def drawObject(self):
        if self.hasTex:
            GL.glEnable(GL.GL_TEXTURE_2D) 
            ## Use GL.GL_MODULATE instead of GL.GL_DECAL to retain lighting
            GL.glTexEnvf(GL.GL_TEXTURE_ENV,
                         GL.GL_TEXTURE_ENV_MODE,
                         GL.GL_MODULATE)
            
        ## *****************************************************************
        ## Change GL.GL_FRONT to GL.GL_FRONT_AND_BACK if faces are missing
        ## (or fix the normals in the model so they point in the correct
        ## direction)
        ## *****************************************************************
        GL.glPolygonMode(GL.GL_FRONT, GL.GL_FILL)                    
        for face in self.faces:
            ## Check if a material
            if face[0] == -1:
               self.setModelColor(face[1])
            else:
               
               GL.glBegin(GL.GL_POLYGON)
               ## drawing normal, then texture, then vertice coords.  
               for f in face:
                   if f[2] != -1:
                       GL.glNormal3f(self.norms[f[2]][0],
                                     self.norms[f[2]][1],
                                     self.norms[f[2]][2])
                   if f[1] != -1:
                       GL.glTexCoord2f(self.texCoords[f[1]][0],
                                       self.texCoords[f[1]][1])              
                   GL.glVertex3f(self.verts[f[0]][0],
                                 self.verts[f[0]][1],
                                 self.verts[f[0]][2])
               GL.glEnd()
        ## Turn off texturing (global state variable again)
        GL.glDisable(GL.GL_TEXTURE_2D)        

    ## Finds the matching material properties and sets them.  
    def setModelColor(self, material):
        mat = []
        for tempMat in self.materials:
            if tempMat[0] == material:
                mat = tempMat
                ## found it, break out.
                break

        ## Set the color for the case when lighting is turned off.  Using 
        ##  the diffuse color, since the diffuse component best describes
        ##  the object color.
        GL.glColor3f(mat[3][0], mat[3][1],mat[3][2])    
        ## Set the model to smooth or flat depending on the attribute setting
        if self.isSmooth:
            GL.glShadeModel(GL.GL_SMOOTH)
        else:
            GL.glShadeModel(GL.GL_FLAT)
        ## The RGBA values for the specular light intesity.  The alpha value
        ## (1.0) is ignored unless blending is enabled.   
        mat_specular = [mat[4][0], mat[4][1], mat[4][2], 1.0]
        ## The RGBA values for the diffuse light intesity.  The alpha value
        ## (1.0) is ignored unless blending is enabled.   
        mat_diffuse = [mat[3][0], mat[3][1],mat[3][2], 1.0]
        ## The value for the specular exponent.  The higher the value, the
        ## "tighter" the specular highlight.  Valid values are [0.0, 128.0]   
        mat_ambient = [mat[2][0], mat[2][1], mat[2][2],1.0]
        ## The value for the specular exponent.  The higher the value, the
        ## "tighter" the specular highlight.  Valid values are [0.0, 128.0]   
        mat_shininess = 0.128*mat[1]
        ## Set the material specular values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, mat_specular)
        ## Set the material shininess values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, mat_shininess)
        ## Set the material diffuse values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, mat_diffuse)
        ## Set the material ambient values for the polygon front faces.   
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, mat_ambient)
        ## See if there is a texture and bind it if it's there
        if mat[5] != None:
            GL.glBindTexture(GL.GL_TEXTURE_2D, mat[5])
                        

    ## Load a texture from the provided image file name
    def loadTexture(self, texFile):
        if self.verbose:
            print("Loading " + texFile)
        ## Open the image file
        texImage = imageOpen(texFile)        
        try:
            ix, iy, image = texImage.size[0], \
                            texImage.size[1], \
                            texImage.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = texImage.size[0], \
                            texImage.size[1], \
                            texImage.tobytes("raw", "RGBX", 0, -1)
        ## GL.glGenTextures() and GL.glBindTexture() name and create a texture
        ## object for a texture image
        tempID = GL.glGenTextures(1)
        GL.glBindTexture(GL.GL_TEXTURE_2D, tempID)
        ## The four calls to GL.glTexParameter*() specify how the texture is to
        ## be wrapped and how the colors are to be filtered if there isn't an
        ## exact match between pixels in the texture and pixels on the screen
        ## Values for GL.GL_TEXTURE_WRAP_S and GL.GL_TEXTURE_WRAP_T are
        ## GL.GL_REPEAT and GL.GL_CLAMP
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_WRAP_S,
                           GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_WRAP_T,
                           GL.GL_REPEAT)
        ## The MAG_FILTER has values of GL.GL_NEAREST and GL.GL_LINEAR.  There
        ## are many choices for values for the MIN_FILTER.  GL.GL_NEAREST has
        ## more pixelation, but is the fastest
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_MAG_FILTER,
                           GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D,
                           GL.GL_TEXTURE_MIN_FILTER,
                           GL.GL_NEAREST)
        ## Store the pixel data
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT,1)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                        GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image)
        return tempID                    
         
