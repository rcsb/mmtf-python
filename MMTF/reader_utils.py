import gzip
import msgpack
import time
import urllib2
from StringIO import StringIO

from mmtf import Utils, MMTFDecoder

def get_data_from_url(pdb_id):
    """" Get the msgpack unpacked data given a PDB id.
    :param the input PDB id
    :return the unpacked data (a dict) """
    url = Utils.BASE_URL + pdb_id
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    out_data = msgpack.unpackb(data)
    return out_data

def get_decoded_data_from_url(pdb_id):
    """Return a decoded API to the data from a PDB id
    :param the input PDB id
    :return an API to decoded data """
    timeOne = time.time()
    decoder = MMTFDecoder()
    decoder.decode_data(get_data_from_url(pdb_id))
    print time.time()-timeOne
    return decoder