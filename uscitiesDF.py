import pandas as pd
import pickle

filename = 'uscities.csv'

cityDF = pd.read_csv(filename)
cities = ["Seattle", "Portland", "Oakland", "Los Angeles", "Helena", "Boise",
          "Salt Lake City", "Las Vegas", "Santa Fe", "Colorado Springs"]


westCoastDF = cityDF[cityDF['city'].isin(cities)]
westCoastDF = westCoastDF[['city', 'lat', 'lng']]
westCoastDF = westCoastDF.drop_duplicates(subset = 'city')
westCoastDF = westCoastDF.set_index('city')

westCoastDF.to_pickle('westCoastCities.pkl')