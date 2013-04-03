"""Just using regular lists and tuples for the things taken care of using
GLM in the original tutorial. Nothing here is complex enough to require resorting
to numpy or another library yet."""
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

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glDepthRange(0.0,1.0)

        self.Objects = (NullScale((0.0,0.0,-45.0)),
                        StaticUniformScale((-10.0,-10.0,-45.0)),
                        StaticNonUniformScale((-10.0,10.0,-45.0)),
                        DynamicUniformScale((10.0,10.0,-45.0)),
                        DynamicNonUniformScale((10.0,-10.0,-45.0)))

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
        self.model2cam_matrix_unif = GL.glGetUniformLocation(self.shader,"modelToCameraMatrix")
        self.cam2clip_matrix_unif = GL.glGetUniformLocation(self.shader,"cameraToClipMatrix")
        self.frustum_scale = self.calc_frust_scale(45.0)
        self.z_near,self.z_far = 1.0,61.0
        self.create_matrix()

        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.cam2clip_matrix_unif,1,GL.GL_FALSE,self.the_matrix)
        GL.glUseProgram(0)

    def calc_frust_scale(self,angle):
        rads = math.radians(angle)
        return 1.0/math.tan(rads/2.0)

    def create_matrix(self):
        self.the_matrix = [0.0 for i in range(16)]
        self.the_matrix[0] = self.frustum_scale
        self.the_matrix[5] = self.frustum_scale
        self.the_matrix[10] = (self.z_far+self.z_near)/(self.z_near-self.z_far)
        self.the_matrix[14] = (2*self.z_far*self.z_near)/(self.z_near-self.z_far)
        self.the_matrix[11] = -1.0

    def display(self):
        GL.glClearColor(0,0,0,0)
        GL.glClearDepth(1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        GL.glBindVertexArray(self.vao)

        elapsed_time = pg.time.get_ticks()/1000.0
        for Obj in self.Objects:
            matrix = Obj.construct_matrix(elapsed_time)
            GL.glUniformMatrix4fv(self.model2cam_matrix_unif,1,GL.GL_FALSE,matrix)
            GL.glDrawElements(GL.GL_TRIANGLES,len(self.indices),GL.GL_UNSIGNED_SHORT,None)

        GL.glBindVertexArray(0)
        GL.glUseProgram(0)

    def reshape(self,width,height):
        self.the_matrix[0] = self.frustum_scale/(width/float(height))
        self.the_matrix[5] = self.frustum_scale
        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.cam2clip_matrix_unif,1,GL.GL_FALSE,self.the_matrix)
        GL.glUseProgram(0)
        GL.glViewport(0,0,width,height)

class Generic:
    def __init__(self,offset):
        self.offset = offset
    def construct_matrix(self,time):
        mat = [[0.0 for i in range(4)] for j in range(4)]
        scale = self.calc_scale(time)
        for i in range(3):
            mat[i][i] = scale[i]
        mat[3] = self.offset+(1.0,)
        return mat
    def calc_lerp(self,time,period):
        value = time%period/period
        if value > 0.5:
            value = 1.0-value
        return value*2.0

class NullScale(Generic):
    def calc_scale(self,time):
        return (1.0,1.0,1.0)
class StaticUniformScale(Generic):
    def calc_scale(self,time):
        return (4.0,4.0,4.0)
class StaticNonUniformScale(Generic):
    def calc_scale(self,time):
        return (0.5,1.0,10.0)
class DynamicUniformScale(Generic):
    def calc_scale(self,time):
        period = 3.0
        lerp = self.calc_lerp(time,period)
        return (1+3*lerp,)*3
class DynamicNonUniformScale(Generic):
    def calc_scale(self,time):
        period_x = 3.0
        period_z = 5.0
        lerp_x = self.calc_lerp(time,period_x)
        lerp_z = self.calc_lerp(time,period_z)
        return ((1-0.5*lerp_x),1.0,(1+9*lerp_z))

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
    MyClock = pg.time.Clock()
    MyGL = Shader(VERTICES[:],os.path.join("data","PosColorLocalTransform.vert"),
                  os.path.join("data","ColorPassthrough.frag"),INDICES[:])
    done = False
    while not done:
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pass
            elif event.type == pg.VIDEORESIZE:
                MyGL.reshape(*event.size)
        MyGL.display()
        pg.display.flip()
        MyClock.tick(60)

if __name__ == '__main__':
    main()
    pg.quit();sys.exit()