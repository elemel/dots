import math

class Triangle(object):
    def __init__(self, x1, y1, x2, y2, x3, y3, red, green, blue, alpha):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    @staticmethod
    def generate(random):
        x, y = random.random(), random.random()
        radius = random.random() ** 3
        a1, a2, a3 = [2 * math.pi * random.random() for _ in xrange(3)]
        x1, y1 = x + radius * math.cos(a1), y + radius * math.sin(a1)
        x2, y2 = x + radius * math.cos(a2), y + radius * math.sin(a2)
        x3, y3 = x + radius * math.cos(a3), y + radius * math.sin(a3)
        red, green, blue, alpha = [random.random() for _ in xrange(4)]
        return Triangle(x1, y1, x2, y2, x3, y3, red, green, blue, alpha)

    def mutate(self, random):
        values = [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3,
                  self.red, self.green, self.blue, self.alpha]
        i = random.randrange(len(values))
        values[i] += random.choice([-1, 1]) * random.random() ** 3
        values[i] = max(0, min(values[i], 1))
        return Triangle(*values)

    def draw(self, graphics):
        graphics.draw_triangle(self.x1, self.y1, self.x2, self.y2,
                               self.x3, self.y3,
                               self.red, self.green, self.blue, self.alpha)
