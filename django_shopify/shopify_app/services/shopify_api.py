import requests
import simplejson as json

from log_service import LogService

from django.conf import settings


class APIWrapper(object):

    def __init__(self, shop=None, token=None, api_domain=None, log=True):

        if shop is not None:
            token = shop.token
            api_domain = shop.myshopify_domain

        self.api_domain = "https://%s/admin" % api_domain
        self.log = log

        self.params = {
            "headers": {
                'X-Shopify-Access-Token': token,
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

        if self.log and getattr(settings, "LOG_SHOPIFY_API_REQUESTS", False):
            LogService().log_shopify_request(url, method=method, params=params, response=response.text)

        return response

    def _pluralize_entity(self, entity):

        if not entity.endswith("s"):
            return "%ss" % entity
        return entity

    def _return_entity(self, response, entity):

        decoded_response = self._decode_response(response)

        if decoded_response is not None:
            return decoded_response.get(entity)

    def create(self, entity, data):

        params = self.params.copy()
        params["data"] = json.dumps({entity: data})

        pluralized_entity = self._pluralize_entity(entity)

        url = "%s/%s.json" % (self.api_domain, pluralized_entity)
        response = self._make_request(url, "post", params)

        return self._return_entity(response, entity)

    def search(self, entity, filters):

        entity = self._pluralize_entity(entity)

        url = "%s/%s/search.json?query=%s" % (self.api_domain, entity, filters)
        response = self._make_request(url, "get", self.params)

        return self._return_entity(response, entity)

    def find(self, entity, filters):

        entity = self._pluralize_entity(entity)

        url = "%s/%s.json?%s" % (self.api_domain, entity, filters)
        response = self._make_request(url, "get", self.params)

        response = self._decode_response(response)
        if entity in response:
            return response[entity]
        else:
            return response

    def get(self, entity, id):

        if isinstance(id, dict):
            id = id.get("id")

        pluralized_entity = self._pluralize_entity(entity)

        url = "%s/%s/%s.json" % (self.api_domain, pluralized_entity, id)
        response = self._make_request(url, "get", self.params)

        return self._return_entity(response, entity)

    def activate_charge(self, entity, charge_id):

        entity = self._pluralize_entity(entity)

        url = "%s/%s/%s/activate.json" % (self.api_domain, entity, charge_id)
        response = self._make_request(url, "post", self.params)

        return self._decode_response(response)

    def current_shop(self):

        url = "%s/shop.json" % (self.api_domain, )
        response = self._make_request(url, "get", self.params)

        return self._return_entity(response, "shop")
