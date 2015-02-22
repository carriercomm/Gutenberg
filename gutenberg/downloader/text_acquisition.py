"""Module to deal with text acquisition."""


def _format_download_uri(etextno):
    raise NotImplementedError


def fetch_etext(etextno):
    raise NotImplementedError


if __name__ == '__main__':
    # pylint: disable=C0111
    # pylint: disable=R0904
    import unittest

    class Test(unittest.TestCase):
        mobydick_etextno = 2701
        constitution_etextno = 5

        def test_fetch_etext(self):
            mobydick = fetch_etext(Test.mobydick_etextno)
            constitution = fetch_etext(Test.constitution_etextno)

            self.assertIsInstance(mobydick, unicode)
            self.assertIsInstance(constitution, unicode)
            self.assertIn(u'Moby Dick; or The Whale', mobydick)
            self.assertIn(u"The United States' Constitution", constitution)

        def test_format_download_uri(self):
            self.assertEquals(
                _format_download_uri(Test.mobydick_etextno),
                r'http://www.gutenberg.lib.md.us/2/7/0/2701/2701.txt',
                'bad download-uri for newstyle e-text')
            self.assertEquals(
                _format_download_uri(Test.constitution_etextno),
                r'http://www.gutenberg.lib.md.us/etext90/const11.txt',
                'bad download-uri for oldstyle e-text')

    unittest.main()
