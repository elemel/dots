import os, pyglet, random, sys
from pyglet.gl import *

dir_path = os.path.dirname(os.path.abspath(__file__))

class DotsWindow(pyglet.window.Window):
    def __init__(self):
        pyglet.window.Window.__init__(self, width=256, height=256,
                                      caption='Dots')
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        dot_path = os.path.join(dir_path, 'dot.png')
        dot_image = pyglet.image.load(dot_path)
        self.dot_texture = dot_image.get_texture()
        self.dots = [self.generate_dot() for _ in xrange(256)]

    def on_draw(self):
        glClearColor(0, 0, 0, 0)
        self.clear()
        glLoadIdentity()
        glScaled(self.width ** 2 / self.dot_texture.width,
                 self.height ** 2 / self.dot_texture.height, 1)
        for dot in self.dots:
            self.draw_dot(dot)

    def generate_dot(self):
        r = random.random
        center = r(), r()
        radius = r()
        color = r(), r(), r(), r()
        return center, radius, color

    def draw_dot(self, dot):
        center, radius, color = dot
        x, y = center
        glPushMatrix()
        glTranslated(x, y, 0)
        glScaled(radius, radius, 1)
        glColor4d(*color)
        glEnable(self.dot_texture.target)
        glBindTexture(self.dot_texture.target, self.dot_texture.id)
        glBegin(GL_QUADS)
        glTexCoord2d(0, 0)
        glVertex2d(-0.5, -0.5)
        glTexCoord2d(0, 1)
        glVertex2d(-0.5, 0.5)
        glTexCoord2d(1, 1)
        glVertex2d(0.5, 0.5)
        glTexCoord2d(1, 0)
        glVertex2d(0.5, -0.5)
        glEnd()
        glDisable(self.dot_texture.target)
        glPopMatrix()

    def on_close(self):
        self.close()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.save_image()
            self.close()

    def save_image(self):
        image_path = os.path.join(dir_path, 'image.png')
        color_buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        color_buffer.texture.save(image_path)
