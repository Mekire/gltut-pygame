from OpenGL import GL

SHADER2STRING = {GL.GL_VERTEX_SHADER   : "vertex",
                 GL.GL_GEOMETRY_SHADER : "geometry",
                 GL.GL_FRAGMENT_SHADER : "fragment"}

class ShaderError(Exception):
    pass

class BaseShader:
    def __init__(self,vertices,vert_file,frag_file,indices=None):
        self.vertices = vertices
        self.indices = indices
        self.shader = GL.glCreateProgram()
        self.size_float = self.vert_comp = 4
        self.size_short = 2
        self.vbo = None
        self.init_all(vert_file,frag_file)
        self.reshape(500,500)
    def init_all(self,vert_file,frag_file):
        self.attach_shaders(vert_file,frag_file)
        self.setup_attributes()
        self.setup_uniforms()
        self.init_vertex_buf()
        self.init_vao()
    def init_vao(self):
        self.vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.vao)
    def init_vertex_buf(self):
        self.vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER,self.vbo)
        ArrayType = (GL.GLfloat*len(self.vertices))
        GL.glBufferData(GL.GL_ARRAY_BUFFER,len(self.vertices)*self.size_float,
                        ArrayType(*self.vertices),GL.GL_STATIC_DRAW)
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
            raise ShaderError,"Compile failure in {} shader:\n{}\n".format(shader_name,log)
        return shader
    def link(self):
        GL.glLinkProgram(self.shader)
        status = GL.glGetProgramiv(self.shader,GL.GL_LINK_STATUS)
        if not status:
            log = GL.glGetProgramInfoLog(self.shader)
            raise ShaderError,"Linking failue:\n{}\n".format(log)
    def reshape(self,width,height):
        GL.glViewport(0,0,width,height)
    def setup_uniforms(self):
        pass
    def setup_attributes(self):
        pass