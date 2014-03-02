from mongoengine import *
from django.conf import settings

connect(getattr(settings,"_MONGODB_NAME",None))

class Entrada(Document):
   title = StringField(max_length = 64)
      
   meta = {'collection':'test_entrada'}
