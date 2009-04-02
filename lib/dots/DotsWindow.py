from __future__ import division

import os, pyglet, random, sys
import PIL.Image, PIL.ImageChops, PIL.ImageStat
from pyglet.gl import *
from dots.Dot import Dot
from dots.DotsImage import DotsImage
from dots.io import load, save

dir_path = os.path.dirname(os.path.abspath(__file__))

class DotsWindow(pyglet.window.Window):
    def __init__(self, goal_path):
        caption = 'Dots: %s' % os.path.split(goal_path)[1]
        pyglet.window.Window.__init__(self, width=256, height=256,
                                      caption=caption)
        self.goal_path = goal_path
        self.goal = PIL.Image.open(goal_path).convert('RGB')
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.dot_texture = self.load_dot_texture()
        self.dots_image_path = '%s.dots' % os.path.splitext(self.goal_path)[0]
        try:
            self.dots_image = load(self.dots_image_path)
        except Exception, e:
            self.dots_image = DotsImage.generate(256, Dot.generate, random)
        self.screenshot = None
        self.fitness = None
        self.best_fitness = None
        self.best_dots_image = self.dots_image
        self.display_lists = {}
        pyglet.clock.schedule_interval_soft(self.step, 0.001)

    def load_dot_texture(self):
        dot_path = os.path.join(dir_path, 'dot.png')
        dot_image = pyglet.image.load(dot_path)
        return dot_image.get_texture()

    def step(self, dt):
        if self.screenshot is not None:
            diff = PIL.ImageChops.difference(self.screenshot, self.goal)
            stat = PIL.ImageStat.Stat(diff)
            self.fitness = sum(stat.rms) / len(stat.rms) / 256
            if self.best_fitness is None or self.fitness < self.best_fitness:
                self.best_dots_image = self.dots_image
                self.best_fitness = self.fitness
                print "Fitness: %.9f" % self.best_fitness
            for element in set(self.display_lists).difference(self.best_dots_image.elements):
                glDeleteLists(self.display_lists.pop(element), 1)
            self.dots_image = self.best_dots_image.mutate(Dot.generate, random)

    def on_draw(self):
        glClearColor(0, 0, 0, 0)
        self.clear()
        glLoadIdentity()
        glScaled(self.width, self.height, 1)
        for element in self.dots_image.elements:
            if element in self.display_lists:
                glCallList(self.display_lists[element])
            else:
                self.display_lists[element] = glGenLists(1)
                glNewList(self.display_lists[element], GL_COMPILE_AND_EXECUTE)
                self.draw_dot(element)
                glEndList()
        self.screenshot = self.get_screenshot()

    def draw_dot(self, dot):
        glPushMatrix()
        glTranslated(dot.x, dot.y, 0)
        glScaled(dot.radius, dot.radius, 1)
        glColor4d(dot.red, dot.green, dot.blue, dot.alpha / 2)
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
        save(self.best_dots_image, self.dots_image_path)
        self.save_screenshot()
        self.close()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            self.on_close()

    def save_screenshot(self):
        if self.screenshot is not None:
            self.screenshot.save(self.dots_image_path + '.png')

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
