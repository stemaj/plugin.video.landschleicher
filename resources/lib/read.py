import io

def load_file(fileSuffix):
    with io.open('resources/tests/file.'+fileSuffix, 'rb') as fo:
        data = fo.read()
    return data
