# -*- coding: utf-8 -*-
"""Module to deal with text acquisition."""


import contextlib
import urllib2


def _urlopen(*args, **kwargs):
    """Wrapper for urllib2.urlopen to make the function usable in
    with-statements.

    """
    return contextlib.closing(urllib2.urlopen(*args, **kwargs))


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
        return '{root}/{path}/{etextno}/{etextno}.txt'.format(
            root=uri_root,
            path='/'.join(etextno[:len(etextno) - 1]),
            etextno=etextno)


def fetch_etext(etextno):
    """Returns a unicode representation of the full body of a Project Gutenberg
    text (makes a remote call to Project Gutenberg's servers).

    """
    download_uri = _format_download_uri(etextno)
    with _urlopen(download_uri) as response:
        encoding = response.headers.getparam('charset') or 'utf-8'
        return response.read().decode(encoding)


if __name__ == '__main__':
    # pylint: disable=C0111
    # pylint: disable=R0904
    import unittest

    class Test(unittest.TestCase):
        newstyle_etextno = 2701
        oldstyle_etextno = 5
        unicode_etextno = 14287

        def test_fetch_etext(self):
            mobydick = fetch_etext(Test.newstyle_etextno)
            constitution = fetch_etext(Test.oldstyle_etextno)
            ilemysterieuse = fetch_etext(Test.unicode_etextno)

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
