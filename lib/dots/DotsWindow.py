import os, pyglet, random, sys
import PIL.Image, PIL.ImageChops, PIL.ImageStat
from pyglet.gl import *

dir_path = os.path.dirname(os.path.abspath(__file__))

class DotsWindow(pyglet.window.Window):
    def __init__(self, goal):
        pyglet.window.Window.__init__(self, width=256, height=256,
                                      caption='Dots')
        self.goal = goal
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
        screenshot = self.get_screenshot()
        diff = PIL.ImageChops.difference(screenshot, self.goal)
        stat = PIL.ImageStat.Stat(diff)
        print stat.rms

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
            image = self.get_pil_image()
            image.save('dots.png')
            self.close()

    def get_screenshot(self):
        buffer_manager = pyglet.image.get_buffer_manager()
        color_buffer = buffer_manager.get_color_buffer()
        image_data = color_buffer.image_data
        pil_image = PIL.Image.frombuffer(image_data.format,
                                         (image_data.width, image_data.height),
                                         image_data.data, 'raw',
                                         image_data.format, 0, 1)
        pil_image = pil_image.convert('RGB')
        pil_image = pil_image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        return pil_image
