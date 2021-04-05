import csv
AREA_CENTROID = {}
CITY_CENTROID = {}
def fetch_area_centroid():
    global AREA_CENTROID
    with open("./assets/jma_area_centroid.csv", "r", encoding="utf-8") as f1:
        fieldnames = ("codename", "name", "latitude", "longitude")
        reader = csv.DictReader(f1, fieldnames)
        for row in reader:
            AREA_CENTROID[row["codename"]] = (row["latitude"], row["longitude"])
        f1.close()
    return AREA_CENTROID
def fetch_city_centroid():
    global CITY_CENTROID
    with open("./assets/jma_city_centroid.csv", "r", encoding="utf-8") as f1:
        fieldnames = ("codename", "name", "latitude", "longitude")
        reader = csv.DictReader(f1, fieldnames)
        for row in reader:
            CITY_CENTROID[row["codename"]] = (row["latitude"], row["longitude"])
        f1.close()
    return CITY_CENTROID