import os

from vcr import VCR

vcr = VCR(
    serializer='yaml',
    cassette_library_dir=os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'fixtures/oneclient'
    ),
    record_mode='once',
    path_transformer=VCR.ensure_suffix('.yaml'),
)
