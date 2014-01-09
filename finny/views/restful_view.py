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

class BaseView(object):
  decorators = [serialize]

  @classmethod
  def register(cls, app, route_prefix=None):
    decorator = app.route("/")

    methods = dict(inspect.getmembers(cls, predicate=inspect.ismethod))

    def call_method(method_name):
      instance = cls()
      method = getattr(instance, method_name)
      return method

    resource_name = cls.__name__.lower()
    pos = resource_name.find("view")
    resource_name = resource_name[:pos]

    if hasattr(cls, "route_base"):
      resource_name = cls.route_base

    if hasattr(cls, "index") and "index" in methods:
      decorator = app.route("/" + resource_name ,methods=['GET'])
      setattr(cls, "index", decorator(call_method("index")))

    if hasattr(cls, "create") and "create" in methods:
      decorator = app.route("/" + resource_name ,methods=['POST'])
      setattr(cls, "create", decorator(call_method("create")))

class RESTView(BaseView):

  def __intercept__(self, *args, **kwargs):
    pass

class RestfulView(RESTView):
  pass

class NestedRestfulView(RESTView):
  pass

#  def index(self):
#    pass
#
#  def get(self, entity_id):
#    if(hasattr(self, "show")):
#      return self.show(entity_id)
#    else:
#      raise NotImplemented("No method found with the name show")
#
#  def post(self):
#    if(hasattr(self, "create")):
#      return self.create()
#    else:
#      raise NotImplemented("No method found with the name create")
#
#  def put(self, entity_id):
#    if(hasattr(self, "update")):
#      return self.update(entity_id)
#    else:
#      raise NotImplemented("No method found with the name update")
#
#  def patch(self):
#    if(hasattr(self, "update")):
#      return self.update(entity_id)
#    else:
#      raise NotImplemented("No method found with the name update")
#
#class RestfulView(RESTView):
#  model = None
#  __exclude__ = []
#  db = None
#
#  def create(self):
#    data = request.data
#
#    if data == None or len(data) == 0:
#      data = "{}"
#
#    data = json.loads(data)
#    item = self.model(**data)
#
#    #if not item.valid:
#    #  raise HttpBadRequest(item.errors)
#
#    self.db.session.add(item)
#    self.db.session.commit()
#
#    return item
#
#  def index(self):
#    items = self.model.query.all()
#    return items
#
#  def show(self, entity_id):
#    item = self.model.query.get(entity_id)
#
#    if item:
#      return item
#    else:
#      raise HttpNotFound({'error': 'Item not found in database'})
#
#  def update(self, entity_id):
#    data = json.loads(request.data)
#    item = self.model.query.get(entity_id)
#
#    if not item:
#      raise HttpNotFound({'error': 'Item not found in database'})
#
#    for field in data:
#      if hasattr(item, field):
#        setattr(item, field, data[field])
#
#    #if not item.valid:
#    #  raise HttpBadRequest(item.errors)
#
#    self.db.session.add(item)
#    self.db.session.commit()
#
#    return item
#
#  def delete(self, entity_id):
#    item = self.model.query.get(entity_id)
#
#    if item:
#      self.db.session.delete(item)
#      self.db.session.commit()
#      return {'success': 'Item was deleted!'}
#    else:
#      raise HttpNotFound({'error': 'Item not found in database'})
#
#
#class NestedRestfulView(RestfulView):
#  pass
