"""Module to deal with metadata acquisition."""


import contextlib
import gzip
import os
import re
import shutil
import tarfile
import tempfile
import urllib2

from rdflib.graph import Graph

from gutenberg._domain_model.persistence import local_path
from gutenberg._domain_model.vocabulary import DCTERMS
from gutenberg._domain_model.vocabulary import PGTERMS
from gutenberg._util.os import makedirs
from gutenberg._util.os import remove


@contextlib.contextmanager
def _download_metadata_archive():
    """Makes a remote call to the Project Gutenberg servers and downloads the
    entire Project Gutenberg meta-data catalog. The catalog describes the texts
    on Project Gutenberg in RDF. The function returns a file-pointer to the
    catalog.

    """
    data_url = r'http://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2'
    with tempfile.NamedTemporaryFile(delete=False) as metadata_archive:
        shutil.copyfileobj(urllib2.urlopen(data_url), metadata_archive)
    yield metadata_archive.name
    remove(metadata_archive.name)


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
            for graph in _iter_metadata_graphs(metadata_archive):
                metadata_graph += graph
        metadata_graph.bind('pgterms', PGTERMS)
        metadata_graph.bind('dcterms', DCTERMS)
        with gzip.open(cached, 'wb') as metadata_file:
            metadata_file.write(metadata_graph.serialize(format='pretty-xml'))
    else:
        with gzip.open(cached, 'rb') as metadata_file:
            metadata_graph.parse(file=metadata_file, format='xml')
    return metadata_graph
