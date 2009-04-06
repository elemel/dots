from __future__ import division

from itertools import chain
from math import atan2, cos, pi, sin
from pyglet.gl import *

__all__ = 'ShadedTriangleFan'

class ShadedTriangleFan(object):
    # chromosome = CV{7}
    # C = rgba
    # V = xya

    def __init__(self, color, vertices):
        self.color = tuple(color)
        self.vertices = tuple(tuple(v) for v in vertices)

    @staticmethod
    def generate(random):
        center_x, center_y = random.random(), random.random()
        color = [random.random() for _ in xrange(4)]
        radius = 0.1 * random.random()
        vertices = []
        for _ in xrange(7):
            angle = 2 * pi * random.random()
            vertex_x = center_x + radius * cos(angle)
            vertex_y = center_y + radius * sin(angle)
            vertices.append((vertex_x, vertex_y, 0))
        return ShadedTriangleFan(color, vertices)

    @staticmethod
    def decode(chromosome):
        chromosome = tuple(chromosome)
        color = chromosome[:4]
        vertex_count = (len(chromosome) - 4) // 3
        vertices = [chromosome[4 + i * 3:7 + i * 3]
                    for i in xrange(vertex_count)]
        return ShadedTriangleFan(color, vertices)

    def encode(self):
        return self.color + tuple(chain(*self.vertices))

    def mutate(self, random):
        chromosome = list(self.encode())
        i = random.randrange(len(chromosome))
        sigma = random.choice([0.001, 0.01, 0.1])
        chromosome[i] = random.normalvariate(chromosome[i], sigma)
        chromosome[i] = max(0, min(chromosome[i], 1))
        return ShadedTriangleFan.decode(chromosome)

    def draw(self, graphics):
        r, g, b, center_a = self.color
        xs = [x for x, y, a in self.vertices]
        ys = [y for x, y, a in self.vertices]
        center_x, center_y = sum(xs) / len(xs), sum(ys) / len(ys)
        glBegin(GL_TRIANGLE_FAN)
        glColor4d(r, g, b, center_a / 2)
        glVertex2d(center_x, center_y)
        def angle(vertex):
            vertex_x, vertex_y, vertex_a = vertex
            return atan2(vertex_y - center_y, vertex_x - center_x)
        vertices = sorted(self.vertices, key=angle)
        for vertex_x, vertex_y, vertex_a in vertices:
            glColor4d(r, g, b, vertex_a / 2)
            glVertex2d(vertex_x, vertex_y)
        vertex_x, vertex_y, vertex_a = vertices[0]
        glColor4d(r, g, b, vertex_a / 2)
        glVertex2d(vertex_x, vertex_y)
        glEnd()
