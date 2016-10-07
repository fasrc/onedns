import os
import StringIO
import xml.etree.ElementTree as ET

from vcr import VCR


def scrub_auth(request):
    xml = StringIO.StringIO(request.body)
    tree = ET.parse(xml)
    root = tree.getroot()
    auth_param = root.findall('./params/param/value/string')[0]
    auth_param.text = 'someuser:sometoken'
    scrubbed = StringIO.StringIO()
    tree.write(scrubbed)
    scrubbed.seek(0)
    request.body = scrubbed.read()
    return request


vcr = VCR(
    serializer='yaml',
    cassette_library_dir=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'fixtures/oneclient'
    ),
    record_mode='once',
    decode_compressed_response=True,
    path_transformer=VCR.ensure_suffix('.yaml'),
    before_record=scrub_auth,
)
