"""Module to deal with metadata acquisition."""


import gzip
import os
import re
import shutil
import tarfile
import tempfile
import urllib2

from rdflib import Graph

from gutenberg.util.os import makedirs
from gutenberg.util.os import remove
from gutenberg.util.persistence import local_path


def _download_metadata_archive():
    """Makes a remote call to the Project Gutenberg servers and downloads the
    entire Project Gutenberg meta-data catalog. The catalog describes the texts
    on Project Gutenberg in RDF. The function returns a file-pointer to the
    catalog.

    """
    data_url = r'http://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
    metadata_archive = tempfile.NamedTemporaryFile()
    shutil.copyfileobj(urllib2.urlopen(data_url), metadata_archive)
    return metadata_archive


def _iter_metadata_graphs(metadata_archive_path):
    """Yields all meta-data of Project Gutenberg texts contained in the catalog
    dump.

    """
    with tarfile.open(metadata_archive_path) as metadata_archive:
        for item in metadata_archive:
            if re.match(r'^.*pg(?P<etextno>\d+).rdf$', item.name):
                yield Graph().parse(metadata_archive.extractfile(item))


def load_metadata(refresh_cache=False):
    """Returns a graph representing meta-data for all Project Gutenberg texts.
    Pertinent information about texts or about how texts relate to each other
    (e.g. shared authors, shared subjects) can be extracted using standard RDF
    processing techniques (e.g. SPARQL queries). After making an initial remote
    call to Project Gutenberg's servers, the meta-data is persisted locally.

    """
    metadata_graph = Graph()
    cached = local_path(os.path.join('metadata', 'metadata.rdf.xml.gz'))
    if refresh_cache:
        remove(cached)
    if not os.path.exists(cached):
        makedirs(os.path.dirname(cached))
        with _download_metadata_archive() as metadata_archive:
            for graph in _iter_metadata_graphs(metadata_archive.name):
                metadata_graph += graph
        with gzip.open(cached, 'wb') as metadata_file:
            metadata_file.write(metadata_graph.serialize(format='xml'))
    else:
        with gzip.open(cached, 'rb') as metadata_file:
            metadata_graph.parse(file=metadata_file, format='xml')
    return metadata_graph
