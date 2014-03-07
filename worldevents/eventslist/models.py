from mongoengine import *
from django.conf import settings

connect('worldevents')

class Event(Document):
   title = StringField(max_length = 64)
   location = PointField()
   description = StringField()
   category = StringField()
   #tags = ListField()
   
   def __str__(self):
      return self.title +'-'+str(self.location['coordinates'][0])+str(self.location['coordinates'][1])+'-'+self.description +'-'+self.category

   meta = {'collection':'event'}


class Category(Document):
   name = StringField(max_length = 64, required = True, unique = True)
   
   def __str__(self):
      return self.name
   
   meta = {'collection':'category'}
