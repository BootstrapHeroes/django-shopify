from base import BaseService
from shopify_app.models import Config

from plan_config_service import PlanConfigService


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

                self.config = self.new(id=1)

                if self.config.plan_config is None:

                    plan_config = PlanConfigService().new()
                    plan_config.save()

                    self.config.plan_config = plan_config

                self.config.save()

        return self.config

    def is_active_billing(self):
        """
            Returns if the billing is enabled or not
        """

        config = self.get_config()
        return config is not None and config.enable_billing