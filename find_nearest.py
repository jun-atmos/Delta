import pandas as pd
from geopy.distance import geodesic

def find_nearest(lat,lon,aws):
    distances = aws.apply(
        lambda row: geodesic((lat, lon), (row["Latitude"], row["Longitude"])).kilometers, axis=1
    )
    aws["Distance"] = distances
    aws = aws.dropna(subset=['tourism_index'])
    aws['rank'] = aws['tourism_index'].rank(method='min', ascending=False).astype(int)
    nearest_station = aws.loc[distances.idxmin()]
    return nearest_station