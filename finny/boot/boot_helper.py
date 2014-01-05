import os
from importlib import import_module

import inflect

from flask import url_for

STAGES = [ "development", "test", "production" ]

def load_runner(name, app, runner):
  pluralize = inflect.engine()
  # loads the runner that has a list of endpoints
  module = import_module("%s.runners.%s" % (name, runner))

  for endpoint in module.ENDPOINTS:
    endpoint_plural = pluralize.plural(endpoint)

    module = import_module("resources.%s.api" % endpoint)
    klass = getattr(module, "%sView" % endpoint_plural.capitalize())
    # TODO: Think at something better that this hardcoded prefix
    klass.register(app, route_prefix='/v1.0/')

  # TODO: Remove this HACK!
  @app.errorhandler(404)
  def page_not_found(e):
    import urllib
    output = ""
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        line = "<strong>%s</strong> %s %s" % (rule.endpoint, methods, urllib.unquote(url))
        output += "<li>" + line + "</li>"

    return """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>

<h3>Current routes:</h3>
<ul>
%s
</ul>
    """ % output, 404

def load_environment_config(app, env):
  if env not in STAGES:
    raise AttributeError("Stage %s must be in %s" % (env, STAGES))

  config = os.path.join(app.root_path, '%s.py' % env)
  app.config.from_pyfile(config)
