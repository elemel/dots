import pyglet, sys, getopt
import PIL.Image
from dots.DotsWindow import DotsWindow

def main():
    opts, args = getopt.getopt(sys.argv[1:], 'n:s:', ['count=', 'shape='])
    if len(args) != 1:
        print "Usage: dots [<options>] <goal>"
        sys.exit(1)
    config = {}  
    config['goal'] = args[0]
    for opt, opt_arg in opts:
        if opt in ['-n', '--count']:
            config['count'] = int(opt_arg)
        if opt in ['-s', '--shape']:
            config['shape'] = opt_arg
    window = DotsWindow(config)
    pyglet.app.run()

if __name__ == '__main__':
    main()
