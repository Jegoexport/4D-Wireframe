from engine import *

degree = 0.017453292519943295

def keys(cube):
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

            if event.key == pg.K_a:
                cube.rotate(np.array([degree, 0, 0, 0, 0, 0]))
            if event.key == pg.K_d:
                cube.rotate(np.array([-degree, 0, 0, 0, 0, 0]))

            if event.key == pg.K_s:
                cube.rotate(np.array([0, degree, 0, 0, 0, 0]))
            if event.key == pg.K_w:
                cube.rotate(np.array([0, -degree, 0, 0, 0, 0]))

            if event.key == pg.K_q:
                cube.rotate(np.array([0, 0, degree, 0, 0, 0]))
            if event.key == pg.K_e:
                cube.rotate(np.array([0, 0, -degree, 0, 0, 0]))

            if event.key == pg.K_r:
                cube.rotate(np.array([0, 0, 0, degree, 0, 0]))
            if event.key == pg.K_f:
                cube.rotate(np.array([0, 0, 0, -degree, 0, 0]))

            if event.key == pg.K_p:
                setattr(cube, 'rotation', np.array([0, 0, 0, 0, 0, 0]))


def main():
    #load object from json
    with open('exampleObject.json') as f:
        data = json.load(f)
    cubeVertices = data['vertices']
    cubeEdges = data['edges']
    cube = mesh(cubeVertices, cubeEdges)

    #initalize 4D engine
    main = engine()
    cam = camera()

    # initalize pygame
    pg.init()
    screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)
    pygame.display.set_caption('4D Wireframe')

    while True:
        keys(cube)
        main.update(screen, [cube], cam)

if __name__ == '__main__':
    main()
