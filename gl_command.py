"""Test simple functions (i.e. no pointers involved)"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

import lldb
import commands
import optparse
import shlex

start = time.time()

window = None

def drawText( value, x,y,  windowHeight, windowWidth, step = 18 ):
    """Draw the given text at given 2D position in window
    """
    glMatrixMode(GL_PROJECTION);
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPushMatrix()
    matrix = glGetDouble( GL_PROJECTION_MATRIX )
    
    glLoadIdentity();
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    glRasterPos2i(x, y);
    lines = 0
    for character in value:
        if character == '\n':
            glRasterPos2i(x, y-(lines*18))
        else:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character));
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPopMatrix();
    glLoadMatrixd( matrix ) # should have un-decorated alias for this...
    
    glMatrixMode(GL_MODELVIEW);

def display():
    glutSetWindow(window);
    #glClearColor (0.0, 0.0, (time.time()%1.0)/1.0, 0.0)
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glClear (GL_COLOR_BUFFER_BIT)
    #drawText( 'hello', 20,20, size[0],size[1] )
    #glutBitmapCharacter( GLUT_BITMAP_8_BY_13, ord('a'))
    glutSolidTeapot( .7 )
    glFlush ()
    glutSwapBuffers()

size = (250,250)

def reshape( *args ):
    global size 
    size = args
    glViewport( *( (0,0)+args) )
    display()

def ontimer( *args ):
    print 'timer', args, '@time', time.time()-start
    glutTimerFunc( 1000, ontimer, 24 )

def idle():
    delta = time.time()-start
    if delta < 10:
        global size 
        x,y = size 
        if delta < 5:
            change = +1
        else:
            change = -1
        x = x-change
        y = y+change
        if x < 1:
            x = 1
        if y < 1:
            y = 1
        glutReshapeWindow( x, y )
        size = (x,y)
        glutSetWindow(window)
        glutPostRedisplay()
    else:
        glutDestroyWindow( window )
        print 'window destroyed'
        import sys
        sys.exit( 0 )

def printFunction( name ):
    def onevent( *args ):
        print '%s -> %s'%(name, ", ".join( [str(a) for a in args ]))
    return onevent

def my_cmd(debugger, command, result, internal_dict):
    import sys

    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB )
    glutInitWindowSize(250, 250)
    glutInitWindowPosition(100, 100)

    window = glutCreateWindow("hello")

    print 'window', repr(window)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    # glutMouseFunc(printFunction( 'Mouse' ))
    # glutEntryFunc(printFunction( 'Entry' ))
    # glutKeyboardFunc( printFunction( 'Keyboard' ))
    # glutKeyboardUpFunc( printFunction( 'KeyboardUp' ))
    # glutMotionFunc( printFunction( 'Motion' ))
    # glutPassiveMotionFunc( printFunction( 'PassiveMotion' ))
    # glutVisibilityFunc( printFunction( 'Visibility' ))
    # glutWindowStatusFunc( printFunction( 'WindowStatus' ))
    # glutSpecialFunc( printFunction( 'Special' ))
    # glutSpecialUpFunc( printFunction( 'SpecialUp' ))
    # glutTimerFunc( 1000, ontimer, 23 )
    
    glutIdleFunc( idle )
    glutMainLoop()


    # target = debugger.GetSelectedTarget()
    # process = target.GetProcess()
    # thread = process.GetSelectedThread()

    # for frame in thread:

    #     print str(frame)

    #     function = frame.GetFunction()
    #     print 'FUNCTION = ', function

    #     if frame.IsInlined():
    #         print 'INLINED'
    #     else:
    #         args = frame.get_arguments()

    #         print '# of arguments = ', len(args)

    #         for arg in args:
    #             print arg

    #         vars = frame.get_all_variables()

    #         print '# of vars =', len(args)

    #         for var in vars:
    #             print var

def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f gl_command.my_cmd my_cmd')
    print 'The "my_cmd" python command has been installed and is ready for use.'
