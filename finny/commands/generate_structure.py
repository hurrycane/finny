import os

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
  "development.py.sample"
  "test.py.sample",
  "production.py.sample"
]

TEMPLATES_PATH = ""

class GenerateStructure(Command):

  def __init__(self, name, path):
    self.name = name
    self.path = path

  def _template(self, template_name, path):
    pass

  def _copy_template(self, source, src, dst):
    pass

  def run(self):
    os.mkdir(self.path, 0755)

    self._copy_templates(BASE_FOLDER_TEMPLATES, TEMPLATES_PATH, self.path)

    self._copy_templates(CONFIG_INITIALIZERS_TEMPLATES,
                         TEMPLATES_PATH + "initializers",
                         "%s/%s/initializers" % (self.path, self.name) )

    self._copy_templates(CONFIG_RUNNERS_TEMPLATES,
                         TEMPLATES_PATH + "runners",
                         "%s/%s/runners" % (self.path, self.name) )

    self._copy_templates(CONFIG_TEMPLATES,
                         TEMPLATES_PATH + "config",
                         "%s/%s/" % (self.path, self.name) )
