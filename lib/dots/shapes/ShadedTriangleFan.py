from __future__ import division

import math

class ShadedTriangleFan(object):
    # chromosome = CV{7}
    # C = rgba
    # V = xyrgba

    def __init__(self, chromosome):
        center_color = chromosome[:4]
        xs = chromosome[4:len(chromosome):6]
        ys = chromosome[5:len(chromosome):6]
        center_x, center_y = sum(xs) / len(xs), sum(ys) / len(ys)
        vertex_count = (len(chromosome) - 4) // 6
        vertices = [chromosome[4 + i * 6:10 + i * 6]
                    for i in xrange(vertex_count)]
        def angle(vertex):
            x, y, r, g, b, a = vertex
            return math.atan2(y - center_y, x - center_x)
        vertices.sort(key=angle)
        chromosome = []
        chromosome.extend(center_color)
        for vertex in vertices:
            chromosome.extend(vertex)
        self.chromosome = tuple(chromosome)

    @staticmethod
    def generate(random):
        center_x, center_y = random.random(), random.random()
        radius = 0.1 * random.random()
        center_color = [random.random() for _ in xrange(4)]
        center_color[3] /= 2
        vertex_color = list(center_color)
        vertex_color[3] /= 2
        chromosome = []
        chromosome.extend(center_color)
        for _ in xrange(7):
            angle = 2 * math.pi * random.random()
            chromosome.append(center_x + radius * math.cos(angle))
            chromosome.append(center_y + radius * math.sin(angle))
            chromosome.extend(vertex_color)
        return ShadedTriangleFan(chromosome)

    def mutate(self, random):
        chromosome = list(self.chromosome)
        i = random.randrange(len(chromosome))
        chromosome[i] += random.choice([-1, 1]) * 0.1 * random.random()
        chromosome[i] = max(0, min(chromosome[i], 1))
        return ShadedTriangleFan(chromosome)

    def draw(self, graphics):
        graphics.draw_shaded_triangle_fan(self.chromosome)
