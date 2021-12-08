"""
 EEWMap - Tools - ObsIntCombiner
 Combines the observation_points.json and intensity_stations.csv together.
 NOTES:
    - Before running, make sure that following files are present in this folder:
        - Stations.txt (as csv)
"""
import csv
import json


def run():
    try:
        content_stations = []
        with open("Stations.txt", "r", encoding="utf-8") as f:
            station_reader = csv.reader(f, delimiter=';')
            for row in station_reader:
                content_stations.append({
                    "Type": row[2],
                    "Name": row[3],
                    "Region": row[4],
                    "SubRegionCode": row[5],
                    "RegionCode": row[6],
                    "IsSuspended": False,
                    "Location": {
                        "Latitude": row[8],
                        "Longitude": row[7]
                    },
                    "OldLocation": None,
                    "Point": {
                        "X": row[9],
                        "Y": row[10]
                    },
                    "ClassificationId": None,
                    "PrefectureClassificationId": None
                })
            f.close()
    except:
        print("Failed to open station.txt. Check file existence.")
        return
    print(content_stations)
    with open("observation_points.json", "w+", encoding="utf-8") as f:
        f.write(json.dumps(content_stations))
        f.close()
if __name__ == "__main__":
    run()
