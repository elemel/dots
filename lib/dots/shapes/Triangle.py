import math
from dots.shapes.Gene import Gene
from dots.shapes.Shape import Shape

class Triangle(Shape):
    chromosome_len = 10

    x1 = Gene(0)
    y1 = Gene(1)
    x2 = Gene(2)
    y2 = Gene(3)
    x3 = Gene(4)
    y3 = Gene(5)
    red = Gene(6)
    green = Gene(7)
    blue = Gene(8)
    alpha = Gene(9)

    @classmethod
    def generate(cls, random):
        center = random.random(), random.random()
        scale = random.random() * random.choice([0.01, 0.1, 1])
        chromosome = []
        for _ in xrange(3):
            vertex = [x + random.choice([-1, 1]) * scale * random.random()
                      for x in center]
            chromosome.extend(vertex)
        color = [random.random() for _ in xrange(4)]
        chromosome.extend(color)
        return cls(chromosome)

    def draw(self, gl, textures):
        gl.glColor4d(self.red, self.green, self.blue, self.alpha / 2)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex2d(self.x1, self.y1)
        gl.glVertex2d(self.x2, self.y2)
        gl.glVertex2d(self.x3, self.y3)
        gl.glEnd()
