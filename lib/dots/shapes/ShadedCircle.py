class ShadedCircle(object):
    def __init__(self, center, radius, colors):
        self.center = tuple(center)
        self.radius = radius
        self.colors = tuple(tuple(color) for color in colors)

    @staticmethod
    def generate(random):
        center = random.random(), random.random()
        radius = random.random() ** 3
        color = tuple(random.random() for _ in xrange(4))
        colors = tuple(color for _ in xrange(4))
        return ShadedCircle(center, radius, colors)

    def mutate(self, random):
        values = list(self.center) + [self.radius]
        for color in self.colors:
            values.extend(color)
        i = random.randrange(len(values))
        values[i] += random.choice([-1, 1]) * random.random() ** 3
        values[i] = max(0, min(values[i], 1))
        center = values[:2]
        radius = values[2]
        colors = values[3:7], values[7:11], values[11:15], values[15:19]
        return ShadedCircle(center, radius, colors)

    def draw(self, graphics):
        graphics.draw_shaded_circle(self.center, self.radius, self.colors)
