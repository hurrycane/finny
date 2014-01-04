import os
import sys

from finny.commands import GenerateStructure

import cli.app

class Finny(cli.app.CommandLineApp):
  """
  Finny entry point
  """
  def __init__(self, is_structure):
    super(Finny, self).__init__()

    self.is_structure = is_structure

  def run_command(self):
    pass

  def generate_structure(self):
    path = self.params.path

    if path[0] != "/":
      path = os.path.abspath(os.getcwd() + "/" + self.params.path)

    name = path.split("/")[-1]

    if os.path.exists(path):
      raise AttributeError("Path %s is already present." % path)

    GenerateStructure(name, path).run()

  def main(self):

    if self.is_structure:
      self.run_command()
    else:
      self.generate_structure()

def detect_current_structure():
  return False

def execute_from_cli():
  current_path = os.getcwd()
  is_structure = detect_current_structure()

  f = Finny(is_structure)

  if is_structure:
    Finny.add_param("name", help="Run command in the ", choices=["new"])
  else:
    f.add_param("command", help="Generate new finny based flask structure", choices=["new"])
    f.add_param("path", help="Path or name of the finny app", default=False)

  f.run()
