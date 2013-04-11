# Create your views here.
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from recommendation_item.models import Restaurant, Address
from utility import match
import json

def pickgotos(request, template = "gotos.html"):

    raw_gotos = [] 
    for count in range(5):
        raw_gotos.append(["", ""])

    return render_to_response(template, locals(), context_instance=RequestContext(request))

def savegotos(request):
    if request.user.is_authenticated():
      user_profile = request.user.get_profile()
      rawgotos = request.POST.getlist(unicode('rawgotos'),'')
      fgotos = [match.matchRestaurant(r) for r in rawgotos]
      gotos = []
      
      for f in fgotos:
        if f:
          datum = f[0]
          
          sources = "{'factual':["+datum.get('factual_id', 0)+"]}"
          
          a, a_created = Address.objects.get_or_create(street_address=datum.get('address',""),
                                                           city=datum.get('locality',""),
                                                          state=datum.get('region',""),
                                                        zipcode=datum.get('postcode',""),
                                                      longitude=datum.get('longitude',-1),
                                                       latitude=datum.get('latitude',-1))

          r, r_created = Restaurant.objects.get_or_create( title=datum.get('name',None),
                                                       cuisines=datum.get('cuisine',None),
                                                         rating=datum.get('rating', -1),
                                                          price=datum.get('price', -1),
                                                        address=a,
                                                   data_sources=sources)
         
          
          if not r_created and (not r in user_profile.gotos.all()):
            gotos.append(r)

      [user_profile.gotos.add(i) for i in gotos]
      user_profile.save()

    return render_to_response(template, locals(), context_instance=RequestContext(request))
