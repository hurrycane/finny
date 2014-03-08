import os

import imp
from importlib import import_module

from flask.ext.testing import TestCase

class ResourceTest(TestCase):

  def setUp(self):
    self.db.create_all()

  def tearDown(self):
    self.db.session.remove()
    self.db.drop_all()

  def create_app(self):
    current_path = os.getcwd()

    config = imp.new_module('config')
    config.__file__ = "config"
    # loads the configuration file
    with open(current_path + "/__init__.py") as config_file:
      exec(compile(config_file.read(), "config", 'exec'), config.__dict__)

    finny_app = config.__APP__

    boot_module = import_module("%s.boot" % finny_app)

    create_app = boot_module.create_app
    self.db = boot_module.db

    return create_app("andromeda_api", "development", "default")
