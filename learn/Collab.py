import cPickle, json, math
from datetime import date

from user_profile.models import UserProfile
from reccomendation_item.models import ReccomendationItem, Restaurant

# Collab is based on the memory-based collaboration filtering
# algorithm found at http://en.wikipedia.org/wiki/Collaborative_filtering

class Collab(object):

  ########################################
  # FUNCTIONS FOR OUTSIDE USE (PUBLIC)
  ########################################

  # predicts the rating of the reccomendation item at index i
  # by the user whose index is u
  # returns actual rating if that item is already rated
  # this rating is not stored in the rating matrix
  def predict_rating(self, i, u):

    # find top n users most similar to u that have rated item i
    relevant_users = [ x for x in UserProfile.objects.all()
                                  if not x == u and self._get_rating(i,x) ]
    top_n_most_sim = sorted(relevant_users,
                            key=lambda x: abs(self._user_user_sim(u,x)),
                            reverse=True)[:self.n]

    # return a weighted average of the ratings of the item in question
    weighted_sum = 0.0
    sum_of_weights = 0.0
    for user in top_n_most_sim:
      weight = self._user_user_sim(u, user)
      sum_of_weights += weight
      weighted_sum += weight * self._get_rating(i, user)
    if isinstance(i, Restaurant):
      return (weighted_sum + i.rating) / (sum_of_weights + 1.0)
    if sum_of_weights == 0:
      return 0
    return (weighted_sum / sum_of_weights)

  # returns a sorted list of the top n items that user u has not rated
  # that the user is most likely to like
  def suggest_items(self, n, u):
    item_rating_pairs = []
    for i in ReccomendationItem.objects.all():
      if not self._get_rating(i, u):
        item_rating_pairs.append((i, self.predict_rating(i, u)))
    return zip(*sorted(item_rating_pairs,
                       key=lambda x: x[1],
                       reverse=True)[:n])[0]

  def suggest_restaurants(self, n, u):
    item_rating_pairs = []
    for i in Restaurant.objects.all():
      if not self._get_rating(i, u):
        item_rating_pairs.append((i, self.predict_rating(i, u)))
    return zip(*sorted(item_rating_pairs,
                       key=lambda x: x[1],
                       reverse=True)[:n])[0]

  # returns true if a user u has recommended reccomendation item i
  # else returns false
  def has_reccomended(self, i, u):
    if self._get_rating(i, u):
      return True
    return False

  # retuns a list of the n users most similar to the given user_id
  def suggest_users(self, u, n):
    return sorted(UserProfile.objects.all(),
                  key=lambda x: abs(self._user_user_sim(u,x)),
                  reverse=True)[:n]

  #########################################
  # FUNCTIONS NOT FOR OUTSIDE USE (PRIVATE)
  #########################################

  # user-user similarity metric
  # returns a scaler between 0 and 1 representing the similarity
  # between two given UserProfiles u1 and u2. Closer to 1 is more similar.
  def _user_user_sim(self, u1, u2):
    u1_features = self._get_feature_vector(u1)
    u2_features = self._get_feature_vector(u2)
    u1_vec = []
    u2_vec = []
    keys = set(u1_features.keys()) | set(u2_features.keys())
    for key in keys:
      u1_vec.append(u1_features[key] if key in u1_features else 0)
      u2_vec.append(u2_features[key] if key in u2_features else 0)
    prod_sum = 0.0
    u1_sq_sum = 0.0
    u2_sq_sum = 0.0
    for f1, f2 in zip(u1_vec, u2_vec):
      prod_sum += f1 * f2
      u1_sq_sum += f1 * f1
      u2_sq_sum += f2 * f2
    return prod_sum / ( math.sqrt(u1_sq_sum) * math.sqrt(u2_sq_sum) )


  # returns the rating of item i by user u. If user u has not rated item i,
  # returns None
  def _get_rating(self, i, u):
   fv = self._get_feature_vector(u)
   if i.title in fv:
     return fv[i.title]
   return None

  # returns the feature vector corresponding to that UserProfile. missing items
  # have the value None
  def _get_feature_vector(self, u):
    fb_data = json.loads(u.fb_data)
    feature_vector = {}
    if 'likes' in fb_data:
      for l in fb_data['likes']:
        feature_vector[l[0]] = 1
    return feature_vector
