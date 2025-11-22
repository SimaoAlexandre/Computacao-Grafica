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
    draw_cylinder(1.2, 0.5, (0.05, 0.05, 0.05))

def geo_jante(flip=False):
    glPushMatrix()
    if flip:
        glRotatef(180.0, 0.0, 1.0, 0.0)
        glTranslatef(0.0, 0.0, -0.6)

    # Aro da jante
    glColor3f(0.7, 0.7, 0.7)
    glutSolidTorus(0.1, 0.6, 12, 24)

    # Centro
    glColor3f(0.3, 0.3, 0.3)
    glutSolidSphere(0.2, 16, 16)

    for i in range(5):    # 5 raios
        glPushMatrix()
        glRotatef(i * 72.0, 0.0, 0.0, 1.0)
        glTranslatef(0.3, 0.0, 0.0)
        glScalef(0.6, 0.05, 0.05)
        glColor3f(0.4, 0.4, 0.4)
        glutSolidCube(1.0)
        glPopMatrix()

    glPopMatrix()

def draw_corpo(color):
    glColor3f(*color)
    glutSolidCube(2.0)

def geo_corpo():
    draw_corpo((0.8, 0.1, 0.1))

def geo_parede():
    glColor3f(0.8, 0.8, 0.9)
    glutSolidCube(1.0)

def geo_portao():
    glColor3f(0.3, 0.3, 0.3)
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

def geo_matricula(): #Inspirado na TP06 do 2-cube-textured.py
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tex_matricula)
    glColor3f(1.0, 1.0, 1.0)

    w = 7.0 # largura
    h = 1.5  # altura
    d = 0.05  # espessura

    glBegin(GL_QUADS)
    # Frente da matrícula (face principal com textura)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0); glVertex3f(-w/2, -h/2, d/2)
    glTexCoord2f(1, 0); glVertex3f( w/2, -h/2, d/2)
    glTexCoord2f(1, 1); glVertex3f( w/2,  h/2, d/2)
    glTexCoord2f(0, 1); glVertex3f(-w/2,  h/2, d/2)

    # Trás da matrícula
    glNormal3f(0, 0, -1)
    glTexCoord2f(1, 0); glVertex3f(-w/2, -h/2, -d/2)
    glTexCoord2f(0, 0); glVertex3f( w/2, -h/2, -d/2)
    glTexCoord2f(0, 1); glVertex3f( w/2,  h/2, -d/2)
    glTexCoord2f(1, 1); glVertex3f(-w/2,  h/2, -d/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)

def geo_volante():
    # Aro do volante (torus)
    glColor3f(0.1, 0.1, 0.1)  # Preto
    glutSolidTorus(0.15, 0.8, 16, 24)

    # Coluna central (cilindro pequeno)
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glutSolidSphere(0.25, 16, 16)
    glPopMatrix()

    for i in range(3):     # 3 barras radiais (raios do volante)
        glPushMatrix()
        angle = i * 120.0  # Dividir 360 graus por 3
        glRotatef(angle, 0.0, 0.0, 1.0)
        glTranslatef(0.4, 0.0, 0.0)  # Mover para o raio médio
        glScalef(0.8, 0.08, 0.1)  # Barra alongada e fina
        glColor3f(0.15, 0.15, 0.15)
        glutSolidCube(1.0)
        glPopMatrix()

def geo_vidro():
    # Desabilitar escrita no depth buffer para transparência bidirecional
    glDepthMask(GL_FALSE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glDisable(GL_CULL_FACE)

    # Manter iluminação ligada para reflexos suaves
    # Configurar material para reflexo ligeiro
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.3, 0.3, 0.3, 1.0))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 20.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (0.2, 0.2, 0.25, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.7, 0.8, 0.85, 0.15))

    # Vidro transparente com leve tom azulado
    glColor4f(0.7, 0.8, 0.9, 0.15)  # RGBA - alpha=0.15 para transparência com reflexo

    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)  # Normal para iluminação correta
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f( 0.5, -0.5, 0.0)
    glVertex3f( 0.5,  0.5, 0.0)
    glVertex3f(-0.5,  0.5, 0.0)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, -1.0)  # Normal oposta para a outra face
    glVertex3f(-0.5, -0.5, 0.0)
    glVertex3f(-0.5,  0.5, 0.0)
    glVertex3f( 0.5,  0.5, 0.0)
    glVertex3f( 0.5, -0.5, 0.0)
    glEnd()

    glEnable(GL_CULL_FACE)
    glDisable(GL_BLEND)

    # Reativar escrita no depth buffer
    glDepthMask(GL_TRUE)

