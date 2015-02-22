"""Module to handle os-level interactions."""


from __future__ import absolute_import
import errno
import os
import shutil


def makedirs(*args, **kwargs):
    """Wrapper around os.makedirs that doesn't raise an exception if the
    directory already exists.

    """
    try:
        os.makedirs(*args, **kwargs)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise


def remove(path):
    """Wrapper that switches between os.remove and shutil.rmtree depending on
    whether the provided path is a file or directory.

    """
    if not os.path.exists(path):
        return

    if os.path.isdir(path):
        return shutil.rmtree(path)

    if os.path.isfile(path):
        return os.remove(path)
