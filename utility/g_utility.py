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

  url = ("https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q="+query)
  
  request = urllib2.Request(
      url, None, {'Referer': 'Noone'})
  rawResponse = urllib2.urlopen(request)
  
  # Process the JSON string.
  response = simplejson.load(rawResponse)
  results = response[unicode('responseData')][unicode('results')]
 
  return results[0][unicode('url')]
