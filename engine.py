import pygame
import pygame as pg
import numpy as np
import math
import time
import json


class engine:
    def __init__(self, screen: pygame.Surface,
                 drawEdges: bool = 1, drawVertices: bool = 1, debug: bool = 0, ):
        self.screen = screen

        self.debug = debug
        self.drawEdges = drawEdges
        self.drawVertices = drawVertices
        if debug:
            self.now = time.time()
            if not pygame.font.get_init():
                pygame.font.init()
            self.font1 = pygame.font.SysFont('freesanbold.ttf', 50)

    def update(self, objects: list, camera):
        self.render(objects, camera)

    def renderDebug(self):
        self.last = self.now
        self.now = time.time()
        self.fps = round(1/(self.now - self.last))
        fps = self.font1.render(str(self.fps), True, (255, 255, 255) if self.fps > 30 else (255, 0, 0))
        fpsRect = fps.get_rect()
        fpsRect.center = (30, 20)
        self.screen.blit(fps, fpsRect)


    def render(self, objects, cam):
        self.screen.fill([0, 0, 0])

        for object in objects:
            vertices, edges, color = object.render()

            points = [self.projection(getattr(cam, 'CameraDirection'),
                                      getattr(cam, 'CameraPos') - vert,
                                      getattr(cam, 'CameraPos'),
                                      getattr(cam, 'point0'), 0.125)
                      for vert in vertices]

            if self.drawEdges:
                for i in edges:
                    pg.draw.line(self.screen, (0, 255, 0), points[i[0]] * self.screen.get_width(), points[i[1]] * self.screen.get_width())
            if self.drawVertices:
                for i in points:
                    pg.draw.circle(self.screen, color, i * self.screen.get_width(), 4)

        if self.debug:
            self.renderDebug()

        pg.display.flip()

    def projection(self, faceNormal, rayDirection, rayPoint, vert, scale, epsilon=1e-6):
        """intersection with plane"""
        ndotu = faceNormal.dot(rayDirection)
        # ray and plane are parallel if ndotu is close to 0
        if abs(ndotu) < epsilon:
            raise RuntimeError("no intersection or line is within plane")
        w = rayPoint - vert
        si = -faceNormal.dot(w) / ndotu
        Psi = w + si * rayDirection + vert  # calulate Intersectionpoint
        """Intersection with Camera"""
        r = (Psi[0]) * scale + 0.5
        s = (Psi[1]) * scale + 0.25
        return np.array([r, s])

class camera:
    def __init__(self):
        self.CameraDirection = np.array([0, 0, 1, 0])
        self.CameraPos = np.array([0, 0, -32, 0])
        self.point0 = np.array([2, 4, -2, 0])

class mesh:
    def __init__(self, vertices: tuple, edges: list,
                 rotation: np.ndarray = np.array([0,0,0,0,0,0]),
                 position: np.ndarray = np.array([(0,0,0,0)]),
                 color: list = (255,255,255)):
        self.vertices = vertices
        self.edges = edges
        self.rotation = rotation
        self.position = position
        self.color = color
        self.globalVertices = vertices

    def render(self) -> tuple:
        return self.globalVertices, self.edges, self.color

    def move(self, delta):
        self.position = self.position + delta
        self.renderTransformation()


    def rotate(self, delta):
        self.rotation = self.rotation + delta
        self.renderRotation()
        self.renderTransformation()


    def transform(self):
        self.renderRotation()
        self.renderTransformation()

    def renderRotation(self):
        def calcSinCos(rotation: float) -> (float, float):
            """
            Calculates sinus and cosinus

            :param rotation: rotation of object in radians
            :return: sinus, cosinus
            """
            return math.sin(rotation), math.cos(rotation)

        def calcRotation(oldPoint: tuple):
            """
            Applies the rotation to absolut position
            :param oldPoint: position of point, that should be rotated around the origin
            :return: returns position of the rotated point
            """
            newPoint = [0,0,0,0] #oldPoint[0:4]
            '''WZ-Rotation'''
            sin, cos, = calcSinCos(self.rotation[0])
            newPoint[0], newPoint[1] = cos * oldPoint[0] + sin * oldPoint[1], -sin * oldPoint[0] + cos * oldPoint[1]
            '''XY-Rotation'''
            sin, cos, = calcSinCos(self.rotation[5])
            newPoint[2], newPoint[3] = cos * oldPoint[2] - sin * oldPoint[3], sin * oldPoint[2] + cos * oldPoint[3]
            '''WY-Rotation'''
            sin, cos, = calcSinCos(self.rotation[1])
            newPoint[0], newPoint[2] = cos * newPoint[0] - sin * newPoint[2], sin * newPoint[0] + cos * newPoint[2]
            '''YZ-Rotation'''
            sin, cos, = calcSinCos(self.rotation[2])
            newPoint[0], newPoint[3] = cos * newPoint[0] - sin * newPoint[3], sin * newPoint[0] + cos * newPoint[3]
            '''WX-Rotation'''
            sin, cos, = calcSinCos(self.rotation[3])
            newPoint[1], newPoint[2] = cos * newPoint[1] + sin * newPoint[2], -sin * newPoint[1] + cos * newPoint[2]
            '''XZ-Rotation'''
            sin, cos, = calcSinCos(self.rotation[4])
            newPoint[1], newPoint[3] = cos * newPoint[1] - sin * newPoint[3], sin * newPoint[1] + cos * newPoint[3]
            return newPoint

        self.globalVertices = [calcRotation(vert) for vert in self.vertices]


    def renderTransformation(self):
        self.globalVertices = self.globalVertices + self.position

    def loadFromJson(self, path):
        """
        EXPERIMENTAL
        loads object data from json file
        :param path: path to json file
        """

        with open(path) as f:
            data = json.load(f)
        self.vertices = data['vertices']
        self.edges = data['edges']
        self.rotation = data['rotation']
        self.position = data['position']

