from mongoengine.queryset import QuerySetManager

class EventManager(QuerySetManager):
   def search_events(self,title,category,lat,lng,distance):
	return self(Q(title__icontains=title) & Q(category=category) & Q(location__geo_within_sphere=[(float(lat),float(lng)),float(distance)/6371])).order_by('-added_date')[:20]

   
