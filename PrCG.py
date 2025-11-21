# Projecto de Computação Gráfica

import sys, math, os
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image


def draw_cylinder(radius, height, color):
    glColor3f(*color)
    glutSolidCylinder(radius, height, 24, 8)

def geo_roda_traseira():
    draw_cylinder(1.2, 0.6, (0.05, 0.05, 0.05))

def geo_roda_dianteira():
    draw_cylinder(0.9, 0.5, (0.05, 0.05, 0.05))

def draw_corpo(color):
    glColor3f(*color)
    glutSolidCube(2.0)

def geo_corpo():
    draw_corpo((0.8, 0.1, 0.1))

def geo_parede():
    glColor3f(0.8, 0.8, 0.9)
    glutSolidCube(1.0)

def geo_portao():
    glColor3f(0.6, 0.4, 0.2)
    glScalef(0.5, 10.0, 20.0)
    glutSolidCube(1.0)

def geo_parachoque():
    glColor3f(0.3, 0.3, 0.3)
    glutSolidCube(1.0)

def geo_parede_traseira():
    glColor3f(0.8, 0.1, 0.1)
    glutSolidCube(1.0)

def geo_parede_lateral():
    glColor3f(0.8, 0.1, 0.1)
    glutSolidCube(1.0)

def geo_porta():
    glColor3f(0.7, 0.05, 0.05)
    glutSolidCube(1.0)

def geo_capo():
    glColor3f(0.8, 0.1, 0.1)
    glutSolidCube(1.0)

def geo_volante():
    # Aro do volante (torus)
    glColor3f(0.1, 0.1, 0.1)  # Preto
    glutSolidTorus(0.15, 0.8, 16, 24)

    # Coluna central (cilindro pequeno)
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)  # Cinza escuro
    glutSolidCylinder(0.25, 0.3, 12, 8)
    glPopMatrix()

def load_texture(path, repeat=True): #TP06 do 2-cube-textured.py
    if not os.path.isfile(path):
        print("Texture not found:", path); sys.exit(1)

    img = Image.open(path).convert("RGBA")
    w, h = img.size
    data = img.tobytes("raw", "RGBA", 0, -1)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    # filtros  e  mipmaps (veremos esta parte mais tarde )
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT if repeat else GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT if repeat else GL_CLAMP_TO_EDGE)

    # Criação de mipmaps com o GLU
    gluBuild2DMipmaps(GL_TEXTURE_2D, GL_RGBA, w, h, GL_RGBA, GL_UNSIGNED_BYTE, data)

    #devolve o ID de cada textura carregada que será usado quando os objectos forem desenhados
    return tex_id

def draw_chao(): #adaptado da TP06 do 2-cube-textured.py
    S = 100.0
    T = 50.0  # Quantas vezes multiplicar a textura no chão
    
    # Ativar texturas apenas para o chão
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_floor)
    glColor3f(1, 1, 1)
    glNormal3f(0, 1, 0)

    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-S, 0.0,  S)
    glTexCoord2f(T,   0.0); glVertex3f( S, 0.0,  S)
    glTexCoord2f(T,    T ); glVertex3f( S, 0.0, -S)
    glTexCoord2f(0.0,  T ); glVertex3f(-S, 0.0, -S)
    glEnd()
    
    # Desativar texturas para não afetar outros objetos
    glDisable(GL_TEXTURE_2D)

# -------------------------------
# Classe Node
# -------------------------------
class Node:
    def __init__(self, name, geom=None, transform=None, updater=None, state=None):
        self.name = name
        self.geom = geom
        self.transform = transform
        self.updater = updater
        self.state = state or {}
        self.children = []

    def add(self, *kids):
        for k in kids:
            self.children.append(k)
        return self

    def update(self, dt):
        if self.updater:
            self.updater(self, dt)
        for c in self.children:
            c.update(dt)

    def draw(self):
        glPushMatrix()
        if self.transform:
            self.transform(self)
        if self.geom:
            self.geom()
        for c in self.children:
            c.draw()
        glPopMatrix()


# -------------------------------
# Transformações e Atualizações
# -------------------------------

def tf_obj(x, y, z, sx, sy, sz, ang_deg, ax, ay, az):
    def _tf(node):
        glTranslatef(x, y, z)
        glRotate(ang_deg, ax, ay, az)
        glScalef(sx, sy, sz)
    return _tf


# posição do carro (agora em X)
def tf_pos_carro(node):
    glTranslatef(node.state["x"], 0.0, node.state["z"])

# mudar o angulo do portão da garagem
def tf_portao_garagem(node):
    ang = node.state.get("ang_portao", 0.0)
    glTranslatef(-10.0, 9.0, 0.0)
    glRotatef(-ang, 0.0, 0.0, 1.0)
    glTranslatef(0.0, -5.0, 0.0)

