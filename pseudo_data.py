import pandas
import random
import shapefile
import re
import csv
import shapely.geometry
import numpy

country_running_total = {}
runningSum = 0
df = pandas.read_csv('TotalPopulationByCountry - Data.csv')
for index, row in df.iterrows():
    if(row['ISO 3166-1 numeric code'] < 900):
        country_running_total[row['Location'].strip()] = [
            runningSum, runningSum + int(row['2021'].replace(" ", ""))]
        runningSum += int(row['2021'].replace(" ", ""))


def random_point_in_country(country_name):
    # reading shapefile with pyshp library
    shapes = shapefile.Reader('World_Countries.shp')
    # getting feature(s) that match the country name
    country = [s for s in shapes.records() if country_name in s]
    if len(country) == 0:
        return -1
    country_zero = country[0]
    # getting feature(s)'s id of that match
    country_id = int(re.findall(r'\d+', str(country_zero))[0])

    shapeRecs = shapes.shapeRecords()
    feature = shapeRecs[country_id].shape.__geo_interface__

    shp_geom = shapely.geometry.shape(feature)

    minx, miny, maxx, maxy = shp_geom.bounds
    while True:
        p = shapely.geometry.Point(random.uniform(
            minx, maxx), random.uniform(miny, maxy))
        if shp_geom.contains(p):
            return p.x, p.y


f = open('clinician_data.csv', 'w')

with f:
    fnames = ['index', 'country', 'longitude', 'latitude', 'availability']
    writer = csv.DictWriter(f, fieldnames=fnames, lineterminator='\n')
    writer.writeheader()

    for i in range(100):
        rand = random.randrange(runningSum)
        for key, value in country_running_total.items():
            if rand > value[0] and rand <= value[1]:
                print(key)
                location = random_point_in_country(key)
                rand_availability = numpy.random.normal(0.5, 0.2)
                if location != -1 and rand_availability > 0:
                    caregiver_data = {
                        'index': i, 'country': key, 'longitude': location[0], 'latitude': location[1], 'availability': rand_availability}
                    writer.writerow(caregiver_data)
f.close()
