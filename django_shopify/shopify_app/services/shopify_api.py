import requests
import simplejson as json


class APIWrapper(object):

    def __init__(self, shop):

        self.shop = shop
        self.api_domain = "https://%s/admin" % self.shop.myshopify_domain

        self.params = {
            "headers": {
                'X-Shopify-Access-Token': shop.token,
                'Content-type': 'application/json',
            }
        }

    def create(self, entity, data):

        self.params["data"] = json.dumps(data)
        url = "%s/%s.json" % (self.api_domain, entity)
        response = requests.post(url, **self.params)

        return json.loads(response.text)

    def search(self, entity, filters):

        url = "%s/%s/search.json?query=%s" % (self.api_domain, entity, filters)
        response = requests.get(url, **self.params)

        return json.loads(response.text)[entity]

    def find(self, entity, filters):

        url = "%s/%s.json?%s" % (self.api_domain, entity, filters)
        response = requests.get(url, **self.params)

        response = json.loads(response.text)
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

        response = requests.post(url, **self.params)
        return json.loads(response.text)
