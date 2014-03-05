import os

from django.core.management import call_command
from django.utils.crypto import get_random_string
from templates import render_template
import sys
from ansicolors import AnsiColors

class ProjectBuilder(object):
    """
        A builder for creating the directories structure and files described on:
        https://github.com/SocalProofit/django-shopify/wiki/Getting-started#basic-usage
    """

    def __init__(self, *args):
        """ 
            Setups the project_name and app_name based on *args
            *args are the parameters the user sends through the console command.

            Example:

                #in this case *args would be (project_name, )
                start_shopify_app [project_name]
        """

        self.args = args
        self.project_name = args[0] if self.args else None
        self.app_name = "{0}_app".format(self.project_name)
        self.type = args[1] if len(self.args) > 1 else False
        self.public_app = self.type == "public"

    def build(self):
        """
            Builds the project structure and create files.
        """

        print
        print AnsiColors.WHITEONBLUE + "                                                     " + AnsiColors.ENDC
        print AnsiColors.WHITEONBLUE + "  Django Shopify Core Library - by Bootstrap Heroes  " + AnsiColors.ENDC
        print AnsiColors.WHITEONBLUE + "                                                     " + AnsiColors.ENDC
        print

        if self.project_name == None:
            print AnsiColors.WARNING + "Please provide a project name." + AnsiColors.ENDC
            print "Usage: start_shopify_app [project_name]" + AnsiColors.ENDC
            print
            sys.exit()
        else:  
            self.make_project()
            self.setup_media()
            self.make_default_app()
            
            self.setup_urls()
            self.setup_settings()

            self.go_back_to_main_dir()

            print AnsiColors.OKGREEN + "Shopify Django app " + AnsiColors.WHITE + self.project_name + AnsiColors.OKGREEN + " created! :)" + AnsiColors.ENDC

        print

    def make_project(self):
        """
            Creates the django project and some templates.
        """
 
        call_command("startproject", self.project_name)
        os.chdir(self.project_name)

        self._create_dir("templates")
        self._create_dir("templates", "index")
        self._create_file(self._get_dir("templates", "index", "index.html"), render_template("index.html"))

        if self.public_app:
            self._create_dir("templates", "oauth")
            self._create_file(self._get_dir("templates", "oauth", "login.html"), render_template("login.html"))

    def make_default_app(self):
        """
            Creates the django app, the views root folder and some example views.
        """
        
        print AnsiColors.OKCYAN + "Starting Django app..." + AnsiColors.ENDC

        call_command("startapp", self.app_name)

        os.remove(self._get_app_dir("views.py"))

        self._create_dir(self.app_name, "views")
        self._create_file(self._get_app_dir("views", "__init__.py"), "")
        self._create_file(self._get_app_dir("views", "index.py"), render_template("index"))

        os.chdir(self.project_name)

    def setup_settings(self):
        """
            Replaces the django default settings.py for a template we provide.
        """

        print AnsiColors.OKCYAN + "Configuring " + AnsiColors.WHITE + "settings.py" + AnsiColors.OKCYAN + "..." + AnsiColors.ENDC

        # Create a random SECRET_KEY hash to put it in the main settings.
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)

        if self.public_app:
            template_name = "settings_public"
        else:
            template_name = "settings"

        settings_file = render_template(template_name, {"app_name": self.app_name, "project_name": self.project_name, "secret_key": secret_key })

        self._create_file("settings.py", settings_file)

    def setup_urls(self):
        """
            Replaces the django default urls.py for a template we provide.
        """

        print AnsiColors.OKCYAN + "Configuring " + AnsiColors.WHITE + "urls.py" + AnsiColors.OKCYAN + "..." + AnsiColors.ENDC

        if self.public_app:
            template_name = "urls_public"
        else:
            template_name = "urls"

        urls_file = render_template(template_name, {"app_name": self.app_name })
        self._create_file("urls.py", urls_file)

    def setup_media(self):
        """
            Creates the media folder
        """

        print AnsiColors.OKCYAN + "Creating media folder..." + AnsiColors.ENDC

        self._create_dir("media")
        self._create_dir("media", "js")
        self._create_dir("media", "css")
        self._create_dir("media", "img")

    def go_back_to_main_dir(self):
        """
            After creating the structure this goes back to the directory where we started
            before calling os.chdir in order to create some dirs and files inside the tree.
        """

        os.chdir(os.pardir)
        os.chdir(os.pardir)

    def _create_file(self, name, content):
        """
            Created a file with [content]
        """

        with open(name, "w") as f:
            f.write(content)

    def _get_app_dir(self, *args):
        """
            Returns the app directory
        """

        return os.path.join(self.app_name, *args)

    def _get_dir(self, *args):
        """
            Returns a directory using os.path.join
        """

        return os.path.join(*args)

    def _create_dir(self, *args):
        """
            Creates a new dir joining *args
        """

        os.mkdir(self._get_dir(*args))