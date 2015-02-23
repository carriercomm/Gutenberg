# -*- coding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=R0904


import unittest

from gutenberg._domain_model.vocabulary import DCTERMS
from gutenberg._domain_model.vocabulary import PGTERMS
from gutenberg.acquire.metadata import load_metadata
from gutenberg.acquire.text import _format_download_uri
from gutenberg.acquire.text import load_etext


class TestAcquireMetadata(unittest.TestCase):
    def test_load_metadata(self):
        metadata = load_metadata()
        self.assertGreater(len(list(metadata[::PGTERMS.ebook])), 0)
        self.assertGreater(len(list(metadata[:DCTERMS.creator:])), 0)
        self.assertGreater(len(list(metadata[:DCTERMS.subject:])), 0)
        self.assertGreater(len(list(metadata.query(r'''
            SELECT (SAMPLE($author) AS $author)
                   (COUNT($ebook) AS $num_ebooks)
            WHERE { $ebook rdf:type pgterms:ebook.
                    $author dcterms:creator $ebook. }
            GROUP BY $author
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

    def test_format_download_uri(self):
        self.assertEquals(
            _format_download_uri(TestAcquireText.newstyle_etextno),
            r'http://www.gutenberg.lib.md.us/2/7/0/2701/2701.txt',
            'bad download-uri for newstyle e-text')
        self.assertEquals(
            _format_download_uri(TestAcquireText.oldstyle_etextno),
            r'http://www.gutenberg.lib.md.us/etext90/const11.txt',
            'bad download-uri for oldstyle e-text')
        self.assertEquals(
            _format_download_uri(TestAcquireText.unicode_etextno),
            r'http://www.gutenberg.lib.md.us/1/4/2/8/14287/14287-8.txt',
            'bad download-uri for unicode e-text')
