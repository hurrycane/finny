import os

STAGES = [ "development", "test", "production" ]

def load_runner(app, runner):
  # loads the runner that has a list of endpoints
  pass

def load_environment_config(app, env):
  if env not in STAGES:
    raise AttributeError("Stage %s must be in %s" % (env, STAGES))

  config = os.path.join(app.root_path, '%s.py' % env)
  app.config.from_pyfile(config)
