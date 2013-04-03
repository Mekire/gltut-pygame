"""I fought a while trying to get this one to work.  Firstly I thought that *
did matrix multiplication when using numpy arrays; it doesn't (you need to use
numpy.dot instead). Then I had a series of issues which ended up being a result
of the tutorial using the column-major convention, and numpy arrays using the
row-major convention. The solution to this was to do matrix multiplications
in the oposite order indictated in the original. Anyway, the final product is
quite amusing and I'm glad I got it to work.

This program is interactive. The controls are:
    Base Spin         : A/D
    Arm Raise/Lower   : W/S
    Elbow Raise/Lower : R/F
    Wrist Raise/Lower : T/G
    Wrist Spin        : Z/C
    Finger Open/Close : Q/E
    Space-Bar         : Print the current state of the armature."""

import sys,os,math
import pygame as pg,numpy as np
from OpenGL import GL

sys.path.append("..")
sys.path.append("data")
import myframework
from hierarchy_data import VERTICES,INDICES,NUMBER_OF_VERTICES

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

        self.Armature = Hierarchy()

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
        GL.glEnableVertexAttribArray(self.pos_attrib)
        GL.glEnableVertexAttribArray(self.col_attrib)
        GL.glVertexAttribPointer(self.pos_attrib,3,GL.GL_FLOAT,GL.GL_FALSE,0,None)
        GL.glVertexAttribPointer(self.col_attrib,4,GL.GL_FLOAT,GL.GL_FALSE,0,GL.GLvoidp(color_data_offset))
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,self.ibo)
        GL.glBindVertexArray(0)

    def setup_attributes(self):
        self.pos_attrib = GL.glGetAttribLocation(self.shader,"position")
        self.col_attrib = GL.glGetAttribLocation(self.shader,"color")
    def setup_uniforms(self):
        self.model2cam_matrix_unif = GL.glGetUniformLocation(self.shader,"modelToCameraMatrix")
        self.cam2clip_matrix_unif = GL.glGetUniformLocation(self.shader,"cameraToClipMatrix")
        self.frustum_scale = self.calc_frust_scale(45.0)
        self.z_near,self.z_far = 1.0,100.0
        self.create_matrix()

        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.cam2clip_matrix_unif,1,GL.GL_FALSE,self.persp_matrix)
        GL.glUseProgram(0)

    def calc_frust_scale(self,angle):
        rads = math.radians(angle)
        return 1.0/math.tan(rads/2.0)

    def create_matrix(self):
        self.persp_matrix = [0.0 for i in range(16)]
        self.persp_matrix[0] = self.frustum_scale
        self.persp_matrix[5] = self.frustum_scale
        self.persp_matrix[10] = (self.z_far+self.z_near)/(self.z_near-self.z_far)
        self.persp_matrix[14] = (2*self.z_far*self.z_near)/(self.z_near-self.z_far)
        self.persp_matrix[11] = -1.0

    def display(self):
        GL.glClearColor(0,0,0,0)
        GL.glClearDepth(1.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.Armature.draw(self)

    def reshape(self,width,height):
        self.persp_matrix[0] = self.frustum_scale/(width/float(height))
        self.persp_matrix[5] = self.frustum_scale
        GL.glUseProgram(self.shader)
        GL.glUniformMatrix4fv(self.cam2clip_matrix_unif,1,GL.GL_FALSE,self.persp_matrix)
        GL.glUseProgram(0)
        GL.glViewport(0,0,width,height)

class MatrixStack:
    def __init__(self):
        self.current_matrix = np.identity(4,'f')
        self.matrices = []
    def rotate_X(self,ang):
        rad_ang = math.radians(ang)
        mat = np.identity(4,'f')
        mat[1][1] =  math.cos(rad_ang)
        mat[1][2] =  math.sin(rad_ang)
        mat[2][1] = -mat[1][2]
        mat[2][2] =  mat[1][1]
        self.current_matrix = np.dot(mat,self.current_matrix)
    def rotate_Y(self,ang):
        rad_ang = math.radians(ang)
        mat = np.identity(4,'f')
        mat[0][0] =  math.cos(rad_ang)
        mat[0][2] = -math.sin(rad_ang)
        mat[2][0] = -mat[0][2]
        mat[2][2] =  mat[0][0]
        self.current_matrix = np.dot(mat,self.current_matrix)
    def rotate_Z(self,ang):
        rad_ang = math.radians(ang)
        mat = np.identity(4,'f')
        mat[0][0] =  math.cos(rad_ang)
        mat[0][1] =  math.sin(rad_ang)
        mat[1][0] = -mat[0][1]
        mat[1][1] =  mat[0][0]
        self.current_matrix = np.dot(mat,self.current_matrix)
    def scale(self,scale_vec):
        scale_mat = np.identity(4,'f')
        for i in range(3):
            scale_mat[i][i] = scale_vec[i]
        self.current_matrix = np.dot(scale_mat,self.current_matrix)
    def translate(self,offset):
        translate_mat = np.identity(4,'f')
        translate_mat[3] = offset+(1.0,)
        self.current_matrix = np.dot(translate_mat,self.current_matrix)

    def push(self):
        self.matrices.append(self.current_matrix[:])
    def pop(self):
        self.current_matrix = self.matrices.pop()

class Hierarchy:
    def __init__(self):
        self.make_part_dict()
        self.Stack = None
        self.STAND_ANG_INC = 2.0
    def make_part_dict(self):
        self.base = {"pos"    : (3.0,-5.0,-40.0),
                     "ang"    : -45.0,
                     "pos_L"  : (2.0,0.0,0.0),
                     "pos_R"  : (-2.0,0.0,0.0),
                     "scale_Z": 3.0}
        self.arm = {"up_ang"   : -33.75,
                    "up_size"  : 9.0,
                    "low_pos"  : (0.0,0.0,8.0),
                    "low_ang"  : 146.25,
                    "low_len"  : 5.0,
                    "low_width": 1.5}
        self.wrist = {"pos"      : (0.0,0.0,5.0),
                      "roll_ang" : 0.0,
                      "pitch_ang": 67.5,
                      "len"      : 2.0,
                      "width"    : 2.0}
        self.finger = {"pos_L"   : (1.0, 0.0, 1.0),
                       "pos_R"   : (-1.0,0.0,1.0),
                       "open_ang": 180.0,
                       "len"     : 2.0,
                       "width"   : 0.5,
                       "low_ang" : 45.0}

    def draw(self,Shader):
        self.Stack = MatrixStack()
        GL.glUseProgram(Shader.shader)
        GL.glBindVertexArray(Shader.vao)

        self.Stack.translate(self.base["pos"])
        self.Stack.rotate_Y(self.base["ang"])
        self.draw_base(Shader)
        self.draw_arm(Shader)

        GL.glBindVertexArray(0)
        GL.glUseProgram(0)

    def draw_and_pop(self,Shader):
        GL.glUniformMatrix4fv(Shader.model2cam_matrix_unif,1,GL.GL_FALSE,self.Stack.current_matrix)
        GL.glDrawElements(GL.GL_TRIANGLES,len(Shader.indices),GL.GL_UNSIGNED_SHORT,None)
        self.Stack.pop()

    def draw_base(self,Shader):
        for part in ("pos_L","pos_R"):
            self.Stack.push()
            self.Stack.translate(self.base[part])
            self.Stack.scale((1.0,1.0,self.base["scale_Z"]))
            self.draw_and_pop(Shader)
    def draw_arm(self,Shader):
        self.draw_up_arm(Shader)

    def draw_fingers(self,Shader):
        for pos,angle in (("pos_L",1),("pos_R",-1)):
            self.Stack.push()
            self.Stack.translate(self.finger[pos])
            self.Stack.rotate_Y(self.finger["open_ang"]*angle)

            self.Stack.push()
            self.Stack.translate((0.0,0.0,self.finger["len"]/2.0))
            self.Stack.scale((self.finger["width"]/2.0,self.finger["width"]/2.0,self.finger["len"]/2.0))
            self.draw_and_pop(Shader)
            self.draw_low_finger(Shader,angle)

            self.Stack.pop();self.Stack.pop()

    def draw_low_finger(self,Shader,angle):
        self.Stack.push()
        self.Stack.translate((0.0,0.0,self.finger["len"]))
        self.Stack.rotate_Y(-self.finger["low_ang"]*angle)

        self.Stack.push()
        self.Stack.translate((0.0,0.0,self.finger["len"]/2.0))
        self.Stack.scale((self.finger["width"]/2.0,self.finger["width"]/2.0,self.finger["len"]/2.0))
        self.draw_and_pop(Shader)

    def draw_wrist(self,Shader):
        self.Stack.push()
        self.Stack.translate(self.wrist["pos"])
        self.Stack.rotate_Z(self.wrist["roll_ang"])
        self.Stack.rotate_X(self.wrist["pitch_ang"])

        self.Stack.push()
        self.Stack.scale((self.wrist["width"]/2.0,self.wrist["width"]/2.0,self.wrist["len"]/2.0))
        self.draw_and_pop(Shader)

        self.draw_fingers(Shader)
        self.Stack.pop()

    def draw_low_arm(self,Shader):
        self.Stack.push()
        self.Stack.translate(self.arm["low_pos"])
        self.Stack.rotate_X(self.arm["low_ang"])

        self.Stack.push()
        self.Stack.translate((0.0,0.0,self.arm["low_len"]/2.0))
        self.Stack.scale((self.arm["low_width"]/2.0,self.arm["low_width"]/2.0,self.arm["low_len"]/2.0))
        self.draw_and_pop(Shader)

        self.draw_wrist(Shader)
        self.Stack.pop()

    def draw_up_arm(self,Shader):
        self.Stack.push()
        self.Stack.rotate_X(self.arm["up_ang"])

        self.Stack.push()
        self.Stack.translate((0.0,0.0,(self.arm["up_size"]/2.0)-1.0))
        self.Stack.scale((1.0,1.0,self.arm["up_size"]/2.0))
        self.draw_and_pop(Shader)

        self.draw_low_arm(Shader)
        self.Stack.pop()

    def clamp(self,value,low,high):
        return max(low,min(high,value))

    def adj_ang(self,pos,attrib,feat,clamp=None):
        value = getattr(self,attrib)[feat]
        value += (self.STAND_ANG_INC if pos else -self.STAND_ANG_INC)
        if clamp:
            getattr(self,attrib)[feat] = self.clamp(value,*clamp)
        else:
            getattr(self,attrib)[feat] = value%360.0

    def print_state(self):
        print("{:<17} : {}".format("Base Angle",self.base["ang"]))
        print("{:<17} : {}".format("Upper-Arm Angle",self.arm["up_ang"]))
        print("{:<17} : {}".format("Lower-Arm Angle",self.arm["low_ang"]))
        print("{:<17} : {}".format("Wrist Pitch Angle",self.wrist["pitch_ang"]))
        print("{:<17} : {}".format("Wrist Roll Angle",self.wrist["roll_ang"]))
        print("{:<17} : {}\n".format("Finger Open Angle",self.finger["open_ang"]))

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
    MyClock = pg.time.Clock()
    MyGL = Shader(VERTICES[:],os.path.join("data","PosColorLocalTransform.vert"),
                  os.path.join("data","ColorPassthrough.frag"),INDICES[:])

    KEY_DICT = {(pg.K_d,pg.K_a) : ("base","ang"),
                (pg.K_w,pg.K_s) : ("arm","up_ang",(-90.0,0)),
                (pg.K_r,pg.K_f) : ("arm","low_ang",(0.0,146.25)),
                (pg.K_t,pg.K_g) : ("wrist","pitch_ang",(0.0,90.0)),
                (pg.K_c,pg.K_z) : ("wrist","roll_ang"),
                (pg.K_e,pg.K_q) : ("finger","open_ang",(9.0,180.0))}

    done = False
    while not done:
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type==pg.QUIT or (event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE):
                done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    MyGL.Armature.print_state()
            elif event.type == pg.VIDEORESIZE:
                MyGL.reshape(*event.size)
        for pair in KEY_DICT:
            for i,key in enumerate(pair):
                if keys[key]:
                    MyGL.Armature.adj_ang(i,*KEY_DICT[pair])
        MyGL.display()
        pg.display.flip()
        MyClock.tick(60)

if __name__ == '__main__':
    main()
    pg.quit();sys.exit()