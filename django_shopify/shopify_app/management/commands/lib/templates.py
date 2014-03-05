import os.path

__dir__ = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(__dir__, os.pardir, "templates")


def render_template(template_name, context=None):
    """
        Renders a template located on the /management/commands/templates
        directory.
    """

    if context is None:
        context = {}

    if not template_name.endswith(".tm"):
        template_name = "{0}.tm".format(template_name)

    with open(os.path.join(templates_dir, template_name), "r") as f:
        content = f.read()

    return content.format(**context)