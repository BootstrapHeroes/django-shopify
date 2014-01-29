from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from lib.builder import ProjectBuilder

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.do_run(*args)
    
    def do_run(self, *args):
        builder = ProjectBuilder(*args)
        builder.build()