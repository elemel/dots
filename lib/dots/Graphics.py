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

    def draw_shaded_circle(self, center, radius, colors):
        glPushMatrix()
        glTranslated(center[0], center[1], 0)
        glScaled(radius, radius, 1)
        glEnable(self.circle_texture.target)
        glBindTexture(self.circle_texture.target, self.circle_texture.id)
        glBegin(GL_QUADS)
        glColor4d(colors[0][0], colors[0][1], colors[0][2], colors[0][3] / 2)
        glTexCoord2d(0, 0)
        glVertex2d(-0.5, -0.5)
        glColor4d(colors[1][0], colors[1][1], colors[1][2], colors[1][3] / 2)
        glTexCoord2d(0, 1)
        glVertex2d(-0.5, 0.5)
        glColor4d(colors[2][0], colors[2][1], colors[2][2], colors[2][3] / 2)
        glTexCoord2d(1, 1)
        glVertex2d(0.5, 0.5)
        glColor4d(colors[3][0], colors[3][1], colors[3][2], colors[3][3] / 2)
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

    def draw_shaded_triangle_fan(self, chromosome):
        r, g, b, a = chromosome[:4]
        xs = chromosome[4:len(chromosome):3]
        ys = chromosome[5:len(chromosome):3]
        glPushMatrix()
        glBegin(GL_TRIANGLE_FAN)
        glColor4d(r, g, b, a / 2)
        glVertex2d(sum(xs) / len(xs), sum(ys) / len(ys))
        for i in xrange((len(chromosome) - 4) // 3):
            x, y, a = chromosome[4 + i * 3:7 + i * 3]
            glColor4d(r, g, b, a / 2)
            glVertex2d(x, y)
        x, y, a = chromosome[4:7]
        glColor4d(r, g, b, a / 2)
        glVertex2d(x, y)
        glEnd()
        glPopMatrix()
