from factual import Factual

FACTUAL_KEY = "frBfryFdtbYqmlgHrMB7LeSYWCOefyS0fhkIQTpp"
FACTUAL_SECRET = "Qh25xjtI1XzsJ2CT7TohBArnSQKt3P3v8uyHZKpC"

factual = Factual(FACTUAL_KEY, FACTUAL_SECRET)

def matchRestaurant(restaurant_name, city="", state=""):

    address = city + " " + state
    s = factual.table("restaurants").search(restaurant_name + " " + address).data()
    if not s:
      s = factual.table("restaurants").search(restaurant_name + " " + state).data()

    return s
