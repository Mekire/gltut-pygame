"""I used Numpy arrays and functions in this tutorial.  It is still pretty
easy to get by without doing so if necessary however."""
import sys,os,math
import pygame as pg,numpy as np
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

        self.Objects = (NullRotation((0.0,0.0,-10.0)),
                        Rotate_X((-5.0,-5.0,-25.0)),
                        Rotate_Y((-5.0,5.0,-25.0)),
                        Rotate_Z((5.0,5.0,-25.0)),
                        RotateAxis((5.0,-5.0,-25.0)))

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
        mat = np.identity(4,'f')
        mat = self.calc_rotation(mat,time)
        mat[3] = self.offset+(1.0,)
        return mat

    def get_rad_angle(self,time,period):
        angular_speed = 2*math.pi/period
        time_through_loop = time%period
        return time_through_loop*angular_speed

class NullRotation(Generic):
    def calc_rotation(self,mat,time):
        return mat
class Rotate_X(Generic):
    def calc_rotation(self,mat,time):
        rad_ang = self.get_rad_angle(time,3.0)
        mat[1][1] =  math.cos(rad_ang)
        mat[1][2] =  math.sin(rad_ang)
        mat[2][1] = -mat[1][2]
        mat[2][2] =  mat[1][1]
        return mat
class Rotate_Y(Generic):
    def calc_rotation(self,mat,time):
        rad_ang = self.get_rad_angle(time,2.0)
        mat[0][0] =  math.cos(rad_ang)
        mat[0][2] = -math.sin(rad_ang)
        mat[2][0] = -mat[0][2]
        mat[2][2] =  mat[0][0]
        return mat
class Rotate_Z(Generic):
    def calc_rotation(self,mat,time):
        rad_ang = self.get_rad_angle(time,2.0)
        mat[0][0] =  math.cos(rad_ang)
        mat[0][1] =  math.sin(rad_ang)
        mat[1][0] = -mat[0][1]
        mat[1][1] =  mat[0][0]
        return mat
class RotateAxis(Generic):
    def calc_rotation(self,mat,time):
        rad_ang = self.get_rad_angle(time,2.0)
        cos = math.cos(rad_ang); icos = 1.0-cos
        sin = math.sin(rad_ang); isin = 1.0-sin
        rot_axis = np.array([1.0,1.0,1.0])
        rot_axis /= np.linalg.norm(rot_axis)

        mat[0][0] = (rot_axis[0]**2) + ((1-rot_axis[0]**2)*cos)
        mat[1][0] = (rot_axis[0]*rot_axis[1]*icos) - (rot_axis[2]*sin)
        mat[2][0] = (rot_axis[0]*rot_axis[2]*icos) + (rot_axis[1]*sin)

        mat[0][1] = (rot_axis[0]*rot_axis[1]*icos) + (rot_axis[2]*sin)
        mat[1][1] = (rot_axis[1]**2) + ((1-rot_axis[1]**2)*cos)
        mat[2][1] = (rot_axis[1]*rot_axis[2]*icos) - (rot_axis[0]*sin)

        mat[0][2] = (rot_axis[0]*rot_axis[2]*icos) - (rot_axis[1]*sin)
        mat[1][2] = (rot_axis[1]*rot_axis[2]*icos) + (rot_axis[0]*sin)
        mat[2][2] = (rot_axis[2]**2) + ((1-rot_axis[2]**2)*cos)
        return mat

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