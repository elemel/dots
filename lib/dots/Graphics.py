from __future__ import division

from pyglet.gl import *

class Graphics(object):
    def __init__(self, circle_texture):
        self.circle_texture = circle_texture

    def draw_circle(self, x, y, radius, red, green, blue, alpha):
        glPushMatrix()
        glTranslated(x, y, 0)
        glScaled(radius, radius, 1)
        glColor4d(red, green, blue, alpha / 2)
        glEnable(self.circle_texture.target)
        glBindTexture(self.circle_texture.target, self.circle_texture.id)
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
        glDisable(self.circle_texture.target)
        glPopMatrix()

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, red, green, blue, alpha):
        glPushMatrix()
        glColor4d(red, green, blue, alpha / 2)
        glBegin(GL_TRIANGLES)
        glVertex2d(x1, y1)
        glVertex2d(x2, y2)
        glVertex2d(x3, y3)
        glEnd()
        glPopMatrix()
