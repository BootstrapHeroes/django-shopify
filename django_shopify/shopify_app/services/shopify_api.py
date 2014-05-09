from urllib import urlencode

import requests
import simplejson as json

from log_service import LogService

from django.conf import settings


class APIWrapper(object):

    def __init__(self, shop=None, token=None, api_domain=None, shop_url=None, log=True):

        if shop is not None:
            token = shop.token
            api_domain = shop.myshopify_domain

        if shop_url is not None:
            shop_url = self._normalize_shop_url(shop_url)

        if not api_domain:
            self.api_domain = "%s/admin" % (shop_url, )
        else:
            self.api_domain = "https://%s/admin" % api_domain

        self.log = log
        self.shop_url = shop_url

        self.params = {
            "headers": {
                'X-Shopify-Access-Token': token,
                'Content-type': 'application/json',
            }
        }

    def _decode_response(self, response):

        try:
            response_json = json.loads(response.text)
        except:
            return

        if "errors" in response_json:
            raise Exception(response_json["errors"])

        return response_json

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


    def update(self, id, entity, data):

        params = self.params.copy()
        params["data"] = json.dumps({entity: data})

        pluralized_entity = self._pluralize_entity(entity)

        url = "%s/%s/%s.json" % (self.api_domain, pluralized_entity, id)
        response = self._make_request(url, "put", params)

        return self._return_entity(response, entity)

    def search(self, entity, filters):

        if isinstance(filters, dict):
            filters = urlencode(filters)

        entity = self._pluralize_entity(entity)

        url = "%s/%s/search.json?query=%s" % (self.api_domain, entity, filters)
        response = self._make_request(url, "get", self.params)

        return self._return_entity(response, entity)

    def find(self, entity, filters):

        if isinstance(filters, dict):
            filters = urlencode(filters)

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

    def _normalize_shop_url(self, shop_url):

        if not shop_url.startswith("http://") and not shop_url.startswith("https://"):
            shop_url = "https://%s" % shop_url

        return shop_url

    def permanent_token(self, code):

        url = "%s/oauth/access_token" % (self.api_domain, )

        params = self.params.copy()
        params["params"] = {
            "code": code,
            "client_id": settings.SHOPIFY_API_KEY,
            "client_secret": settings.SHOPIFY_API_SECRET,
        }

        response = self._make_request(url, "post", params)
        decoded_response = self._decode_response(response)

        return decoded_response["access_token"]

    def permissions_url(self):

        params = {
            "scope": ",".join(settings.SHOPIFY_API_SCOPE),
            "client_id": settings.SHOPIFY_API_KEY,
        }

        return "%s/oauth/authorize?%s" % (self.api_domain, urlencode(params))

    def current_shop(self):

        url = "%s/shop.json" % (self.api_domain, )
        response = self._make_request(url, "get", self.params)

        return self._return_entity(response, "shop")
