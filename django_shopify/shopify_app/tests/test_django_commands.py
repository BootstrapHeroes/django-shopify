import os
from shopify_app.management.commands.start_shopify_app import Command

from django.test import TestCase
from shopify_app.services import ShopifyService

import shutil

class CommandsTest(TestCase):

    def clean(self, path):

        try:
            shutil.rmtree(path)
        except:
            pass

    def _get_dir(self, *args):

        return os.path.join(*args)

    def test_start_app(self):

        test_name = "project_testing"
        app_name = "{0}_app".format(test_name)

        self.clean(test_name)

        Command().do_run(test_name)        
        
        self.assert_exists([test_name])
        self.assert_exists([test_name, "templates"])
        self.assert_exists([test_name, "media"])
        self.assert_exists([test_name, app_name])
        self.assert_exists([test_name, "manage.py"], is_dir=False)

        self.assert_exists([test_name, test_name])
        self.assert_exists([test_name, test_name, "settings.py"], is_dir=False)
        self.assert_exists([test_name, test_name, "urls.py"], is_dir=False)
        self.assert_exists([test_name, test_name, "wsgi.py"], is_dir=False)

        self.assert_exists([test_name, app_name, "views"])
        self.assert_exists([test_name, app_name, "views", "index.py"], is_dir=False)

        self.clean(test_name)

    def assert_exists(self, dir_parts, is_dir=True):
        
        assert_func = "isdir" if is_dir else "isfile"

        self.assertTrue(getattr(os.path, assert_func)(self._get_dir(*dir_parts)))        
