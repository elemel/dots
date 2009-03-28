import pyglet, sys
import PIL.Image
from dots.DotsWindow import DotsWindow

def main():
    if len(sys.argv) != 2:
        print "Usage: dots <goal>"
        sys.exit(1)
    goal = PIL.Image.open(sys.argv[1]).convert('RGB')
    window = DotsWindow(goal)
    pyglet.app.run()

if __name__ == '__main__':
    main()
