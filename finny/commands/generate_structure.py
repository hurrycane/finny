import os

from finny.command import Command

class GenerateStructure(Command):

  def __init__(self, name, path):
    self.name = name
    self.path = path

  def run(self):
    os.mkdir(self.path, 0755)

    """
    You need to create:

    .gitignore
    requirements.txt
    README.md

    manage.py

    {{ app_name }}:
      initializers:
        app.py

      boot.py

      runners:
        default.py

      development.py
      test.py
      production.py

    monitors:
      api.py
      models.py
      tests:
        fixtures/
        test_base.py

    utils.py

    """
