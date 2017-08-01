from urllib2 import urlopen
import warnings
import os
import json
URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = 'osconfeed.json'
def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)
        remote=urlopen(URL)

        with open(JSON, 'wb') as local:
            local.write(remote.read())
    with open(JSON) as fp:
        json.load(fp)
    print 'end'