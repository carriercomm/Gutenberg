# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0212


import gzip
import os
import tempfile


NEWSTYLE_ETEXTNO = 2701
OLDSTYLE_ETEXTNO = 5
UNICODE_ETEXTNO = 14287


class MockMetadataMixin(object):
    def setUp(self):
        import gutenberg.acquire.metadata
        self.mock_metadata_cache = _mock_metadata_cache()
        gutenberg.acquire.metadata._METADATA_CACHE = self.mock_metadata_cache

    def tearDown(self):
        os.remove(self.mock_metadata_cache)


def _mock_metadata_cache():
    with tempfile.NamedTemporaryFile(delete=False) as metadata_file:
        with gzip.GzipFile(fileobj=metadata_file, mode='wb') as gzip_file:
            gzip_file.write('\n'.join([
                r'<http://www.gutenberg.org/ebooks/{newstyle_etextno}> '
                r'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
                r'<http://www.gutenberg.org/2009/pgterms/ebook> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/{newstyle_etextno}> '
                r'<http://purl.org/dc/terms/creator> '
                r'<http://www.gutenberg.org/2009/agents/9> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/{newstyle_etextno}> '
                r'<http://purl.org/dc/terms/title> '
                r'"Moby Dick; Or, The Whale" '

                r'.',
                r'<http://www.gutenberg.org/ebooks/{oldstyle_etextno}> '
                r'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
                r'<http://www.gutenberg.org/2009/pgterms/ebook> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/{oldstyle_etextno}> '
                r'<http://purl.org/dc/terms/creator> '
                r'<http://www.gutenberg.org/2009/agents/1> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/{oldstyle_etextno}> '
                r'<http://purl.org/dc/terms/title> '
                r'"The United States Constitution" '
                r'.',

                r'<http://www.gutenberg.org/ebooks/{unicode_etextno}> '
                r'<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> '
                r'<http://www.gutenberg.org/2009/pgterms/ebook> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/{unicode_etextno}> '
                r'<http://purl.org/dc/terms/creator> '
                r'<http://www.gutenberg.org/2009/agents/60> '
                r'.',
                r'<http://www.gutenberg.org/ebooks/{unicode_etextno}> '
                r'<http://purl.org/dc/terms/title> '
                r'"L\'\u00EEle myst\u00E9rieuse" '
                r'.',
            ]).format(
                newstyle_etextno=NEWSTYLE_ETEXTNO,
                oldstyle_etextno=OLDSTYLE_ETEXTNO,
                unicode_etextno=UNICODE_ETEXTNO,
            ))

    return metadata_file.name
