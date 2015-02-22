"""Module to deal with text acquisition."""


import gzip
import os

import requests

from gutenberg._util.os import makedirs
from gutenberg._util.os import remove
from gutenberg._util.persistence import local_path
from gutenberg._util.types import validate_etextno


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


def load_etext(etextno, refresh_cache=False):
    """Returns a unicode representation of the full body of a Project Gutenberg
    text. After making an initial remote call to Project Gutenberg's servers,
    the text is persisted locally.

    """
    etextno = validate_etextno(etextno)
    cached = local_path(os.path.join('text', '{}.txt.gz'.format(etextno)))

    if refresh_cache:
        remove(cached)
    if not os.path.exists(cached):
        makedirs(os.path.dirname(cached))
        download_uri = _format_download_uri(etextno)
        response = requests.get(download_uri)
        text = response.text
        with gzip.open(cached, 'w') as cache:
            cache.write(text.encode('utf-8'))
    else:
        with gzip.open(cached, 'r') as cache:
            text = cache.read().decode('utf-8')
    return text
