from factual import Factual

FACTUAL_KEY = "koqW7kcnT4qXVi6ruJC25LSVZhhpEwnxTJnDT0Kn"
FACTUAL_SECRET = "JgofM3V440POwypFRGgtgkbDuOGbPbTCoTw0M4Gv"

factual = Factual(FACTUAL_KEY, FACTUAL_SECRET)

def matchRestaurant(restaurant_name, city="", state=""):

    address = city + " " + state
    s = factual.table("restaurants").search(restaurant_name + " " + address).data()
    if not s:
      s = factual.table("restaurants").search(restaurant_name + " " + state).data()

    return s

def matchCoordinates(address):
    query = factual.table("world-geographies").search(address).limit(1)
    query = query.select("longitude,latitude")
    s = query.data()
    if len(s):
      return (s[0][unicode('latitude')], s[0][unicode('longitude')])
    return (42.350933, -71.069209)
