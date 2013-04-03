import sys,os,math
import pygame as pg
from OpenGL import GL

sys.path.append("..")
sys.path.append("data")
import myframework
from vertex_data import VERTICES,INDICES,NUMBER_OF_VERTICES

class Shader(myframework.BaseShader):
    def __init__(self,vertices,vert_file,frag_file,indices=None):
        myframework.BaseShader.__init__(self,vertices,vert_file,frag_file,indices)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glFrontFace(GL.GL_CW)

    def init_vertex_buf(self):
        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        ArrayType = GL.GLfloat*len(self.vertices)
        GL.glBufferData(GL.GL_ARRAY_BUFFER,len(self.vertices)*self.size_float,
                        ArrayType(*self.vertices),GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,0)

        self.ibo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,self.ibo)
        ArrayType = (GL.GLushort*len(self.indices))
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,len(self.indices)*self.size_short,
                        ArrayType(*self.indices),GL.GL_STATIC_DRAW)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,0)

    def init_vao(self):
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
        color_data_offset = 3*self.size_float*NUMBER_OF_VERTICES

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0,3,GL.GL_FLOAT,GL.GL_FALSE,0,None)
        GL.glVertexAttribPointer(1,4,GL.GL_FLOAT,GL.GL_FALSE,0,GL.GLvoidp(color_data_offset))
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,self.ibo)
        GL.glBindVertexArray(0)

    def setup_uniforms(self):
        self.offset_location = GL.glGetUniformLocation(self.shader,"offset")
        self.perspective_matrix_unif = GL.glGetUniformLocation(self.shader,"perspectiveMatrix")
        self.frustum_scale = 1.0
        self.z_near,self.z_far = 1.0,3.0
        self.create_matrix()

        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.perspective_matrix_unif,1,GL.GL_FALSE,self.the_matrix)
        GL.glUseProgram(0)

    def create_matrix(self):
        self.the_matrix = [0.0 for i in range(16)]
        self.the_matrix[0] = self.frustum_scale
        self.the_matrix[5] = self.frustum_scale
        self.the_matrix[10] = (self.z_far+self.z_near)/(self.z_near-self.z_far)
        self.the_matrix[14] = (2*self.z_far*self.z_near)/(self.z_near-self.z_far)
        self.the_matrix[11] = -1.0

    def display(self):
        GL.glClearColor(0,0,0,0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        GL.glBindVertexArray(self.vao)
        GL.glUniform3f(self.offset_location,0.0,0.0,0.0)
        GL.glDrawElements(GL.GL_TRIANGLES,len(self.indices),GL.GL_UNSIGNED_SHORT,None)

        GL.glUniform3f(self.offset_location,0.0,0.0,-1.0)
        GL.glDrawElementsBaseVertex(GL.GL_TRIANGLES,len(self.indices),
                                    GL.GL_UNSIGNED_SHORT,None,NUMBER_OF_VERTICES/2)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)

    def reshape(self,width,height):
        self.the_matrix[0] = self.frustum_scale/(width/float(height))
        self.the_matrix[5] = self.frustum_scale
        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.perspective_matrix_unif,1,GL.GL_FALSE,self.the_matrix)
        GL.glUseProgram(0)
        GL.glViewport(0,0,width,height)

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
    MyClock = pg.time.Clock()
    MyGL = Shader(VERTICES[:],os.path.join("data","Standard.vert"),
                  os.path.join("data","Standard.frag"),INDICES[:])
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
        MyClock.tick(60)

if __name__ == '__main__':
    main()
    pg.quit()
    sys.exit()