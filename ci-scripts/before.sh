#!/bin/bash
echo 'someuser:sometoken' > ${ONE_AUTH}
pip install -r requirements.txt
pip install -r test-requirements.txt
coverage erase
