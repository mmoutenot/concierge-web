import math
from django.db import models
from django.contrib.gis.db import models as geo_models
from django.contrib.localflavor.us.models import USStateField

from django.contrib.auth.models import User


# address model from: https://docs.djangoproject.com/en/dev/ref/contrib/gis/model-api/
class Address(geo_models.Model):
  longitude = models.FloatField()
  latitude = models.FloatField()
  street_address = models.CharField(max_length=200)
  city = models.CharField(max_length=100)
  state = USStateField()
  zipcode = models.CharField(max_length=10)
  objects = geo_models.GeoManager()

# holds a set of recommendation_items and their ratings for a particular user
class RecommendationList(models.Model):
  user = models.ForeignKey(User)

# a recommendation item abstracts the item being recommended. And example of a
# recommendation item is a restaurant, an event, or a song.
#
# Important features of a recommendation item (LIVE LIST)
# - Has one or more data sources to get information from
# - Has an address that can be filtered based on proximity to a location
class RecommendationItem(models.Model):
  recommendation_list = models.ManyToManyField(RecommendationList)
  date_added = models.DateTimeField(auto_now=True)
  data_sources = models.TextField(null=True, blank=True)
  address = models.ForeignKey(Address)
  title = models.CharField(max_length=120, default="")

  # takes in a destination and returns the distance from it in miles
  def distanceFromRestaurant(self, dest):
    lat1 = self.address.latitude
    lon1 = self.address.longitude
    lat2 = dest.address.latitude
    lon2 = dest.address.longitude
    radius = 6371 # km of earth

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))\
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    # convert to miles
    d = d * 0.621371

    return d

  def distanceFromPoint(self, point):
    lat1 = self.address.latitude
    lon1 = self.address.longitude
    lat2_u, lon2_u = point
    lat2 = float(lat2_u)
    lon2 = float(lon2_u)
    radius = 6371 # km of earth

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))\
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    # convert to miles
    d = d * 0.621371

    return d

# specific recommendation item extensions
class Restaurant(RecommendationItem):
  cuisines = models.CharField(max_length=400, null=True, blank=True)
  # rating, dangerous assumption that this is always out of 5
  rating = models.FloatField(null=True, blank=True)
  # price from 1-5
  price = models.IntegerField()
  image = models.CharField(max_length=600, null=True, blank=True)

  def __unicode__(self):
    return self.title

def addressFromFactual(datum):
    a, a_created = Address.objects.get_or_create(street_address=datum.get('address',""),
                                                           city=datum.get('locality',""),
                                                          state=datum.get('region',""),
                                                        zipcode=datum.get('postcode',""),
                                                      longitude=datum.get('longitude',-1),
                                                       latitude=datum.get('latitude',-1))
    return [a, a_created]

def restaurantFromFactual(datum, a, sources):
    r, r_created = Restaurant.objects.get_or_create( title=datum.get('name',None),
                                                       cuisines=datum.get('cuisine',None),
                                                         rating=(datum.get('rating', 3) - 3) / 2,
                                                          price=datum.get('price', -1),
                                                        address=a,
                                                   data_sources=sources)
    return [r, r_created]
