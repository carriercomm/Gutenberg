# pylint: disable=C0111
# pylint: disable=R0904


import os
import shutil
import tempfile
import unittest

from gutenberg._util.os import makedirs
from gutenberg._util.os import remove


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
