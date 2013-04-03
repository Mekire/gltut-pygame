import sys,os,math
import pygame as pg
from OpenGL import GL

sys.path.append("..")
sys.path.append("data")
import myframework
from vertices_perspective import VERTICES

class Shader(myframework.BaseShader):
    def __init__(self,vertices,vert_file,frag_file):
        myframework.BaseShader.__init__(self,vertices,vert_file,frag_file)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_BACK)
        GL.glFrontFace(GL.GL_CW)

    def setup_uniforms(self):
        self.offset_location = GL.glGetUniformLocation(self.shader,"offset")
        self.frustum_scale_unif = GL.glGetUniformLocation(self.shader,"frustumScale")
        self.z_near_unif = GL.glGetUniformLocation(self.shader,"zNear")
        self.z_far_unif = GL.glGetUniformLocation(self.shader,"zFar")

        GL.glUseProgram(self.shader)
        GL.glUniform1f(self.frustum_scale_unif,1.0)
        GL.glUniform1f(self.z_near_unif,1.0)
        GL.glUniform1f(self.z_far_unif,3.0)
        GL.glUseProgram(0)

    def display(self):
        GL.glClearColor(0,0,0,0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        GL.glUseProgram(self.shader)
        GL.glUniform2f(self.offset_location,0.5,0.5)
        color_data = GL.GLvoidp((len(self.vertices)*self.size_float)/2)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.vbo)
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0,self.vert_comp,GL.GL_FLOAT,GL.GL_FALSE,0,None)
        GL.glVertexAttribPointer(1,self.vert_comp,GL.GL_FLOAT,GL.GL_FALSE,0,color_data)

        GL.glDrawArrays(GL.GL_TRIANGLES,0,36)

        GL.glDisableVertexAttribArray(0)
        GL.glDisableVertexAttribArray(1)
        GL.glUseProgram(0)

def main():
    pg.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    SCREEN = pg.display.set_mode((500,500),pg.HWSURFACE|pg.OPENGL|pg.DOUBLEBUF|pg.RESIZABLE)
    MyClock = pg.time.Clock()
    MyGL = Shader(VERTICES[:],os.path.join("data","ManualPerspective.vert"),os.path.join("data","StandardColors.frag"))
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
