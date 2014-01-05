import os

from jinja2 import Environment, PackageLoader
from finny.command import Command

import inflect

class GenerateEndpoint(Command):

  def __init__(self):
    self.pluralize = inflect.engine()

  def _touch(self, filepath):
    open(filepath, 'a').close()

  def run(self, params):
    self.params = params

    cwd = os.getcwd()

    self.app_name = cwd.split("/")[-1]

    endpoint_path = cwd + "/" + params.name
    # create folder for endpoint
    os.makedirs(cwd + "/" + params.name)

    # copy templates over
    self._copy_templates([ "api.py", "model.py"], "endpoint", endpoint_path)

  def _copy_templates(self, source, src, dst):
    env = Environment(loader=PackageLoader('finny.commands', 'templates/' + src))

    for item in source:
      template = env.get_template("%s.jinja" % item)
      output = template.render(name=self.params.name,
                               plural_name=self.pluralize.plural(self.params.name),
                               app_name=self.app_name)

      path = dst + "/" + item
      dirname = os.path.dirname(path)

      if not os.path.exists(dirname):
        os.makedirs(dirname)

      self._touch(dirname + "/__init__.py")

      with open(path, "w+") as f:
        f.write(output)
