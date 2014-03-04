from mongoengine import *
from django.conf import settings

#for select test database
if settings.TEST_MODE:
   connect(getattr(settings,"_MONGODB_TEST_NAME",None))
else:
   connect(getattr(settings,"_MONGODB_NAME",None))

class Entrada(Document):
   title = StringField(max_length = 64)
      
   meta = {'collection':'test_entrada'}
