from django.conf import settings
import os
import boto

class storage:
	def local_remove(self,photo_name):
		os.remove(settings.MEDIA_ROOT+photo_name)

	def local_write(self,photo_name,f):
		 with open(settings.MEDIA_ROOT+photo_name, 'wb+') as destination:
        		for chunk in f.chunks():
            			destination.write(chunk)

	def s3_write(self,photo_name,f):
		s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACESS_KEY)
		bucket = s3.get_bucket(settings.BUCKET_NAME)
		key = bucket.new_key('media/'+photo_name)
		key.set_contents_from_file(f)
		key.set_acl('public-read')

	def s3_remove(self,photo_name):
		print photo_name
		s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACESS_KEY)
		key = s3.get_bucket(settings.BUCKET_NAME).get_key('media/'+photo_name)
		print key
		if key.exists:
			key.delete()
