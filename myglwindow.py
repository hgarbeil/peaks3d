from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

class MyGLWindow (QOpenGLWidget) :


    def __init__(self,parent):
        QOpenGLWidget.__init__(self,parent)

        self.setpts = False
        self.rotx = 0.
        self.roty = 0.
        self.scalfac = 1.
        self.lastx = -10
        self.curpos = -10
        self.light_position = [1., 1., -2., 0.]
        self.selFlag = False
        self.selx = 0
        self.sely = 0



    #def startGL (self) :
        #self.initializeGL()
        #self.resizeGL(651, 651)


        #glLightfv (GL_LIGHT0, GL_POSITION, light_position)

        #glEnable (GL_LIGHT0)
        #glEnable (GL_DEPTH_TEST)
        #glEnable(GL_LIGHTING)
        #glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        #glEnable(GL_LIGHT0)

    def resizeGL (self, width, height) :
        super(MyGLWindow,self).resizeGL(width,height)
        glViewport (0,0,width,height)
        glMatrixMode (GL_PROJECTION)
        #glOrtho (-2, 2,-2, 2, -20,20)
        gluPerspective (45,1.,1,20)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()
        glClearColor (0.1,0.1,.2,0)
        glEnable(GL_LIGHTING)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glEnable(GL_LIGHT0)


    def initializeGL(self):
        super(MyGLWindow,self).initializeGL()
        #glClearColor (0,0,.4,0)


    def mousePressEvent (self, ev) :
        print (ev.button())
        print ("start the selection")
        x = ev.x()
        y = ev.y()
        if ev.button() == 2 :
            #a= (GLuint*10)(0)
            #glReadBuffer (GL_FRONT)
            #glPixelStorei (GL_PACK_ALIGNMENT,1)
            #glReadPixels (0, 0,1,1,GL_RGBA, GL_UNSIGNED_INT,a)
            #print (a[0])
            self.selFlag = True
            self.selx = x 
            self.sely = y



    def mouseMoveEvent (self, ev):
        x = ev.pos().x()
        y = ev.pos().y()
        if (self.lastx > 0) :
            ydiff = y - self.lasty
            xdiff = x - self.lastx
            self.roty = self.roty + xdiff / 10.
            self.rotx = self.rotx + ydiff / 10.
        self.lastx = x
        self.lasty = y


    def wheelEvent (self, ev) :
        x = ev.angleDelta().y()

        self.curpos = float(x)/120  +  self.curpos
        print('angle :', float(x) / 120)


    def paintGL (self) :
        npts = self.myx.size
        
            

        glEnable (GL_LIGHTING)
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glEnable (GL_LIGHT0)
        q = gluNewQuadric()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        if (self.selFlag) :
            glScissor (self.selx-15,self.height()-self.sely-15,30,30)
            
            glEnable (GL_SCISSOR_TEST)
            glDisable (GL_DEPTH_TEST)
            queryIDs = (GLuint * npts)(0)
            pixelCounts = (GLint * npts)(0)
            glGenQueries (npts,queryIDs)
            #glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)

        #glColor3f(1, 1, 0)
        myellow = [1,1.,0.,1.]
        mygreen = [0,1,0.,1.]
        #glEnable (GL_SCISSOR_TEST)
        glPushMatrix ()
        if (self.setpts) :
            npts = self.myx.size
            glTranslatef(0.0, 0.0, self.curpos)

            glRotatef(self.rotx, 1., 0., 0)
            glRotatef(self.roty, 0., 1., 0)
            glScalef (self.scalfac, self.scalfac, self.scalfac)
            glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0.,0,1])
            for i in range(npts) :
                if (self.selFlag):
                    glBeginQuery (GL_SAMPLES_PASSED,queryIDs[i])
                if i==1 :
                    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mygreen)
                glTranslatef(self.myx[i], self.myy[i], self.myz[i])
                glLoadName (i)
                gluSphere(q,.03,36,36)
                glTranslatef(-self.myx[i], -self.myy[i], -self.myz[i])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, myellow)
                if (self.selFlag):
                   glEndQuery (GL_SAMPLES_PASSED)
                 #print queryIDs[i]
        else :
            glBegin(GL_TRIANGLES);
            glVertex3f(-0.5, -0.5, 0);
            glVertex3f(0.5, -0.5, 0);
            glVertex3f(0.0, 0.5, 0);
            glEnd()


        glPopMatrix()
        glLoadIdentity()
        #gluLookAt (0.,0.,-1,0.,0.,0.,0.,1.,0.)
        #gluPerspective(45, float(self.width()) / self.height(), 0.1, 50.0)
        #glTranslatef(0.0,0.0, self.curpos)
        
       
        if (self.selFlag) :
            glDisable (GL_SCISSOR_TEST)
            self.selFlag = False
            for k in range (npts) :
                val = glGetQueryObjectiv(queryIDs[k], GL_QUERY_RESULT)
                print queryIDs[k], val
            #glEnable (GL_DEPTH_TEST)
            #print queryIDs
            #glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
            #self.selFlag = True

        #self.rotx = self.rotx+5


    def setVals (self, xs, ys, zs) :
        self.myx = xs[:]
        self.myy = ys[:]
        self.myz = zs[:]
        self.setpts = True