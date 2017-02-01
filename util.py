from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km


def filter_object(obj, filter_function):
    filtered_obj = {}
    for key in obj:
        row = obj[key]
        if filter_function(row):
            filtered_obj[key] = row
    return filtered_obj