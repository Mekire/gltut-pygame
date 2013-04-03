import sys,os,math
import pygame as pg
from OpenGL import GL

VERTICES = [ 0.25, 0.25, 0.0, 1.0,
             0.25,-0.25, 0.0, 1.0,
            -0.25,-0.25, 0.0, 1.0]

SIZE_FLOAT = VERT_COMPONENTS = 4

SHADER2STRING = {GL.GL_VERTEX_SHADER   : "vertex",
                 GL.GL_GEOMETRY_SHADER : "geometry",
                 GL.GL_FRAGMENT_SHADER : "fragment"}

class Shader:
    def __init__(self,vert_file,frag_file):
        self.shader = GL.glCreateProgram()
        self.vbo = None
        self.init_all(vert_file,frag_file)
        self.reshape(500,500)
        self.setup_uniforms()
    def init_all(self,vert_file,frag_file):
        self.attach_shaders(vert_file,frag_file)
        self.init_vertex_buf()
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
    def init_vertex_buf(self):
        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        ArrayType = (GL.GLfloat*len(VERTICES))
        GL.glBufferData(GL.GL_ARRAY_BUFFER,len(VERTICES)*SIZE_FLOAT,
                        ArrayType(*VERTICES),GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,0)

    def attach_shaders(self,vert_file,frag_file):
        vert,frag = self.load_shader_files(vert_file,frag_file)
        shade_list = []
        shade_list.append(self.compile(GL.GL_VERTEX_SHADER,vert))
        shade_list.append(self.compile(GL.GL_FRAGMENT_SHADER,frag))
        for shade in shade_list:
            GL.glAttachShader(self.shader,shade)
        self.link()
        for shade in shade_list:
            GL.glDetachShader(self.shader,shade)
            GL.glDeleteShader(shade)
    def load_shader_files(self,vert_file,frag_file):
        with open(vert_file,'r') as myfile:
            vert = myfile.read()
        with open(frag_file,'r') as myfile:
            frag = myfile.read()
        return vert,frag
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

    def setup_uniforms(self):
        self.elapsed_time_uniform = GL.glGetUniformLocation(self.shader,"time")
        self.period = GL.glGetUniformLocation(self.shader,"period")
        GL.glUseProgram(self.shader)
        GL.glUniform1f(self.period,5.0)
        GL.glUseProgram(0)

    def display(self):
        GL.glClearColor(1,1,1,1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glUseProgram(self.shader)

        GL.glUniform1f(self.elapsed_time_uniform,pg.time.get_ticks()/1000.0)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0,VERT_COMPONENTS,GL.GL_FLOAT,False,0,None)
        GL.glDrawArrays(GL.GL_TRIANGLES,0,3)
        GL.glDisableVertexAttribArray(0)
        GL.glUseProgram(0)

    def reshape(self,width,height):
        GL.glViewport(0,0,width,height)

class ShaderException(Exception):
    pass

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
    MyClock = pg.time.Clock()
    MyGL = Shader(os.path.join("data","calcOffset.vert"),os.path.join("data","standard.frag"))
    done = False
    while not done:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                done = True
            elif event.type == pg.KEYDOWN:
                pass
            elif event.type == pg.VIDEORESIZE:
                MyGL.reshape(*event.size)
        MyGL.display()
        pg.display.flip()
        MyClock.tick(65)

if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()