def tf_porta_esquerda(node):
    ang = node.state.get("ang_porta", 0.0)
    glTranslatef(-2.0, 3.5, 6.0)
    glRotatef(ang, 0.0, -1.0, 0.0)
    glTranslatef(2.0, 0.0, 0.0)

def tf_porta_direita(node):
    ang = node.state.get("ang_porta", 0.0)
    glTranslatef(-2.0, 3.5, -6.0)
    glRotatef(-ang, 0.0, -1.0, 0.0)
    glTranslatef(2.0, 0.0, 0.0)

# update no eixo X
def update_carro(node, dt):
    # integrate velocity
    vel = node.state.get("vel", 0.0)
    nova_posicao = node.state["x"] + vel * dt

    ang_portao = PORTAO_GARAGEM.state.get("ang_portao", 0.0)
    posicao_atual = node.state["x"]
    frente_carro_atual = posicao_atual - 6.0
    traseira_carro_atual = posicao_atual + 6.0
    frente_carro_nova = nova_posicao - 6.0
    traseira_carro_nova = nova_posicao + 6.0

    # Bloqueia entrada (ao tentar atravessar o portão fechado de fora para dentro)
    if ang_portao == 0.0 and vel < 0.0:
        if frente_carro_atual > -8.0 and frente_carro_nova <= -8.0:
            node.state["vel"] = 0.0
            return

    # Bloqueia saída (ao tentar atravessar o portão fechado de dentro para fora)
    if ang_portao == 0.0 and vel > 0.0:
        if traseira_carro_atual < -10.0 and traseira_carro_nova >= -10.0:
            node.state["vel"] = 0.0
            return

    # Atualizar posição
    node.state["x"] = nova_posicao

    # clamp left boundary so the car can't pass x = -30.0
    if node.state["x"] <= -20.0:
        node.state["x"] = -20.0
        node.state["vel"] = 0.0


