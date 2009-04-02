import cPickle as pickle

def load(path):
    file_obj = open(path)
    try:
        return pickle.load(file_obj)
    finally:
        file_obj.close()

def save(dots_image, path):
    file_obj = open(path, 'w')
    try:
        pickle.dump(dots_image, file_obj, pickle.HIGHEST_PROTOCOL)
    finally:
        file_obj.close()
