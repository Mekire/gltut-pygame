"""This version of "01_hello_triangle" makes use of compileProgram and
compileShader from OpenGL.GL.shaders. This takes care of shader compilation,
attachment and linking for us and is quite convenient. For a greater
understanding of what is going on behind the scenes, see
"01_hello_triangle_manually"."""
from OpenGL import GL
from OpenGL.GL.shaders import compileProgram,compileShader
import pygame as pg,sys,os

VERTICES = [ 0.75,  0.75,  0.0,  1.0,
             0.75, -0.75,  0.0,  1.0,
            -0.75, -0.75,  0.0,  1.0]

SIZE_FLOAT = VERT_COMPONENTS = 4

#Shaders:
VERT = """
       #version 330
       layout(location = 0) in vec4 position;
       void main()
       {
          gl_Position = position;
       }"""

FRAG = """
       #version 330
       out vec4 outputColor;
       void main()
       {
          outputColor = vec4(0.0f, 1.0f, 0.0f, 1.0f);
       }"""

class GLtests:
    def __init__(self):
        self.shader = compileProgram(compileShader(VERT,GL.GL_VERTEX_SHADER),
                                     compileShader(FRAG,GL.GL_FRAGMENT_SHADER))
        self.vbo = None
        self.init_all()
        self.reshape(500,500)
    def init_all(self):
        self.init_vertex_buf()
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
    def init_vertex_buf(self):
        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        array_type = (GL.GLfloat*len(VERTICES))
        GL.glBufferData(GL.GL_ARRAY_BUFFER,len(VERTICES)*SIZE_FLOAT,
                        array_type(*VERTICES),GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,0)

    def display(self):
        GL.glClearColor(1, 1, 1, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0,VERT_COMPONENTS,GL.GL_FLOAT,False,0,None)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(VERTICES)//VERT_COMPONENTS)
        GL.glDisableVertexAttribArray(0)
        GL.glUseProgram(0)

    def reshape(self,width,height):
        GL.glViewport(0, 0, width, height)

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF)
    MyClock = pg.time.Clock()
    MyGL = GLtests()
    while 1:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                pg.quit();sys.exit()
            elif event.type == pg.KEYDOWN:
                pass
        MyGL.display()
        pg.display.flip()
        MyClock.tick(65)

if __name__ == '__main__':
    main()