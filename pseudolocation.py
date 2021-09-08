import pandas
import random
import shapefile
import re
import shapely.geometry

country_running_total = {}
runningSum = 0
df = pandas.read_csv('TotalPopulationByCountry - Data.csv')
for index, row in df.iterrows():
  if(row['ISO 3166-1 numeric code'] < 900):
    country_running_total[row['Location'].strip()] = [runningSum, runningSum + int(row['2021'].replace(" ", ""))]
    runningSum += int(row['2021'].replace(" ", ""))

def random_point_in_country(country_name):
    shapes = shapefile.Reader('World_Countries.shp') # reading shapefile with pyshp library
    country = [s for s in shapes.records() if country_name in s][0] # getting feature(s) that match the country name 
    country_id = int(re.findall(r'\d+', str(country))[0]) # getting feature(s)'s id of that match

    shapeRecs = shapes.shapeRecords()
    feature = shapeRecs[country_id].shape.__geo_interface__

    shp_geom =  shapely.geometry.shape(feature)

    minx, miny, maxx, maxy = shp_geom.bounds
    while True:
        p = shapely.geometry.Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if shp_geom.contains(p):
            return p.y, p.x

for i in range(10):
  rand = random.randrange(runningSum)
  for key, value in country_running_total.items():
    if rand > value[0] and rand <= value[1]:
      print(key)
      print(random_point_in_country(key))