# -------------------------------
# Cena
# -------------------------------
def build_scene():
    world = Node("World")

    #Carro
    carro = Node("Carro", transform=tf_pos_carro, updater=update_carro,
                 state={"x": 0.0, "z": 0.0, "vel": 0.0})
    # store global reference so keyboard() always controls the correct node
    global CARRO
    CARRO = carro

    # As rodas com x = 5.0 são consideradas traseiras, que são maiores às dianteiras
    roda1 = Node("R1_Dianteira", geom=geo_roda_dianteira,
                transform=tf_obj(-5.0, 0.9, -6.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))

    roda2 = Node("R2_Dianteira", geom=geo_roda_dianteira,
                transform=tf_obj(-5.0, 0.9, 6, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))

    roda3 = Node("R3_Traseira", geom=geo_roda_traseira,
                transform=tf_obj( 5.0, 1.2, 6, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda4 = Node("R4_Traseira", geom=geo_roda_traseira,
                transform=tf_obj( 5.0, 1.2, -6.6, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))

    # Corpo
    corpo = Node("Corpo", geom=geo_corpo,
                transform=tf_obj(0.0, 2.0, 0.0, 6.0, 1.0, 6.0, 0.0, 0.0, 0.0, 0.0))

    parachoque = Node("Parachoque", geom=geo_parachoque,
                     transform=tf_obj(-6.0, 3.0, 0.0, 0.5, 2.0, 12.0, 0.0, 0.0, 0.0, 0.0))

    # Volante (posicionado na frente do carro, inclinado)
    volante = Node("Volante", geom=geo_volante,
                  transform=tf_obj(-1.9, 4.5, 3.0, 1.0, 1.0, 1.0, 90.0, 0.0, 1.0, 0.0),
                  state={"ang_volante": 0.0})

    parede_traseira = Node("ParedeTraseira", geom=geo_parede_traseira,
                          transform=tf_obj(6.0, 3.5, 0.0, 0.5, 3.0, 12.0, 0.0, 0.0, 0.0, 0.0))

    parede_lat_esq_diant = Node("ParedeLateralEsqDiant", geom=geo_parede_lateral,
                                transform=tf_obj(-4.0, 3.0, 6.0, 4.0, 3.0, 0.3, 0.0, 0.0, 0.0, 0.0))

    porta_esquerda = Node("PortaEsquerda", geom=geo_porta, transform=tf_porta_esquerda,
                         state={"ang_porta": 0.0})
    porta_esq_geom = Node("PortaEsqGeom", geom=geo_porta,
                         transform=tf_obj(0.0, 0.0, 0.0, 4.0, 3.0, 0.3, 0.0, 0.0, 0.0, 0.0))
    porta_esquerda.add(porta_esq_geom)

    parede_lat_esq_tras = Node("ParedeLateralEsqTras", geom=geo_parede_lateral,
                               transform=tf_obj(4.0, 3.5, 6.0, 4.0, 3.0, 0.3, 0.0, 0.0, 0.0, 0.0))

    parede_lat_dir_diant = Node("ParedeLateralDirDiant", geom=geo_parede_lateral,
                                transform=tf_obj(-4.0, 3.0, -6.0, 4.0, 3.0, 0.3, 0.0, 0.0, 0.0, 0.0))

    porta_direita = Node("PortaDireita", geom=geo_porta, transform=tf_porta_direita,
                        state={"ang_porta": 0.0})
    porta_dir_geom = Node("PortaDirGeom", geom=geo_porta,
                         transform=tf_obj(0.0, 0.0, 0.0, 4.0, 3.0, 0.3, 0.0, 0.0, 0.0, 0.0))
    porta_direita.add(porta_dir_geom)

    parede_lat_dir_tras = Node("ParedeLateralDirTras", geom=geo_parede_lateral,
                               transform=tf_obj(4.0, 3.5, -6.0, 4.0, 3.0, 0.3, 0.0, 0.0, 0.0, 0.0))

    capo = Node("Capo", geom=geo_capo,
               state={"ang_capo": 0.0},
            transform=tf_obj(-4.0, 4.25, 0.0, 4, 0.5, 12.0, 0.0, 0.0, 0.0, 0.0))

    global PORTA_ESQUERDA, PORTA_DIREITA, CAPO
    PORTA_ESQUERDA = porta_esquerda
    PORTA_DIREITA = porta_direita
    CAPO = capo

    # Chão
    chao = Node("Chão", geom=draw_chao,
                transform=tf_obj(0.0, -1.0, 0.0, 1.1, 1.1, 1.1, 0.0, 0.0, 0.0, 0.0))

    garagem = Node("Garagem", geom=draw_chao)

    # Garagem
    parede1 = Node("Parede", geom=geo_parede,
                transform=tf_obj(-20.0, 5.0, -10.0, 20.0, 10.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    parede2 = Node("Parede", geom=geo_parede,
                transform=tf_obj(-20.0, 5.0, 10.0, 20.0, 10.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    parede3 = Node("Parede", geom=geo_parede,
                transform=tf_obj(-30.0, 5.0, 0.0, 20.0, 10.0, 1.0, 90.0, 0.0, 1.0, 0.0))
    teto = Node("Teto", geom=geo_parede,
                transform=tf_obj(-20.0, 10.0, 0.0, 20.0, 20.0, 1.0, 90.0, 1.0, 0.0, 0.0))

    # Portão da garagem
    portao = Node("Portao", geom=geo_portao, transform=tf_portao_garagem,
                  state={"ang_portao": 0.0})

    global PORTAO_GARAGEM
    PORTAO_GARAGEM = portao


    world.add(


        carro.add(
            roda1,
            roda2,
            roda3,
            roda4,
            corpo,
            parachoque,
            volante,
            parede_traseira,
            parede_lat_esq_diant,
            porta_esquerda,
            parede_lat_esq_tras,
            parede_lat_dir_diant,
            porta_direita,
            parede_lat_dir_tras,
            capo
        ),
        chao,
        garagem.add(
            parede1,
            parede2,
            parede3,
            teto,
            portao
        )
    )

    return world


# -------------------------------
# OpenGL Setup
# -------------------------------
WIN_W, WIN_H = 800, 600
last_time = 0.0
SCENE = None
CARRO = None
PORTAO_GARAGEM = None
PORTA_ESQUERDA = None
PORTA_DIREITA = None
CAPO = None
tex_floor = None
# Camera control (user-controllable)
camera_distance = 35.0
camera_angle_h = 45.0
camera_angle_v = 20.0
camera_height = 15.0
min_camera_height = 1.0

def init_gl():
    global tex_floor
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    glEnable(GL_LIGHTING)

    # LIGHT0 - Luz principal (branca, direcional, vinda de cima)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0.45, 0.9, 0.35, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.18, 0.18, 0.22, 1.0))

    # LIGHT1 - Luz secundária (laranja/quente, posicional, do lado da garagem)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, (-25.0, 8.0, 0.0, 1.0))  # Posicional (w=1.0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  (1.0, 0.7, 0.4, 1.0))    # Cor laranja/quente
    glLightfv(GL_LIGHT1, GL_AMBIENT,  (0.1, 0.05, 0.0, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.8, 0.6, 0.3, 1.0))

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Configurar modo de textura (mas não ativar ainda)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    
    tex_floor = load_texture("Mosaico.png", repeat=True)

def reshape(w, h):
    global WIN_W, WIN_H
    WIN_W, WIN_H = max(1, w), max(1, h)
    glViewport(0, 0, WIN_W, WIN_H)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, WIN_W/float(WIN_H), 0.1, 1000.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display():
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    # "A posição da cãmara deverá poder ser controlada pelo utilizador"
    cam_x = camera_distance * math.cos(math.radians(camera_angle_v)) * math.sin(math.radians(camera_angle_h))
    cam_y = camera_height + camera_distance * math.sin(math.radians(camera_angle_v))
    if cam_y < min_camera_height:
        cam_y = min_camera_height
    cam_z = camera_distance * math.cos(math.radians(camera_angle_v)) * math.cos(math.radians(camera_angle_h))
    gluLookAt(cam_x, cam_y, cam_z,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

    SCENE.draw()
    glutSwapBuffers()


# -------------------------------
# Animação e Controlo
# -------------------------------
def idle():
    global last_time
    t_ms = glutGet(GLUT_ELAPSED_TIME)
    t = t_ms * 0.001
    if last_time == 0.0:
        last_time = t
    dt = t - last_time
    last_time = t

    SCENE.update(dt)
    glutPostRedisplay()


def keyboard(key, x, y):
    global CARRO

    # debug
    print(f"keyboard: {key}")

    if key == b'\x1b':  # ESC
        try:
            glutLeaveMainLoop()
        except Exception:
            sys.exit(0)

    # resolve carro node
    carro = CARRO if CARRO is not None else (SCENE.children[0] if SCENE and SCENE.children else None)
    if carro is None:
        return

    print("carro.x =", carro.state.get("x"), "vel =", carro.state.get("vel"))

    if key == b's' or key == b'S':
        carro.state["vel"] = 5.0   # mover para +X
    elif key == b'w' or key == b'W':
        if carro.state.get("x", 0.0) > -20.0:
            carro.state["vel"] = -5.0  # mover para -X
        else:
            carro.state["vel"] = 0.0
    elif key == b' ':
        carro.state["vel"] = 0.0   # parar
    elif key == b'g' or key == b'G':  # Abrir/fechar portão da garagem
        if PORTAO_GARAGEM and CARRO:
            # Verificar se o carro está no meio do portão
            x_carro = CARRO.state.get("x", 0.0)
            frente_carro = x_carro - 6.0
            traseira_carro = x_carro + 6.0

            # Portão está entre x = -10 e x = -8 aproximadamente
            # Bloquear se o carro está atravessando o portão
            if frente_carro < -8.0 and traseira_carro > -10.0:
                print("Não é possível fechar o portão: carro está no meio!")
            else:
                PORTAO_GARAGEM.state["ang_portao"] = 90.0 if PORTAO_GARAGEM.state["ang_portao"] == 0.0 else 0.0
        glutPostRedisplay()
    elif key == b'e' or key == b'E':  # Abrir/fechar porta esquerda
        if PORTA_ESQUERDA is not None:
            if PORTA_ESQUERDA.state["ang_porta"] < 5.0:
                PORTA_ESQUERDA.state["ang_porta"] = 60.0
            else:
                PORTA_ESQUERDA.state["ang_porta"] = 0.0
        glutPostRedisplay()
    elif key == b'd' or key == b'D':  # Abrir/fechar porta direita
        if PORTA_DIREITA is not None:
            if PORTA_DIREITA.state["ang_porta"] < 5.0:
                PORTA_DIREITA.state["ang_porta"] = 60.0
            else:
                PORTA_DIREITA.state["ang_porta"] = 0.0
        glutPostRedisplay()


def special_keys(key, x, y):
    """Função para controlar a camera conforme o enunciado, pelo utilizador)."""
    global camera_angle_h, camera_angle_v, camera_distance, camera_height
    if key == GLUT_KEY_LEFT:
        camera_angle_h -= 5.0
    elif key == GLUT_KEY_RIGHT:
        camera_angle_h += 5.0
    elif key == GLUT_KEY_UP:
        camera_angle_v = min(80.0, camera_angle_v + 5.0)
    elif key == GLUT_KEY_DOWN:
        camera_angle_v = max(-80.0, camera_angle_v - 5.0)
    elif key == GLUT_KEY_PAGE_UP:
        camera_distance = max(5.0, camera_distance - 2.0)
    elif key == GLUT_KEY_PAGE_DOWN:
        camera_distance = min(200.0, camera_distance + 2.0)
    glutPostRedisplay()


# -------------------------------
# Main
# -------------------------------
def main():
    global SCENE
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Grafo de Cena OO - Carro no eixo X")

    init_gl()
    SCENE = build_scene()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutMainLoop()


if __name__ == "__main__":
    main()
