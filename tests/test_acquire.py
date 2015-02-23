# -*- coding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=R0904


import unittest

from gutenberg.acquire import load_metadata
from gutenberg.acquire import load_etext


class TestAcquireMetadata(unittest.TestCase):
    def test_load_metadata(self):
        metadata = load_metadata()
        self.assertGreater(len(list(metadata.query(r'''
            SELECT $ebook
            WHERE { $ebook a pgterms:ebook. }
        '''))), 0)
        self.assertGreater(len(list(metadata.query(r'''
            SELECT $author
            WHERE { [] a pgterms:ebook ; dcterms:creator $author. }
        '''))), 0)
        self.assertGreater(len(list(metadata.query(r'''
            SELECT $title
            WHERE { [] a pgterms:ebook ; dcterms:title $title. }
        '''))), 0)


class TestAcquireText(unittest.TestCase):
    newstyle_etextno = 2701
    oldstyle_etextno = 5
    unicode_etextno = 14287

    def test_load_etext(self):
        loaders = (lambda etextno: load_etext(etextno, refresh_cache=True),
                   lambda etextno: load_etext(etextno, refresh_cache=False))
        for load in loaders:
            mobydick = load(TestAcquireText.newstyle_etextno)
            constitution = load(TestAcquireText.oldstyle_etextno)
            ilemysterieuse = load(TestAcquireText.unicode_etextno)

            self.assertIsInstance(mobydick, unicode)
            self.assertIsInstance(constitution, unicode)
            self.assertIsInstance(ilemysterieuse, unicode)
            self.assertIn(u'Moby Dick; or The Whale', mobydick)
            self.assertIn(u"The United States' Constitution", constitution)
            self.assertIn(u"L'île mystérieuse", ilemysterieuse)
