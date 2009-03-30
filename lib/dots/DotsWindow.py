from __future__ import division

import os, pyglet, random, sys
import cPickle as pickle
import PIL.Image, PIL.ImageChops, PIL.ImageStat
from pyglet.gl import *

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
        self.dot_textures = self.load_dot_textures()
        self.dots_path = '%s.dots' % os.path.splitext(self.goal_path)[0]
        try:
            dots_file = open(self.dots_path)
            try:
                self.dots = pickle.load(dots_file)
            finally:
                dots_file.close()
        except Exception, e:
            print e
            self.dots = self.generate_dots()
        self.screenshot = None
        self.fitness = None
        self.best_fitness = None
        self.best_dots = self.dots
        pyglet.clock.schedule_interval_soft(self.step, 0.001)

    def load_dot_textures(self):
        dot_textures = []
        for i in xrange(16):
            dot_path = os.path.join(dir_path, 'dot-%d.png' % i)
            dot_image = pyglet.image.load(dot_path)
            dot_texture = dot_image.get_texture()
            dot_textures.append(dot_texture)
        return dot_textures

    def step(self, dt):
        if self.screenshot is not None:
            diff = PIL.ImageChops.difference(self.screenshot, self.goal)
            stat = PIL.ImageStat.Stat(diff)
            rms = stat.rms
            self.fitness = sum(rms) / len(rms) / 256
            if self.best_fitness is None or self.fitness < self.best_fitness:
                self.best_dots = self.dots
                self.best_fitness = self.fitness
                print "Fitness: %.9f" % self.best_fitness
            self.dots = self.mutate_dots(self.best_dots)

    def on_draw(self):
        glClearColor(0, 0, 0, 0)
        self.clear()
        glLoadIdentity()
        glScaled(self.width ** 2 / self.dot_textures[0].width,
                 self.height ** 2 / self.dot_textures[0].height, 1)
        for dot in self.dots:
            self.draw_dot(dot)
        self.screenshot = self.get_screenshot()

    def draw_dot(self, dot):
        x, y, radius, blur, red, green, blue, alpha = dot
        i = min(int(blur * 16), 15)
        glPushMatrix()
        glTranslated(x, y, 0)
        glScaled(radius, radius, 1)
        glColor4d(red, green, blue, alpha / 2)
        glEnable(self.dot_textures[i].target)
        glBindTexture(self.dot_textures[i].target, self.dot_textures[i].id)
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
        glDisable(self.dot_textures[i].target)
        glPopMatrix()

    def generate_dots(self):
        return tuple(self.generate_dot() for _ in xrange(256))

    def mutate_dots(self, dots):
        mutation = random.choice([self.move_dot, self.replace_dot,
                                  self.mutate_dot])
        return mutation(dots)

    def move_dot(self, dots):
        dots = list(dots)
        i = random.randrange(len(dots))
        j = random.randrange(len(dots))
        dot = dots.pop(i)
        dots.insert(j, dot)
        return tuple(dots)

    def replace_dot(self, dots):
        dots = list(dots)
        i = random.randrange(len(dots))
        j = random.randrange(len(dots))
        dots.pop(i)
        dots.insert(j, self.generate_dot())
        return tuple(dots)

    def mutate_dot(self, dots):
        dots = list(dots)
        i = random.randrange(len(dots))
        dot = list(dots[i])
        j = random.randrange(len(dot))
        dot[j] += random.choice([-1, 1]) * random.random() ** 3
        dot[j] = max(0, min(dot[j], 1))
        dots[i] = tuple(dot)
        return tuple(dots)

    def generate_dot(self):
        return tuple(random.random() for _ in xrange(8))

    def on_close(self):
        self.close()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            dots_file = open(self.dots_path, 'w')
            try:
                pickle.dump(self.best_dots, dots_file, pickle.HIGHEST_PROTOCOL)
            finally:
                dots_file.close()
            if self.screenshot is not None:
                self.screenshot.save(self.dots_path + '.png')
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
