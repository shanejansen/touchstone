import json
import urllib.parse
import urllib.request


class WhenContext(object):
    def __init__(self, config):
        self.config = config

    def get_text(self, endpoint):
        return urllib.request.urlopen(self.config.service_url() + endpoint).read()

    def get_json(self, endpoint):
        response = urllib.request.urlopen(self.config.service_url() + endpoint).read()
        return json.loads(response)

    def post_json(self, endpoint, payload):
        data = json.dumps(payload).encode('utf8')
        request = urllib.request.Request(self.config.service_url() + endpoint, data=data,
                                         headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(request).read()
        return json.loads(response)
