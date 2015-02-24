# -*- coding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=R0904


import unittest

from tests.util import MockMetadataMixin
from tests.util import MockTextMixin
from tests.util import NEWSTYLE_ETEXTNO
from tests.util import OLDSTYLE_ETEXTNO
from tests.util import UNICODE_ETEXTNO

from gutenberg.acquire import load_etext
from gutenberg.acquire import load_metadata


class TestAcquireMetadata(MockMetadataMixin, unittest.TestCase):
    def test_load_metadata(self):
        metadata = load_metadata()
        self.assertEqual(len(list(metadata.query(r'''
            SELECT $ebook
            WHERE { $ebook a pgterms:ebook. }
        '''))), 3)
        self.assertEqual(len(list(metadata.query(r'''
            SELECT $author
            WHERE { [] a pgterms:ebook ; dcterms:creator $author. }
        '''))), 3)
        self.assertEqual(len(list(metadata.query(r'''
            SELECT $title
            WHERE { [] a pgterms:ebook ; dcterms:title $title. }
        '''))), 3)


class TestAcquireText(MockTextMixin, unittest.TestCase):
    def test_load_etext(self):
        loaders = (lambda etextno: load_etext(etextno, refresh_cache=True),
                   lambda etextno: load_etext(etextno, refresh_cache=False))
        for load in loaders:
            mobydick = load(NEWSTYLE_ETEXTNO)
            constitution = load(OLDSTYLE_ETEXTNO)
            ilemysterieuse = load(UNICODE_ETEXTNO)

            self.assertIsInstance(mobydick, unicode)
            self.assertIsInstance(constitution, unicode)
            self.assertIsInstance(ilemysterieuse, unicode)
            self.assertIn(u'Moby Dick; or The Whale', mobydick)
            self.assertIn(u"The United States' Constitution", constitution)
            self.assertIn(u"L'île mystérieuse", ilemysterieuse)
