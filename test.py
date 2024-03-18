import pandas as pd
import pickle

with open("instance.pickle", "rb") as file:
    data = pickle.load(file)
data.deserializeDictionaries('compressed_data.json.gz')
database = pd.read_csv("test_database_v36.csv")
print(data.genre_probability)
data.checkPerformance(database)
