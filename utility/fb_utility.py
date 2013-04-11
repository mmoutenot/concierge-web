from django.db import models
from user_profile.singly import *
from django.contrib.auth.models import User
from recommendation_item.models import Restaurant, Address, restaurantFromFactual, addressFromFactual
from utility import match
import json

def fill_profile(user_profile, singly_id, access_token):
  discovery_endpoint = '/services/facebook'
  self_endpoint = '/services/facebook/self'
  page_likes_endpoint = '/services/facebook/page_likes?limit=1000'
  request = {'auth': 'true'}
  fb_discovery = Singly(access_token=access_token).make_request(discovery_endpoint, request=request)
  fb_self = Singly(access_token=access_token).make_request(self_endpoint, request=request)
  fb_page_likes = Singly(access_token=access_token).make_request(page_likes_endpoint, request=request)

  udata = unicode("data")
  fb_profile = {}

  self_attributes = ["location", "education", "birthday", "gender",
                     "interested_in", "languages"] 

  for a in self_attributes:
      if unicode(a) in fb_self[0][udata]:
          fb_profile[a] = fb_self[0][udata][unicode(a)]

  fb_profile["friend_count"] = fb_discovery[unicode("friends")]
  fb_profile["likes"] = []
  for i in fb_page_likes:
    like = [i[udata][unicode("name")],i[udata][unicode("category")]]
    if(like[1] == "Restaurant/cafe"):
      fill_restaurant_likes(user_profile, like[0], i)
    fb_profile["likes"].append(like)

  return json.dumps(fb_profile)
    
def fill_restaurant_likes(user_profile, name, full_like):
  restaurantQuery = name

  udata = unicode("data")
  ulocation = unicode('location')

  if ulocation in full_like[udata]:
    if unicode('city') in full_like[udata][ulocation]:
      restaurantQuery += " " + full_like[udata][ulocation][unicode('city')]
    if unicode('state') in full_like[udata][ulocation]:
      restaurantQuery += " " + full_like[udata][ulocation][unicode('state')]

  frestaurant = match.matchRestaurant(restaurantQuery)
  if frestaurant:
    sources = "{'factual':["+frestaurant[0].get('factual_id', 0)+"]}"

    a, a_created = addressFromFactual(frestaurant[0])
    r, r_created = restaurantFromFactual(frestaurant[0], a, sources)
    print r
    if not r in user_profile.gotos.all():
      user_profile.gotos.add(r)
      user_profile.save()

