# -*- coding: utf-8 -*-
"""Module to deal with text acquisition."""


import gzip
import os

import requests

from gutenberg.util.persistence import local_file
from gutenberg.util.types import validate_etextno


def _format_download_uri(etextno):
    """Returns the download location on the Project Gutenberg servers for a
    given text.

    """
    uri_root = r'http://www.gutenberg.lib.md.us'

    if 0 < etextno < 10:
        oldstyle_files = (
            'when11',
            'bill11',
            'jfk11',
            'getty11',
            'const11',
            'liber11',
            'mayfl11',
            'linc211',
            'linc111',
        )
        etextno = int(etextno)
        return '{root}/etext90/{name}.txt'.format(
            root=uri_root,
            name=oldstyle_files[etextno - 1])

    else:
        etextno = str(etextno)
        extensions = ('.txt', '-8.txt')
        for extension in extensions:
            uri = '{root}/{path}/{etextno}/{etextno}{extension}'.format(
                root=uri_root,
                path='/'.join(etextno[:len(etextno) - 1]),
                etextno=etextno,
                extension=extension)
            response = requests.head(uri)
            if response.ok:
                return uri
        raise ValueError('download URI for {} not supported'.format(etextno))


def fetch_etext(etextno, refresh_cache=False):
    """Returns a unicode representation of the full body of a Project Gutenberg
    text. After making an initial remote call to Project Gutenberg's servers,
    the text is persisted locally.

    """
    etextno = validate_etextno(etextno)
    cached = local_file(os.path.join('text', '{}.txt.gz'.format(etextno)))

    if refresh_cache or not os.path.exists(cached):
        download_uri = _format_download_uri(etextno)
        response = requests.get(download_uri)
        text = response.text
        with gzip.open(cached, 'w') as cache:
            cache.write(text.encode('utf-8'))
    else:
        with gzip.open(cached, 'r') as cache:
            text = cache.read().decode('utf-8')
    return text


if __name__ == '__main__':
    # pylint: disable=C0111
    # pylint: disable=R0904
    import functools
    import unittest

    class Test(unittest.TestCase):
        newstyle_etextno = 2701
        oldstyle_etextno = 5
        unicode_etextno = 14287

        def test_fetch_etext(self):
            fetchers = (functools.partial(fetch_etext, refresh_cache=True),
                        functools.partial(fetch_etext, refresh_cache=False))
            for fetch in fetchers:
                mobydick = fetch(Test.newstyle_etextno)
                constitution = fetch(Test.oldstyle_etextno)
                ilemysterieuse = fetch(Test.unicode_etextno)

                self.assertIsInstance(mobydick, unicode)
                self.assertIsInstance(constitution, unicode)
                self.assertIsInstance(ilemysterieuse, unicode)
                self.assertIn(u'Moby Dick; or The Whale', mobydick)
                self.assertIn(u"The United States' Constitution", constitution)
                self.assertIn(u"L'île mystérieuse", ilemysterieuse)

        def test_format_download_uri(self):
            self.assertEquals(
                _format_download_uri(Test.newstyle_etextno),
                r'http://www.gutenberg.lib.md.us/2/7/0/2701/2701.txt',
                'bad download-uri for newstyle e-text')
            self.assertEquals(
                _format_download_uri(Test.oldstyle_etextno),
                r'http://www.gutenberg.lib.md.us/etext90/const11.txt',
                'bad download-uri for oldstyle e-text')
            self.assertEquals(
                _format_download_uri(Test.unicode_etextno),
                r'http://www.gutenberg.lib.md.us/1/4/2/8/14287/14287-8.txt',
                'bad download-uri for unicode e-text')

    unittest.main()
