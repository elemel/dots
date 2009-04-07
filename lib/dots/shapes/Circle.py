from pyglet.gl import *
from dots.shapes.Shape import Shape

class Circle(Shape):
    chromosome_len = 7

    @property
    def x(self):
        return self.chromosome[0]

    @property
    def y(self):
        return self.chromosome[1]

    @property
    def radius(self):
        return self.chromosome[2]

    @property
    def red(self):
        return self.chromosome[3]

    @property
    def green(self):
        return self.chromosome[4]

    @property
    def blue(self):
        return self.chromosome[5]

    @property
    def alpha(self):
        return self.chromosome[6]

    @classmethod
    def generate(cls, random):
        chromosome = [random.random() for _ in xrange(cls.chromosome_len)]
        chromosome[2] *= random.choice([0.01, 0.1, 1])
        return cls(chromosome)

    def draw(self, graphics):
        texture = graphics.circle_texture
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)
        glColor4d(self.red, self.green, self.blue, self.alpha / 2)
        glBegin(GL_QUADS)
        glTexCoord2d(0, 0)
        glVertex2d(self.x - self.radius / 2, self.y - self.radius / 2)
        glTexCoord2d(0, 1)
        glVertex2d(self.x - self.radius / 2, self.y + self.radius / 2)
        glTexCoord2d(1, 1)
        glVertex2d(self.x + self.radius / 2, self.y + self.radius / 2)
        glTexCoord2d(1, 0)
        glVertex2d(self.x + self.radius / 2, self.y - self.radius / 2)
        glEnd()
        glDisable(texture.target)
