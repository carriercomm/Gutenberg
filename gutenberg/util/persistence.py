"""Module to deal with storing data files on disk."""


import errno
import os


def _root():
    """Returns the directory at which all other persisted files are rooted.

    """
    default_root = os.path.expanduser('~/gutenberg_data')
    return os.environ.get('GUTENBERG_DATA', default_root)


def _makedirs(*args, **kwargs):
    """Wrapper around os.makedirs that does not fail when the directories
    already exist.

    """
    try:
        return os.makedirs(*args, **kwargs)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def local_file(path):
    """Returns a path that the caller may use to store local files.

    """
    path = os.path.join(_root(), path)
    _makedirs(os.path.dirname(path))
    return path