def geo_arvore():
    # Tronco
    glColor3f(0.4, 0.26, 0.13)
    glPushMatrix()
    glRotatef(-90, 1, 0, 0) # Cilindro cresce em Z, rodar para Y
    glutSolidCylinder(0.8, 4.0, 12, 12)
    glPopMatrix()

    #(Cone 1)
    glColor3f(0.0, 0.5, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 3.0, 0.0)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(3.0, 5.0, 12, 12)
    glPopMatrix()

    #(Cone 2 - Topo)
    glColor3f(0.0, 0.7, 0.0)
    glPushMatrix()
    glTranslatef(0.0, 5.0, 0.0)
    glRotatef(-90, 1, 0, 0)
    glutSolidCone(2.5, 4.0, 12, 12)
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
    T = 50.0  # Quantas vezes multiplicar a textura no chão (menor -> tiles maiores para relva)

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


def tf_pos_carro(node):
    glTranslatef(node.state["x"], 0.0, node.state["z"])
    glRotatef(node.state.get("angle", 0.0), 0.0, 1.0, 0.0)

# mudar o angulo do portão da garagem
def tf_portao_garagem(node):
    ang = node.state.get("ang_portao", 0.0)
    glTranslatef(-10.0, 9.0, 0.0)
    glRotatef(ang, 0.0, 0.0, 1.0)
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

def tf_roda(node):
    ang = node.state.get("ang_roda", 0.0)
    glRotatef(ang, 0.0, 0.0, 1.0)

def tf_roda_dianteira(node):
    # A ordem das transformações é crucial! Queremos: M_final = M_steering * M_rolling
    # Assim, aplica-se Rolling ao vértice (primeiro), e depois Steering ao resultado.

    # 1. Direção (Steering)
    carro = CARRO
    if carro:
        steering_angle = carro.state.get("steering", 0.0)
        glRotatef(steering_angle, 0.0, 1.0, 0.0)

    # 2. Rotação da roda (Rolling)
    ang = node.state.get("ang_roda", 0.0)
    glRotatef(ang, 0.0, 0.0, 1.0)

def update_portao(node, dt):

    cur = node.state.get("ang_portao", 0.0)
    target = node.state.get("target_ang", cur)

    if abs(target - cur) < 1e-3:
        return

    speed = 20.0
    max_step = speed * dt
    diff = target - cur

    if diff > 0:
        step = min(max_step, diff)
    else:
        step = max(-max_step, diff)
    node.state["ang_portao"] = cur + step

def update_roda(node, dt):

    carro = CARRO
    if carro:
        vel = carro.state.get("vel", 0.0)
        raio = 1.2
        rot_speed = (vel / (2.0 * math.pi * raio)) * 360.0
        ang_atual = node.state.get("ang_roda", 0.0)
        node.state["ang_roda"] = ang_atual + rot_speed * dt

