# -*- coding: utf-8 -*-
# pylint: disable=C0111
# pylint: disable=R0904
# pylint: disable=W0212


from gzip import GzipFile
from os import remove
from tempfile import NamedTemporaryFile
import unittest

from gutenberg.acquire import load_metadata
from gutenberg.acquire import load_etext


def _mock_metadata_cache():
    with NamedTemporaryFile(delete=False, suffix='nt.gz') as metadata_file:
        with GzipFile(fileobj=metadata_file, mode='wb') as gzip_file:
            gzip_file.write('\n'.join([
                r'<http://www.gutenberg.org/ebooks/2701> '
                r'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
                r'<http://www.gutenberg.org/2009/pgterms/ebook> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/2701> '
                r'<http://purl.org/dc/terms/creator> '
                r'<http://www.gutenberg.org/2009/agents/9> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/2701> '
                r'<http://purl.org/dc/terms/title> '
                r'"Moby Dick; Or, The Whale" '
                r'.',
                r'<http://www.gutenberg.org/ebooks/5> '
                r'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
                r'<http://www.gutenberg.org/2009/pgterms/ebook> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/5> '
                r'<http://purl.org/dc/terms/creator> '
                r'<http://www.gutenberg.org/2009/agents/1> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/5> '
                r'<http://purl.org/dc/terms/title> '
                r'"The United States Constitution" '
                r'.',
                r'<http://www.gutenberg.org/ebooks/14287> '
                r'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
                r'<http://www.gutenberg.org/2009/pgterms/ebook> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/14287> '
                r'<http://purl.org/dc/terms/creator> '
                r'<http://www.gutenberg.org/2009/agents/60> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/14287> '
                r'<http://purl.org/dc/terms/title> '
                r'"L\'\u00EEle myst\u00E9rieuse" '
                r'.',
            ]))

    return metadata_file.name


class TestAcquireMetadata(unittest.TestCase):
    def setUp(self):
        import gutenberg.acquire.metadata
        self.mock_metadata_cache = _mock_metadata_cache()
        gutenberg.acquire.metadata._METADATA_CACHE = self.mock_metadata_cache

    def tearDown(self):
        remove(self.mock_metadata_cache)

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
