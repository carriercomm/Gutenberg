# pylint: disable=C0111
# pylint: disable=R0903
# pylint: disable=R0904


import os
import shutil
import tempfile
import unittest

from gutenberg._util.objects import all_subclasses
from gutenberg._util.os import makedirs
from gutenberg._util.os import remove


class TestUtilObjects(unittest.TestCase):
    def test_all_subclasses(self):
        class Root(object):
            pass

        class AB(Root):
            pass

        class ABC(AB):
            pass

        class AD(Root):
            pass

        class ABAD(AB, AD):
            pass

        class ABADE(ABAD):
            pass

        self.assertItemsEqual(all_subclasses(Root), [AB, ABC, AD, ABAD, ABADE])
        self.assertSetEqual(all_subclasses(ABADE), set())


class TestUtilOs(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.mkdtemp()
        self.temporary_file = tempfile.NamedTemporaryFile(delete=False).name

    def tearDown(self):
        if os.path.exists(self.temporary_directory):
            shutil.rmtree(self.temporary_directory)
        if os.path.exists(self.temporary_file):
            os.remove(self.temporary_file)

    def test_remove(self):
        for path in (self.temporary_file, self.temporary_directory):
            self.assertTrue(os.path.exists(path))
            remove(path)
            self.assertFalse(os.path.exists(path))

    def test_makedirs(self):
        path = os.path.join(self.temporary_directory, 'foo', 'bar', 'baz')
        self.assertFalse(os.path.exists(path))
        makedirs(path)
        self.assertTrue(os.path.exists(path))
