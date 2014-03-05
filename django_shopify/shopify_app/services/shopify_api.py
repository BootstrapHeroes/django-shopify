import requests
import simplejson as json

from log_service import LogService


class APIWrapper(object):

    def __init__(self, shop, log=False):

        self.shop = shop
        self.api_domain = "https://%s/admin" % self.shop.myshopify_domain
        self.log = log

        self.params = {
            "headers": {
                'X-Shopify-Access-Token': shop.token,
                'Content-type': 'application/json',
            }
        }

    def _decode_response(self, response):

        try:
            return json.loads(response.text)
        except:
            return

    def _make_request(self, url, method, params):

        response = getattr(requests, method)(url, **params)

        if self.log:
            LogService().log_shopify_request(url, method=method, params=params, response=response.text)

        return response

    def create(self, entity, data):

        params = self.params.copy()
        params["data"] = json.dumps(data)

        url = "%s/%s.json" % (self.api_domain, entity)
        response = self._make_request(url, "post", params)

        return self._decode_response(response)

    def search(self, entity, filters):

        url = "%s/%s/search.json?query=%s" % (self.api_domain, entity, filters)
        response = self._make_request(url, "get", self.params)

        decoded_response = self._decode_response(response)
        if decoded_response is not None:
            return decoded_response[entity]

    def find(self, entity, filters):

        url = "%s/%s.json?%s" % (self.api_domain, entity, filters)
        response = self._make_request(url, "get", self.params)

        response = self._decode_response(response)
        if entity in response:
            return response[entity]
        else:
            return response

    def get(self, entity, filters):

        entities = self.find(entity, filters)

        if isinstance(entities, list) and entities:
            return entities[0]

    def activate_charge(self, entity, charge_id):

        url = "%s/%s/%s/activate.json" % (self.api_domain, entity, charge_id)
        response = self._make_request(url, "post", self.params)

        return self._decode_response(response)
