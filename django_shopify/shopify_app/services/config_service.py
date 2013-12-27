from base import BaseService
from shopify_app.models import Config


class ConfigService(BaseService):

    entity = Config

    def __new__(cls, *args, **kwargs):
        """ 
            Singleton class
        """
        if not hasattr(cls, "_instance"):
            cls._instance = super(ConfigService, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_config(self):
        """
            Gets the config object.
            Created a new default config if it doesn't exists.
        """

        #lazy attribute
        if not hasattr(self, "config"):            

            self.config = self.get_one(id=1)

            if self.config is None:
                self.config = self.new().save()

        return self.config