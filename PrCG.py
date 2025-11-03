# Projecto de Computação Gráfica 

import sys, math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


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

def draw_chao():
    S = 100.0
    T = 50.0
    glColor3f(0.2, 0.8, 0.2)
    glNormal3f(0, 1, 0)

    glBegin(GL_QUADS)
    glVertex3f(-S, 0.0,  S)
    glVertex3f( S, 0.0,  S)
    glVertex3f( S, 0.0, -S)
    glVertex3f(-S, 0.0, -S)
    glEnd()


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

# update no eixo X
def update_carro(node, dt):
    # integrate velocity
    node.state["x"] += node.state.get("vel", 0.0) * dt

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

    # As rodas com x = -5.0 são consideradas traseiras, que são maiores às dianteiras
    roda1 = Node("R1", geom=geo_roda_traseira,
                transform=tf_obj(-5.0, 0.0, -5.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    
    roda2 = Node("R2", geom=geo_roda_traseira,
                transform=tf_obj(-5.0, 0.0, 5.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda3 = Node("R3", geom=geo_roda_dianteira,
                transform=tf_obj( 5.0, 0.0, 5.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))
    roda4 = Node("R4", geom=geo_roda_dianteira, 
                transform=tf_obj( 5.0, 0.0, -5.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0))

    # Corpo
    corpo = Node("Corpo", geom=geo_corpo, 
                transform=tf_obj(0.0, 2.0, 0.0, 6.0, 1.0, 6.0, 0.0, 0.0, 0.0, 0.0))

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
    
    
    world.add(

        
        carro.add(
            roda1,
            roda2, 
            roda3, 
            roda4,
            corpo
        ),
        chao,
        garagem.add(
            parede1,
            parede2,
            parede3,
            teto
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

def init_gl():
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

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)


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
    gluLookAt(25.0, 15.0, 20.0,  0.0, 0.0, 0.0,  0.0, 1.0, 0.0)

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

    if key == b's':
        carro.state["vel"] = 5.0   # mover para +X
    elif key == b'w':
        if carro.state.get("x", 0.0) > -20.0:
            carro.state["vel"] = -5.0  # mover para -X
        else:
            carro.state["vel"] = 0.0
    elif key == b' ':
        carro.state["vel"] = 0.0   # parar


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
    glutMainLoop()


if __name__ == "__main__":
    main()
