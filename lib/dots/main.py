import pyglet, sys
import PIL.Image
from dots.DotsWindow import DotsWindow

def main():
    if len(sys.argv) != 2:
        print "Usage: dots <goal>"
        sys.exit(1)
    window = DotsWindow(sys.argv[1])
    pyglet.app.run()

if __name__ == '__main__':
    main()
