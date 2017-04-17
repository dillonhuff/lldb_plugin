"""Test simple functions (i.e. no pointers involved)"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
start = time.time()

window = None

def display():
    glutSetWindow(window);

    glClearColor (0.0, 0.0, 0.0, 0.0)
    glClear (GL_COLOR_BUFFER_BIT)

    glutSolidTeapot( .7 )
    glFlush ()
    glutSwapBuffers()

size = (250,250)

def reshape( *args ):
    global size 
    size = args
    glViewport( *( (0,0)+args) )
    display()

if __name__ == "__main__":

    newArgv = glutInit("")

    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)

    window = glutCreateWindow("hello")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()

#cmd()
