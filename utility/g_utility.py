import urllib2
import simplejson

from recommendation_item.models import Restaurant, Address
# The request also includes the userip parameter which provides the end
# user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.

def gImageSearch(restaurant):

  query = (restaurant.title + " " + 
          restaurant.address.city + " " +
          restaurant.address.state)
  query = query.replace(" ","%20")

  url = ("https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + query + 
         "&key=AIzaSyABwfAPXtUlwllUy7jx1WA4sbKPbDkd9ZE&sensor=false")
  
  

  request = urllib2.Request(
      url, None, {'Referer': 'Noone'})
  rawResponse = urllib2.urlopen(request)
  response = simplejson.load(rawResponse)

  if unicode('results') in response:
    if unicode('photos') in response[unicode('results')][0]:
      photo_reference = response[unicode('results')][0][unicode('photos')][0][unicode('photo_reference')]
      print photo_reference
      image_url = ("https://maps.googleapis.com/maps/api/place/photo?photoreference=" + photo_reference +
                "&sensor=false" +
                "&maxheight=1600&maxwidth=1600&key=AIzaSyABwfAPXtUlwllUy7jx1WA4sbKPbDkd9ZE")
      return image_url

  url = ("https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+query+
         "&safe=active")
  
  request = urllib2.Request(
      url, None, {'Referer': 'Noone'})
  rawResponse = urllib2.urlopen(request)
  response = simplejson.load(rawResponse)



  results = response[unicode('responseData')][unicode('results')]



 
  return results[0][unicode('url')]