# update no eixo X
def update_carro(node, dt):
    vel = node.state.get("vel", 0.0)
    steering = node.state.get("steering", 0.0)
    angle = node.state.get("angle", 0.0)

    # --- Rotação do carro ---
    if abs(vel) > 0.01 and abs(steering) > 0.01:
        wheelbase = 10.0
        steering_rad = math.radians(steering)
        turning_radius = wheelbase / math.tan(steering_rad)
        angle += math.degrees(vel / turning_radius) * dt
        node.state["angle"] = angle

    # --- Movimento ---
    angle_rad = math.radians(angle)
    fwd_x = -math.cos(angle_rad)
    fwd_z =  math.sin(angle_rad)

    dx = fwd_x * vel * dt
    dz = fwd_z * vel * dt

    new_x = node.state["x"] + dx
    new_z = node.state["z"] + dz

    # --- Colisão com portão ---
    ang_portao = PORTAO_GARAGEM.state.get("ang_portao", 0.0)
    dentro_z = abs(node.state["z"]) < 10.0

    if ang_portao == 0.0 and dentro_z:
        frente = new_x + fwd_x * 6.0
        traseira = new_x - fwd_x * 6.0

        # Entrada
        if node.state["x"] > -8 and frente <= -8:
            node.state["vel"] = 0
            return

        # Saída
        if node.state["x"] < -10 and traseira >= -10:
            node.state["vel"] = 0
            return

    # --- Colisão com paredes da garagem ---
    # Definir bounding box do carro (aproximada)
    car_half_size = 6 # Carro tem largura ~12
    car_min_x, car_max_x = new_x - car_half_size, new_x + car_half_size
    car_min_z, car_max_z = new_z - car_half_size, new_z + car_half_size

    # Paredes: (min_x, max_x, min_z, max_z)
    walls = [
        (-30.5, -9.5, -11.0, -9.0), # Parede Z-10 (Sul)
        (-30.5, -9.5,  9.0, 11.0), # Parede Z+10 (Norte)
        (-31.0, -29.0, -11.0, 11.0) # Parede Traseira (Oeste)
    ]

    collision = False
    for (wx1, wx2, wz1, wz2) in walls:
        # Check overlap
        overlap_x = min(car_max_x, wx2) - max(car_min_x, wx1)
        overlap_z = min(car_max_z, wz2) - max(car_min_z, wz1)

        if overlap_x > 0 and overlap_z > 0:
            collision = True
            break
    
    if collision:
        node.state["vel"] = 0
        return

    # --- Colisão nas árvores ---
    trees = [(-15.0, 17.0), (-15.0, -17.0)]
    min_dist = 6.0 + 1.5 # Raio do carro (~6) + Raio da árvore (~1.5)

    for (tx, tz) in trees:
        dist_sq = (new_x - tx)**2 + (new_z - tz)**2
        if dist_sq < min_dist**2:
            node.state["vel"] = 0
            return

    # --- Atualizar posição ---
    node.state["x"] = new_x
    node.state["z"] = new_z

    # --- Limites do mundo ---
    x = node.state["x"]
    z = node.state["z"]

    if x <= -100:
        node.state["x"] = -100
        node.state["vel"] = 0
    elif x >= 100:
        node.state["x"] = 100
        node.state["vel"] = 0

    if z > 100:
        node.state["z"] = 100
    elif z < -100:
        node.state["z"] = -100


