from django.template.loader import get_template
from django.template import Context, Template


def render(template, context):
    
    context = Context(context)
    return get_template(template).render(context)


def render_string(string, context):

    template = Template(string)
    context = Context(context)
    return template.render(context)