from MMTF.Common import Utils
import urllib2,msgpack

from StringIO import StringIO
import gzip



def get_data_from_url(pdb_id):
    url = Utils.BASE_URL+pdb_id
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    return msgpack.unpackb(data)

