import pandas
import random
import shapefile
import re
import csv
import shapely.geometry
import numpy

country_running_total = {}
runningSum = 0

# create pandas dataframe from csv file
df = pandas.read_csv('TotalPopulationByCountry - Data.csv')
for index, row in df.iterrows():
  # filter numeric codes for countries
  if(row['ISO 3166-1 numeric code'] < 900): 
    # represent population as ranges of corresponding to each country
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

    # returns list of all records within the file
    shapeRecs = shapes.shapeRecords()
    # select the given geometry for our country
    feature = shapeRecs[country_id].shape.__geo_interface__

    # returns Shapely geometry from GeoJSON object
    shp_geom = shapely.geometry.shape(feature)
    # generate random point in bounds of rectangle of country shapefile object
    minx, miny, maxx, maxy = shp_geom.bounds
    while True:
        p = shapely.geometry.Point(random.uniform(
            minx, maxx), random.uniform(miny, maxy))
        if shp_geom.contains(p):
            return p.x, p.y


f = open('clinician_data.csv', 'w')

with f:
  fnames = ['index', 'country', 'longitude', 'latitude', 'availability']
  # sets fields of CSV and ensure each line ends with new line
  caregiver_writer = csv.DictWriter(f, fieldnames=fnames, lineterminator='\n')
  caregiver_writer.writeheader()

  for i in range(100):
    rand = random.randrange(runningSum)
    for key, value in country_running_total.items():
      # if random value in population range specified  
      if rand > value[0] and rand <= value[1]: 
        # grab location within country for the user
        location = random_point_in_country(key)
        # normal distribution for availability to represent load balancing
        rand_availability = numpy.random.normal(0.5, 0.2)
        # proportion of caregivers and patients to depict
        #caregiver_or_patient = 'Caregiver' if random.random() > 0.7 else 'Patient'
        if location != -1 and rand_availability > 0:
          # define and write simulated data in a dictionary
          user_data = {
            'index': i, 
            'country': key, 
            'longitude': location[0], 
            'latitude': location[1], 
            'availability': rand_availability, 
            #'user_type': caregiver_or_patient,
            }
        caregiver_writer.writerow(user_data)
f.close()
