# aurora.py - Nanoleaf Aurora python library
#
#   Copyright 2017 Zachary Cornelius
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import requests
import json

from pprint import pprint

class Aurora:

    def __init__(self, auth_token, address, port=16021):
        self.auth_token = auth_token
        self.address = address
        self.port = port
        self.uri_base = "http://%s:%d/api/v1/%s" % (address, port, auth_token)

    def _get_json(self, path):
        uri = "%s%s" % (self.uri_base, path)
        r = requests.get(uri)
        if r.ok:
            return r.json()
        else:
            r.raise_for_status()

    def _put_json(self, path, data):
        uri = "%s%s" % (self.uri_base, path)
        print("PUT'ing to URI %s with data %s" % (uri, json.dumps(data)))
        r = requests.put(uri, data=json.dumps(data))
        if r.ok:
            return True
        else:
            r.raise_for_status()

    def get_info(self):
        return self._get_json("")

    def get_effects(self):
        return self._get_json("/effects/effectsList")

    def get_state(self):
        return self._get_json("/state")

    def get_power(self):
        return self._get_json("/state/on")["value"]

    def get_brightness(self):
        return self._get_json("/state/brightness")["value"]

    def get_brightness_max(self):
        return self._get_json("/state/brightness")['max']

    def get_brightness_min(self):
        return self._get_json("/state/brightness")['min']

    def set_brightness(self, new_brightness):
        self._put_json("/state/brightness", {"brightness": {"value": int(new_brightness)}})
        return self.get_brightness()

    def increment_brightness(self, brightness_increment):
        self._put_json("/state/brightness", {"brightness": {"incrememnt": int(brightness_increment)}})
        return self.get_brightness()

    def get_hue(self):
        return self._get_json("/state/hue")["value"]

    def get_hue_max(self):
        return self._get_json("/state/hue")["max"]

    def get_hue_min(self):
        return self._get_json("/state/hue")["min"]

    def set_hue(self, new_hue):
        self._put_json("/state/hue", {"hue": {"value": int(new_hue)}})
        return self.get_hue()

    def increment_hue(self, hue_increment):
        self._put_json("/state/hue", {"hue": {"increment": int(hue_increment)}})
        return self.get_hue()


    def delete_auth_token(self):
        r = requests.delete(self.uri_base)
        if r.ok:
            return True
        else:
            r.raise_for_status()

    @staticmethod
    def get_auth_token(address, port=16021):
        uri = "http://%s:%d/api/v1/new" % (address, port)
        r = requests.post(uri)
        if r.ok:
            return r.json()["auth_token"]
        else:
            r.raise_for_status()
