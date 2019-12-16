import os
import pickle
import pprint
import tempfile

from contextlib import contextmanager


class Config(object):
    realpath = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(realpath, 'data')
    db_path = os.path.join(data_path, 'db.p')


@contextmanager
def _tempfile(*args, **kwargs):
    fd, name = tempfile.mkstemp(*args, **kwargs)
    os.close(fd)
    try:
        yield name
    finally:
        try:
            os.remove(name)
        except OSError as e:
            if e.errno == 2:
                pass
            else:
                raise e


@contextmanager
def open_atomic(filepath, *args, **kwargs):
    fsync = kwargs.pop('fsync', False)

    with _tempfile(dir=os.path.dirname(filepath)) as tmppath:
        with open(tmppath, *args, **kwargs) as f:
            yield f
            if fsync:
                f.flush()
                os.fsync(f.fileno())
        os.rename(tmppath, filepath)


def safe_pickle_dump(obj, fname):
    with open_atomic(fname, 'wb') as f:
        pickle.dump(obj, f, -1)


def pickle_load(fname):
    try:
        db = pickle.load(open(fname, 'rb'))
    except Exception as e:
        print('error loading existing database:\n{}\nstarting from an empty database'.format(e))
        db = {}
    return db


def preview(problem):
    print('\n문제:')
    n_col = len(problem['env'][0])
    print('   |' + ''.join(['{:3d}|'.format(x) for x in list(range(n_col))]))
    print('---|' + ('---|')*n_col)
    for idx, line in enumerate(problem['env']):
        print('{:2d}'.format(idx), end=' |')
        for element in line:
            if element == 0:
                element = '  '
            print(' {}'.format(element), end='|')
        print()
        print('---|' + ('---|')*n_col)

    print('\n정답:')
    pprint.pprint(problem['words'])


def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')
