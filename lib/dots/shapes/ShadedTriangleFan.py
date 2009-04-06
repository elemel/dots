from __future__ import division

from itertools import chain
from math import atan2, cos, pi, sin
from pyglet.gl import *

__all__ = 'ShadedTriangleFan'

class ShadedTriangleFan(object):
    # chromosome = CV{7}
    # C = rgba
    # V = xya

    def __init__(self, chromosome):
        xs = chromosome[4:len(chromosome):3]
        ys = chromosome[5:len(chromosome):3]
        center_x, center_y = sum(xs) / len(xs), sum(ys) / len(ys)
        vertex_count = (len(chromosome) - 4) // 3
        vertices = [chromosome[4 + i * 3:7 + i * 3]
                    for i in xrange(vertex_count)]
        def angle(vertex):
            x, y, a = vertex
            return atan2(y - center_y, x - center_x)
        chromosome = chromosome[:4]
        chromosome.extend(chain(*sorted(vertices, key=angle)))
        self.chromosome = tuple(chromosome)

    @staticmethod
    def generate(random):
        x, y = random.random(), random.random()
        color = [random.random() for _ in xrange(4)]
        radius = 0.1 * random.random()
        chromosome = []
        chromosome.extend(color)
        for _ in xrange(7):
            angle = 2 * pi * random.random()
            chromosome.append(x + radius * cos(angle))
            chromosome.append(y + radius * sin(angle))
            chromosome.append(0)
        return ShadedTriangleFan(chromosome)

    def mutate(self, random):
        chromosome = list(self.chromosome)
        i = random.randrange(len(chromosome))
        chromosome[i] += random.choice([-1, 1]) * 0.1 * random.random()
        chromosome[i] = max(0, min(chromosome[i], 1))
        return ShadedTriangleFan(chromosome)

    def draw(self, graphics):
        r, g, b, a = self.chromosome[:4]
        xs = self.chromosome[4:len(self.chromosome):3]
        ys = self.chromosome[5:len(self.chromosome):3]
        glBegin(GL_TRIANGLE_FAN)
        glColor4d(r, g, b, a / 2)
        glVertex2d(sum(xs) / len(xs), sum(ys) / len(ys))
        for i in xrange((len(self.chromosome) - 4) // 3):
            x, y, a = self.chromosome[4 + i * 3:7 + i * 3]
            glColor4d(r, g, b, a / 2)
            glVertex2d(x, y)
        x, y, a = self.chromosome[4:7]
        glColor4d(r, g, b, a / 2)
        glVertex2d(x, y)
        glEnd()
