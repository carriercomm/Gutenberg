# pylint: disable=C0103
# pylint: disable=C0111
# pylint: disable=W0212


import gzip
import os
import tempfile


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
