from django.conf import settings
import os

class storage:
	def local_write(self,photo_name,f):
		 with open(settings.MEDIA_ROOT+photo_name, 'wb+') as destination:
        		for chunk in f.chunks():
            			destination.write(chunk)
