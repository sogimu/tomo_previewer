import os

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader( os.path.join('app', 'templates') ))

from utils import Utils
env.globals['create_link_for_preview'] = Utils.create_link_for_preview

def load_template(template_name):
    """
    load template
    """
    template_path = os.path.join(template_name)
    template = env.get_template(template_path)
    return template

def render_template(template_name, context):
    """
    open template and render using context
    """
    template = load_template(template_name)
    return template.render(context)