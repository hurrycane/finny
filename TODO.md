1. Exclude fields per model
In each model have a:
__exclude__ = [ 'field1' ]
2. Generate API Docs
3. Include relationships:
__eager__ => [ for the serialisation decorator it loads the relationship ]
+ serializer

Classy:

GET /users/<user_id>/<entity > [ Books ] >

class UserBookView(..):
  model = Books

  def index(self, user_id):
    pass

/buy/books
/buy/lives

Lives:
  route_prefix = '/colors'

GET /users/3/books/5/pages
GET /books

eager loading child resources
GET /users/5
=> books

ENDPOINTS = [
]
