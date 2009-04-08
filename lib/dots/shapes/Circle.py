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

    def draw(self, gl, textures):
        texture = textures['circle']
        gl.glEnable(texture.target)
        gl.glBindTexture(texture.target, texture.id)
        gl.glColor4d(self.red, self.green, self.blue, self.alpha / 2)
        gl.glBegin(gl.GL_QUADS)
        gl.glTexCoord2d(0, 0)
        gl.glVertex2d(self.x - self.radius / 2, self.y - self.radius / 2)
        gl.glTexCoord2d(0, 1)
        gl.glVertex2d(self.x - self.radius / 2, self.y + self.radius / 2)
        gl.glTexCoord2d(1, 1)
        gl.glVertex2d(self.x + self.radius / 2, self.y + self.radius / 2)
        gl.glTexCoord2d(1, 0)
        gl.glVertex2d(self.x + self.radius / 2, self.y - self.radius / 2)
        gl.glEnd()
        gl.glDisable(texture.target)
