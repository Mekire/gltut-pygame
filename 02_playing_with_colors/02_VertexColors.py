import sys,os
import pygame as pg
from OpenGL import GL

VERTICES = [ 0.0, 0.5, 0.0, 1.0,
             0.5,-0.366, 0.0, 1.0,
            -0.5,-0.366, 0.0, 1.0,
             1.0, 0.0, 0.0, 1.0,
             0.0, 1.0, 0.0, 1.0,
             0.0, 0.0, 1.0, 1.0]

SIZE_FLOAT = VERT_COMPONENTS = 4

SHADER2STRING = {GL.GL_VERTEX_SHADER   : "vertex",
                 GL.GL_GEOMETRY_SHADER : "geometry",
                 GL.GL_FRAGMENT_SHADER : "fragment"}

#Load shaders from files.
with open(os.path.join("data","VertexColors.vert"),'r') as myfile:
    VERT = myfile.read()
with open(os.path.join("data","VertexColors.frag"),'r') as myfile:
    FRAG = myfile.read()

class GLtests:
    def __init__(self):
        self.shader = GL.glCreateProgram()
        self.vbo = None
        self.init_all()
        self.reshape(500,500)
    def init_all(self):
        self.attach_shaders()
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

    def attach_shaders(self):
        shade_list = []
        shade_list.append(self.compile(GL.GL_VERTEX_SHADER,VERT))
        shade_list.append(self.compile(GL.GL_FRAGMENT_SHADER,FRAG))
        for shade in shade_list:
            GL.glAttachShader(self.shader,shade)
        self.link()
        for shade in shade_list:
            GL.glDetachShader(self.shader,shade)
            GL.glDeleteShader(shade)
    def compile(self,shader_type,shader_str):
        shader = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader,shader_str)
        GL.glCompileShader(shader)
        status = GL.glGetShaderiv(shader,GL.GL_COMPILE_STATUS)
        if not status:
            log = GL.glGetShaderInfoLog(shader)
            shader_name = SHADER2STRING[shader_type]
            raise ShaderException,"Compile failure in {} shader:\n{}\n".format(shader_name,log)
        return shader

    def link(self):
        GL.glLinkProgram(self.shader)
        status = GL.glGetProgramiv(self.shader,GL.GL_LINK_STATUS)
        if not status:
            log = GL.glGetProgramInfoLog(self.shader)
            raise ShaderException,"Linking failue:\n{}\n".format(log)

    def display(self):
        GL.glClearColor(0,0,0,0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0,VERT_COMPONENTS,GL.GL_FLOAT,False,0,None)
        GL.glVertexAttribPointer(1,VERT_COMPONENTS,GL.GL_FLOAT,False,0,GL.GLvoidp(48))
        GL.glDrawArrays(GL.GL_TRIANGLES,0,3)

        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)
        GL.glUseProgram(0)

    def reshape(self,width,height):
        GL.glViewport(0,0,width,height)

class ShaderException(Exception):
    pass

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF)
    MyClock = pg.time.Clock()
    MyGL = GLtests()
    done = False
    while not done:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                done = True
            elif event.type == pg.KEYDOWN:
                pass
        MyGL.display()
        pg.display.flip()
        MyClock.tick(65)

if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()
