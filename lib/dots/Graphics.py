from __future__ import division

from pyglet.gl import *

class Graphics(object):
    def __init__(self, circle_texture):
        self.circle_texture = circle_texture

    def draw_shaded_circle(self, center, radius, color, alphas):
        x, y = center
        r, g, b = color
        a1, a2, a3, a4 = alphas
        glPushMatrix()
        glTranslated(x, y, 0)
        glScaled(radius, radius, 1)
        glEnable(self.circle_texture.target)
        glBindTexture(self.circle_texture.target, self.circle_texture.id)
        glBegin(GL_QUADS)
        glColor4d(r, g, b, a1 / 2)
        glTexCoord2d(0, 0)
        glVertex2d(-0.5, -0.5)
        glColor4d(r, g, b, a2 / 2)
        glTexCoord2d(0, 1)
        glVertex2d(-0.5, 0.5)
        glColor4d(r, g, b, a3 / 2)
        glTexCoord2d(1, 1)
        glVertex2d(0.5, 0.5)
        glColor4d(r, g, b, a4 / 2)
        glTexCoord2d(1, 0)
        glVertex2d(0.5, -0.5)
        glEnd()
        glDisable(self.circle_texture.target)
        glPopMatrix()

    def draw_shaded_triangle(self, chromosome):
        glPushMatrix()
        glBegin(GL_TRIANGLES)
        for i in xrange(3):
            x, y, r, g, b, a = chromosome[i * 6:(i + 1) * 6]
            glColor4d(r, g, b, a / 2)
            glVertex2d(x, y)
        glEnd()
        glPopMatrix()
