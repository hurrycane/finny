import os

from jinja2 import Environment, PackageLoader

from finny.command import Command

BASE_FOLDER_TEMPLATES = [
  ".gitignore",
  "requirements.txt",
  "README.md",
  "manage.py"
]

CONFIG_INITIALIZERS_TEMPLATES = [ "app.py" ]
CONFIG_RUNNERS_TEMPLATES = [ "default.py" ]
CONFIG_TEMPLATES = [
  "boot.py",
  "development.py.sample",
  "test.py.sample",
  "production.py.sample"
]

class GenerateStructure(Command):

  def __init__(self, name, path):
    self.name = name
    self.path = path

  def _template(self, template_name, path):
    pass

  def _copy_templates(self, source, src, dst):
    env = Environment(loader=PackageLoader('finny.commands', 'templates/' + src))
    for item in source:
      template = env.get_template("%s.jinja" % item)
      output = template.render(name=self.name)

      path = dst + "/" + item
      dirname = os.path.dirname(path)

      if not os.path.exists(dirname):
        os.makedirs(dirname)

      with open(path, "w+") as f:
        f.write(output)

  def run(self):
    os.makedirs(self.path, 0755)

    self.env = Environment(loader=PackageLoader('finny.commands', 'templates'))

    self._copy_templates(BASE_FOLDER_TEMPLATES, "", self.path)

    self._copy_templates(CONFIG_INITIALIZERS_TEMPLATES, "initializers",
                         "%s/%s/initializers" % (self.path, self.name) )

    self._copy_templates(CONFIG_RUNNERS_TEMPLATES, "runners",
                         "%s/%s/runners" % (self.path, self.name) )

    self._copy_templates(CONFIG_TEMPLATES, "config",
                         "%s/%s/" % (self.path, self.name) )