# -------------------------------
# Cena
# -------------------------------
def build_scene():
    world = Node("World")

    carro = Node("Carro", transform=tf_pos_carro, updater=update_carro,
                 state={"x": 20.0, "z": 0.0, "vel": 0.0, "angle": 0.0, "steering": 0.0})
    global CARRO
    CARRO = carro

    # RODAS DIANTEIRAS (com direção)
    roda1_pos = Node("R1_Pos",
                    transform=tf_obj(-5.0, 1.2, -6.5, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda1 = Node("R1_Dianteira", geom=lambda: [geo_roda_dianteira(), geo_jante(flip=False)],
                transform=tf_roda_dianteira,
                updater=update_roda,
                state={"ang_roda": 0.0})
    roda1_pos.add(roda1)

    roda2_pos = Node("R2_Pos",
                    transform=tf_obj(-5.0, 1.2, 6, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda2 = Node("R2_Dianteira", geom=lambda: [geo_roda_dianteira(), geo_jante(flip=True)],
                transform=tf_roda_dianteira,
                updater=update_roda,
                state={"ang_roda": 0.0})
    roda2_pos.add(roda2)

    # RODAS TRASEIRAS (sem direção)
    roda3_pos = Node("R3_Pos",
                    transform=tf_obj(5.0, 1.2, 6, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda3 = Node("R3_Traseira", geom=lambda: [geo_roda_traseira(), geo_jante(flip=True)],
                transform=tf_roda,
                updater=update_roda,
                state={"ang_roda": 0.0})
    roda3_pos.add(roda3)

    roda4_pos = Node("R4_Pos",
                    transform=tf_obj(5.0, 1.2, -6.6, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda4 = Node("R4_Traseira", geom=lambda: [geo_roda_traseira(), geo_jante(flip=False)],
                transform=tf_roda,
                updater=update_roda,
                state={"ang_roda": 0.0})
    roda4_pos.add(roda4)

    corpo = Node("Corpo", geom=geo_corpo,
                transform=tf_obj(0.0, 2.0, 0.0, 6.0, 1.0, 6.0, 0.0, 0.0, 0.0, 0.0))

    parachoque = Node("Parachoque", geom=geo_parachoque,
                     transform=tf_obj(-6.0, 3.0, 0.0, 0.5, 2.0, 12.0, 0.0, 0.0, 0.0, 0.0))

    def tf_volante(node):
        glTranslatef(-1.9, 4.5, 3.0)
        glRotatef(90.0, 0.0, 1.0, 0.0)
        # Girar o volante baseado no steering do carro
        if CARRO:
            steering = CARRO.state.get("steering", 0.0)
            glRotatef(steering * 3.0, 0.0, 0.0, 1.0)  # Multiplicar para efeito visual

    volante = Node("Volante", geom=geo_volante,
                  transform=tf_volante,
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

    matricula_tras = Node("MatriculaTras", geom=geo_matricula,
                           transform=tf_obj(6.3, 3.0, 0.0, 1.0, 1.0, 1.0, 90.0, 0.0, 1.0, 0.0))

    matricula_frente = Node("MatriculaFrente", geom=geo_matricula,
                         transform=tf_obj(-6.3, 3.0, 0.0, 1.0, 1.0, 1.0, -90.0, 0.0, 1.0, 0.0))

    vidro_frente = Node("VidroFrente", geom=geo_vidro,
                       transform=tf_obj(-3.0, 5.5, 0.0, 11.0, 2.0, 4.0, 90.0, 0.0, 1.0, 0.0))

    global PORTA_ESQUERDA, PORTA_DIREITA, CAPO
    PORTA_ESQUERDA = porta_esquerda
    PORTA_DIREITA = porta_direita
    CAPO = capo

    chao = Node("Chão", geom=draw_chao,
                transform=tf_obj(0.0, -1.0, 0.0, 1.1, 1.1, 1.1, 0.0, 0.0, 0.0, 0.0))

    garagem = Node("Garagem", geom=draw_chao)

    parede1 = Node("Parede", geom=geo_parede,
                transform=tf_obj(-20.0, 5.0, -10.0, 20.0, 10.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    parede2 = Node("Parede", geom=geo_parede,
                transform=tf_obj(-20.0, 5.0, 10.0, 20.0, 10.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    parede3 = Node("Parede", geom=geo_parede,
                transform=tf_obj(-30.0, 5.0, 0.0, 20.0, 10.0, 1.0, 90.0, 0.0, 1.0, 0.0))
    teto = Node("Teto", geom=geo_parede,
                transform=tf_obj(-20.0, 9.5, 0.0, 20.0, 20.0, 1.0, 90.0, 1.0, 0.0, 0.0))

    portao = Node("Portao", geom=geo_portao, transform=tf_portao_garagem,
                  updater=update_portao,
                  state={"ang_portao": 0.0, "target_ang": 0.0})

    global PORTAO_GARAGEM
    PORTAO_GARAGEM = portao

    world.add(

        carro.add(
            roda1_pos,
            roda2_pos,
            roda3_pos,
            roda4_pos,
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
            capo,
            matricula_frente,
            matricula_tras,
            vidro_frente  # Vidro por último para renderização correta de transparência
        ),
        chao,
        garagem.add(
            parede1,
            parede2,
            parede3,
            teto,
            portao
        ),
        Node("Arvore", geom=geo_arvore,
             transform=tf_obj(-15.0, 0.0, 17.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0)),
        Node("Arvore2", geom=geo_arvore,
             transform=tf_obj(-15.0, 0.0, -17.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
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
tex_matricula = None
# Camera control (user-controllable)
camera_mode = 0  # 0 = livre, 1 = 3ª pessoa, 2 = 1ª pessoa
camera_distance = 35.0
camera_angle_h = 45.0
camera_angle_v = 20.0
camera_height = 15.0
min_camera_height = 1.0

def init_gl():
    global tex_floor, tex_matricula

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)

    glEnable(GL_LIGHTING)

    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0.45, 0.9, 0.35, 0.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.18, 0.18, 0.22, 1.0))

    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, (-25.0, 8.0, 0.0, 1.0))  # Posicional (w=1.0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  (1.0, 0.7, 0.4, 1.0))    # Cor laranja/quente
    glLightfv(GL_LIGHT1, GL_AMBIENT,  (0.1, 0.05, 0.0, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0.8, 0.6, 0.3, 1.0))

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

    tex_floor = load_texture("Mosaico_Chao.png", repeat=True)
    tex_matricula = load_texture("Matrícula.png", repeat=False)

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

    # Estado do carro
    car_x = CARRO.state.get("x", 0.0)
    car_y = 2.5
    car_z = CARRO.state.get("z", 0.0)
    car_angle = math.radians(CARRO.state.get("angle", 0.0))

    # Vetores do carro
    fwd_x = -math.cos(car_angle)
    fwd_z =  math.sin(car_angle)
    right_x = -math.sin(car_angle)
    right_z = -math.cos(car_angle)

    if camera_mode == 0: # Camera livre
        ang_v = math.radians(camera_angle_v)
        ang_h = math.radians(camera_angle_h)

        cam_x = camera_distance * math.cos(ang_v) * math.sin(ang_h)
        cam_y = camera_height + camera_distance * math.sin(ang_v)
        cam_y = max(cam_y, min_camera_height)
        cam_z = camera_distance * math.cos(ang_v) * math.cos(ang_h)

        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    elif camera_mode == 1: # 3ª pessoa
        dist = 25.0
        height = 12.0

        cam_x = car_x - fwd_x * dist
        cam_y = car_y + height
        cam_z = car_z - fwd_z * dist

        gluLookAt(cam_x, cam_y, cam_z,
                  car_x, car_y + 4.0, car_z,
                  0, 1, 0)

    elif camera_mode == 2: # 1ª pessoa
        back = 3.0
        up = 4.0
        side = -3.0
        look_dist = 20.0

        cam_x = car_x - fwd_x * back + right_x * side
        cam_y = car_y + up
        cam_z = car_z - fwd_z * back + right_z * side

        gluLookAt(cam_x, cam_y, cam_z,
                  cam_x + fwd_x * look_dist,
                  cam_y,
                  cam_z + fwd_z * look_dist,
                  0, 1, 0)

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
    process_keys()  # Processar teclas mantidas pressionadas

    SCENE.update(dt)
    glutPostRedisplay()

keys_pressed = set() # Variáveis globais para controle contínuo

def keyboard(key, x, y):
    global CARRO, keys_pressed

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

    # Adicionar tecla ao conjunto de teclas pressionadas
    keys_pressed.add(key)

    print("carro.x =", carro.state.get("x"), "vel =", carro.state.get("vel"))

    if key == b'g' or key == b'G':  # Abrir/fechar portão da garagem (animado)
        if PORTAO_GARAGEM and CARRO:
            # Verificar se o carro está no meio do portão
            x_carro = CARRO.state.get("x", 0.0)
            angle = CARRO.state.get("angle", 0.0)
            angle_rad = math.radians(angle)
            frente_carro = x_carro - 6.0 * math.sin(angle_rad)
            traseira_carro = x_carro + 6.0 * math.sin(angle_rad)

            # Portão está entre x = -10 e x = -8 aproximadamente
            # Bloquear se o carro está atravessando o portão
            if frente_carro < 6.0 and traseira_carro > -10.0:
                print("Não é possível fechar/abrir o portão!")
            else:
                # Alterna o alvo (target) — o updater move `ang_portao` gradualmente
                cur_target = PORTAO_GARAGEM.state.get("target_ang", 0.0)
                # se o alvo atual for ~0, mudar para 90; caso contrário, fechar para 0
                PORTAO_GARAGEM.state["target_ang"] = 90.0 if abs(cur_target - 0.0) < 1e-3 else 0.0
        glutPostRedisplay()

    elif key == b'q' or key == b'Q':  # Abrir/fechar porta esquerda
        if PORTA_ESQUERDA is not None:
            if PORTA_ESQUERDA.state["ang_porta"] < 5.0:
                PORTA_ESQUERDA.state["ang_porta"] = 60.0
            else:
                PORTA_ESQUERDA.state["ang_porta"] = 0.0
        glutPostRedisplay()

    elif key == b'e' or key == b'E':  # Abrir/fechar porta direita
        if PORTA_DIREITA is not None:
            if PORTA_DIREITA.state["ang_porta"] < 5.0:
                PORTA_DIREITA.state["ang_porta"] = 60.0
            else:
                PORTA_DIREITA.state["ang_porta"] = 0.0
        glutPostRedisplay()

    elif key == b'c' or key == b'C':  # Alternar modo de câmara
        global camera_mode
        camera_mode = (camera_mode + 1) % 3
        mode_names = ["Câmara Livre", "3ª Pessoa", "1ª Pessoa"]
        print(f"Modo de câmara: {mode_names[camera_mode]}")
        glutPostRedisplay()

def keyboard_up(key, x, y):
    """Chamado quando uma tecla é solta"""
    global keys_pressed
    if key in keys_pressed:
        keys_pressed.remove(key)

def process_keys():
    global CARRO, keys_pressed
    if CARRO is None:
        return

    dt = 0.016 # aproximadamente 60 FPS
    max_speed = 30.0 # Aumentado para 30
    acceleration = 2.0 # unidades/s², a aceleração do carro
    braking_force = 15.0 # Travagem mais forte (era 5.0)

    max_steering = 35.0 # graus máximos de direção
    steering_speed = 120.0 # graus/s
    return_speed = 80.0 # graus/s

    vel = CARRO.state.get("vel", 0.0)
    steering = CARRO.state.get("steering", 0.0)

    # Normalizar teclas
    pressed = {k.lower() for k in keys_pressed}

    # --- Velocidade (W/S) e Travão (Espaço) ---
    if b" " in pressed: # Travão de mão / Travagem forte
        if abs(vel) > 0.1:
            # Travar contra o movimento
            sinal = 1 if vel > 0 else -1
            vel -= sinal * braking_force * dt
            # Se passar de 0, para
            if (sinal == 1 and vel < 0) or (sinal == -1 and vel > 0):
                vel = 0.0
        else:
            vel = 0.0

    elif b"w" in pressed:
        # Se está a andar para trás, trava forte (como o travão)
        if vel < -0.5:
            vel += braking_force * dt
            if vel > 0:
                vel = 0.0
        # Se está parado ou devagar, pode avançar
        else:
            vel = min(max_speed, vel + acceleration * dt)
    elif b"s" in pressed:
        # Se está a andar para a frente, trava forte (como o travão)
        if vel > 0.5:
            vel -= braking_force * dt
            if vel < 0:
                vel = 0.0
        # Se está parado ou devagar, pode recuar
        else:
            vel = max(-max_speed * 0.6, vel - acceleration * dt)
    else:
        # Fricção natural (sem premir nada) - mais suave
        if abs(vel) > 0.1:
            fric = 2.5 * dt # Fricção natural reduzida (era 5.0)
            vel -= fric if vel > 0 else -fric
        else:
            vel = 0.0

    # --- Direção (A/D) ---
    moving = abs(vel) > 0.5

    if moving:
        if b"a" in pressed:
            steering += steering_speed * dt  # Esquerda
        elif b"d" in pressed:
            steering -= steering_speed * dt  # Direita
        else:
            # Voltar ao centro
            if abs(steering) > 0.5:
                steering -= return_speed * dt * (1 if steering > 0 else -1)
            else:
                steering = 0.0
    else:
        # Sem movimento, roda recentra igual
        if abs(steering) > 0.5:
            steering -= return_speed * dt * (1 if steering > 0 else -1)
        else:
            steering = 0.0

    # Limites finais
    steering = max(-max_steering, min(max_steering, steering))

    CARRO.state["vel"] = vel
    CARRO.state["steering"] = steering

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
    glutCreateWindow(b"Projeto de Computacao Grafica - Grupo 06")

    init_gl()
    SCENE = build_scene()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_up)
    glutSpecialFunc(special_keys)
    glutMainLoop()


if __name__ == "__main__":
    main()
