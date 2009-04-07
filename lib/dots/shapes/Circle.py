from pyglet.gl import *
from dots.shapes.Gene import Gene
from dots.shapes.Shape import Shape

class Circle(Shape):
    chromosome_len = 7

    x = Gene(0)
    y = Gene(1)
    radius = Gene(2)
    red = Gene(3)
    green = Gene(4)
    blue = Gene(5)
    alpha = Gene(6)

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
