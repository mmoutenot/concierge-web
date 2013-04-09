from factual import Factual

FACTUAL_KEY = "frBfryFdtbYqmlgHrMB7LeSYWCOefyS0fhkIQTpp"
FACTUAL_SECRET = "Qh25xjtI1XzsJ2CT7TohBArnSQKt3P3v8uyHZKpC"

factual = Factual(FACTUAL_KEY, FACTUAL_SECRET)

def matchRestaurant(restaurant_name, address = None):
    
    if address:
        s = factual.table("restaurants").search(restaurant_name + " " + address).data()
    else:
        s = factual.table("restaurants").search(restaurant_name).data()


    return s
