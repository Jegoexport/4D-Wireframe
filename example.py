from engine import *
import numpy as np

degree = 0.0017453292519943296 # .1 degrees
rotation = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


def keys(cube):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

            if event.key == pg.K_a:
                rotation[0] += degree
            if event.key == pg.K_d:
                rotation[0] -= degree

            if event.key == pg.K_s:
                rotation[1] += degree
            if event.key == pg.K_w:
                rotation[1] -= degree

            if event.key == pg.K_q:
                rotation[2] += degree
            if event.key == pg.K_e:
                rotation[2] -= degree

            if event.key == pg.K_r:
                rotation[3] += degree
            if event.key == pg.K_f:
                rotation[3] -= degree

            if event.key == pg.K_p:
                setattr(cube, 'rotation', np.array([0, 0, 0, 0, 0, 0]))

def main():
    # load object from json
    with open('exampleObject.json') as f:
        data = json.load(f)
    cubeVertices = data['vertices']
    cubeEdges = data['edges']
    cube = mesh(cubeVertices, cubeEdges)

    # initialize 4D engine
    eng = engine()
    cam = camera()

    # initialize pygame
    pg.init()
    screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
    pygame.display.set_caption('4D Wireframe')

    while True:
        cube.rotate(rotation)
        keys(cube)
        eng.update(screen, [cube], cam)


if __name__ == '__main__':
    main()
