import pandas as pd
import csv
import math

user_df = pd.read_csv('clinician_data.csv')

caregiver_distances = open('caregiver_distances.csv', 'w')

def calculateDistance(patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude):
    earth_radius = 3958.8 # radius of the earth in miles
    radian_patient_latitude = patient_latitude * math.pi / 180 # in radians
    radian_caregiver_latitude = caregiver_latitude * math.pi / 180
    angle_latitude = (caregiver_latitude - patient_latitude) * math.pi / 180
    angle_longitude = (caregiver_longitude - patient_longitude) * math.pi / 180

    a = math.sin(angle_latitude / 2) * math.sin(angle_latitude / 2) + \
      math.cos(radian_patient_latitude) * math.cos(radian_caregiver_latitude) * \
      math.sin(angle_longitude / 2) * math.sin(angle_longitude / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c #in miles
    return distance

with caregiver_distances:
  fnames = ['patient_lon', 'patient_lat', 'caregiver_lon', 'caregiver_lat', 'distance']
  # sets fields of CSV and ensure each line ends with new line
  caregiver_writer = csv.DictWriter(caregiver_distances, fieldnames=fnames, lineterminator='\n')
  caregiver_writer.writeheader()

  patient_longitude = user_df['longitude'][0]
  patient_latitude = user_df['latitude'][0]
  for i in range(1, len(user_df)):
    caregiver_longitude = user_df['longitude'][i]
    caregiver_latitude = user_df['latitude'][i]
    distance = calculateDistance(patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude)
    user_data = {
      'patient_lon': patient_longitude, 
      'patient_lat': patient_latitude, 
      'caregiver_lon': caregiver_longitude, 
      'caregiver_lat': caregiver_latitude, 
      'distance': distance, 
      }
    caregiver_writer.writerow(user_data)
caregiver_distances.close()