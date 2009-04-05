from __future__ import division

import os, pyglet, random, sys
import PIL.Image, PIL.ImageChops, PIL.ImageStat
from pyglet.gl import *
from dots.DotsImage import DotsImage
from dots.Graphics import Graphics
from dots.io import load, save
from dots.shapes.Circle import Circle
from dots.shapes.ShadedCircle import ShadedCircle
from dots.shapes.Triangle import Triangle

dir_path = os.path.dirname(os.path.abspath(__file__))

class DotsWindow(pyglet.window.Window):
    def __init__(self, config):
        self.goal_image_path = config['goal']
        shape_factory_name = config.get('shape', 'random')
        self.shape_factory = self.get_shape_factory(shape_factory_name)
        caption = 'Dots: %s' % os.path.split(self.goal_image_path)[1]
        pyglet.window.Window.__init__(self, width=256, height=256,
                                      caption=caption)
        self.goal_image = PIL.Image.open(self.goal_image_path).convert('RGB')
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        circle_texture = self.load_circle_texture()
        self.graphics = Graphics(circle_texture)
        self.dots_image_path = ('%s.dots' %
                                os.path.splitext(self.goal_image_path)[0])
        try:
            self.dots_image = load(self.dots_image_path)
        except Exception, e:
            shape_count = config.get('count', 256)
            self.dots_image = DotsImage.generate(shape_count,
                                                 self.shape_factory, random)
        self.screenshot = None
        self.fitness = None
        self.best_fitness = None
        self.best_dots_image = self.dots_image
        self.display_lists = {}
        pyglet.clock.schedule_interval_soft(self.step, 0.001)

    def get_shape_factory(self, name):
        def generate_random_shape(random):
            factory = random.choice([Circle.generate, Triangle.generate])
            return factory(random)
        factories = {
            'c': Circle.generate,
            'circle': Circle.generate,
            'C': ShadedCircle.generate,
            'shaded-circle': ShadedCircle.generate,
            'r': generate_random_shape,
            'random': generate_random_shape,
            't': Triangle.generate,
            'triangle': Triangle.generate,
        }
        return factories[name]

    def load_circle_texture(self):
        circle_path = os.path.join(dir_path, 'circle.png')
        circle_image = pyglet.image.load(circle_path)
        return circle_image.get_texture()

    def step(self, dt):
        if self.screenshot is not None:
            diff = PIL.ImageChops.difference(self.screenshot, self.goal_image)
            stat = PIL.ImageStat.Stat(diff)
            self.fitness = sum(stat.rms) / len(stat.rms) / 256
            if self.best_fitness is None or self.fitness < self.best_fitness:
                self.best_dots_image = self.dots_image
                self.best_fitness = self.fitness
                print "Fitness: %.9f" % self.best_fitness
            self.update_display_lists()
            self.dots_image = self.best_dots_image.mutate(self.shape_factory,
                                                          random)

    def update_display_lists(self):
        diff = set(self.display_lists).difference(self.best_dots_image.shapes)
        for shape in diff:
            glDeleteLists(self.display_lists.pop(shape), 1)

    def on_draw(self):
        self.clear()
        glPushMatrix()
        glScaled(self.width, self.height, 1)
        for shape in self.dots_image.shapes:
            if shape in self.display_lists:
                glCallList(self.display_lists[shape])
            else:
                self.display_lists[shape] = glGenLists(1)
                glNewList(self.display_lists[shape], GL_COMPILE_AND_EXECUTE)
                shape.draw(self.graphics)
                glEndList()
        glPopMatrix()
        self.screenshot = self.get_screenshot()

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
