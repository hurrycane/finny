from functools import wraps
import json

from flask import Response, request
from sqlalchemy.ext.declarative import DeclarativeMeta

from finny.exceptions import HttpNotFound

class AlchemyEncoder(json.JSONEncoder):

  def _encode_declarative_meta(self, obj):
    # an SQLAlchemy class
    fields = {}
    for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
      data = obj.__getattribute__(field)

      if field in [ "query", "query_class" ]:
        continue

      try:
        json.dumps(data) # this will fail on non-encodable values, like other classes
        fields[field] = data
      except TypeError:
        fields[field] = None
    # a json-encodable dict
    return fields

  def default(self, obj):
    if isinstance(obj.__class__, DeclarativeMeta):
      return self._encode_declarative_meta(obj)

    return json.JSONEncoder.default(self, obj)

def serialize(func):
  @wraps(func)
  def endpoint_method(*args, **kwargs):
    response = func(*args, **kwargs)

    return Response(json.dumps(response, cls=AlchemyEncoder),  mimetype='application/json')

  return endpoint_method

import inspect
from functools import partial

class ResourceBuilder(object):

  DAG = {}

  @classmethod
  def register(cls, klass):
    parent_klass = None
    if hasattr(klass, "__parent__"):
      parent_klass = klass.__parent__

    cls.DAG[klass] = parent_klass

  def __init__(self):
    pass

  def _get_parent_klasses(self, klass):
    def _get_parent(klass):
      if self.DAG[klass] == None:
        return []
      else:
        parent = self.DAG[klass]
        return [ parent ] + _get_parent(parent)

    return _get_parent(klass)

  def _resource_name(self, klass):

    if hasattr(klass, "route_base"):
      resource_name = klass.route_base
    else:
      resource_name = klass.__name__.lower()
      pos = resource_name.find("view")

      if pos == -1:
        raise AttributeError("Resource %s doesn't end in View" % resource_name)

      resource_name = resource_name[:pos]

    return resource_name

  def _make_show_url(self, klass):
    resource_name = self._resource_name(klass)
    return "/%s/<%s_id>" % (resource_name, resource_name)

  def _add_route(self, klass, url, method_name, http_verbs):
    methods = dict(inspect.getmembers(klass, predicate=inspect.ismethod))

    def call_method(method_name):
      instance = klass()
      method = getattr(instance, method_name)
      return method

    if hasattr(klass, method_name) and method_name in methods:
      self.app.add_url_rule(url,
                            "%s::%s" % (klass.__name__, method_name),
                            call_method(method_name),
                            methods=http_verbs)
      setattr(klass, method_name, call_method(method_name))

  def _add_nested_route(self, app, klass, parent_klasses):
    """
    resource_name

    make_show_url(klass, name)
    """

    base_url = [ self._make_show_url(parent) for parent in reversed(parent_klasses) ]
    base_url = "".join(base_url)

    resource_name = self._resource_name(klass)
    resource_base = "%s/%s" % (base_url, resource_name)

    self._add_restful_routes(app, klass, resource_name, resource_base)

  def _add_restful_routes(self, app, klass, resource_name, resource_base):
    self.app = app

    self._add_route(klass, resource_base, "index", ["GET"])
    self._add_route(klass, resource_base, "create", ["POST"])
    self._add_route(klass, resource_base + "/<%s_id>" % resource_name, "show", ["GET"])
    self._add_route(klass, resource_base + "/<%s_id>" % resource_name, "update", ["PUT"])
    self._add_route(klass, resource_base + "/<%s_id>" % resource_name, "delete", ["DELETE"])

  def _add_normal_route(self, app, klass):
    methods = dict(inspect.getmembers(klass, predicate=inspect.ismethod))

    resource_name = self._resource_name(klass)
    resource_base = "/" + resource_name

    self._add_restful_routes(app, klass, resource_name, resource_base)

  def build(self, app):
    for klass, klass_parent in self.DAG.iteritems():
      if klass_parent:
        parent_klasses = self._get_parent_klasses(klass)
        self._add_nested_route(app, klass, parent_klasses)
      else:
        self._add_normal_route(app, klass)

class Resource(object):

  @classmethod
  def register(cls):
    ResourceBuilder.register(cls)

class ModelResource(Resource):
  pass
