class Dot(object):
    def __init__(self, x, y, radius, red, green, blue, alpha):
        self.x = x
        self.y = y
        self.radius = radius
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    @staticmethod
    def generate(random):
        x, y = random.random(), random.random()
        radius = random.random() ** 3
        red, green, blue = random.random(), random.random(), random.random()
        alpha = random.random()
        return Dot(x, y, radius, red, green, blue, alpha)

    def mutate(self, random):
        values = [self.x, self.y, self.radius,
                  self.red, self.green, self.blue, self.alpha]
        i = random.randrange(len(values))
        values[i] += random.choice([-1, 1]) * random.random() ** 3
        values[i] = max(0, min(values[i], 1))
        return Dot(*values)
