from base import BaseService
from shopify_app.models import Config


class ConfigService(BaseService):

    entity = Config

    def get_config(self):
        """
            Gets the config object.
            Created a new default config if it doesn't exists.
        """ 

        #lazy attribute
        if not "config" in self.__dict__:

            self.config = self.get_one(id=1)

            if self.config is None:

                self.config = self.new()
                self.config.save()

        return self.config