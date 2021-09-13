import pandas as pd
import csv
import math

import datetime
import pytz
from timezonefinder import TimezoneFinder

user_df = pd.read_csv('clinician_data.csv')


def calculateDistance(patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude):
    earth_radius = 3958.8  # radius of the earth in miles
    radian_patient_latitude = patient_latitude * math.pi / 180  # in radians
    radian_caregiver_latitude = caregiver_latitude * math.pi / 180
    angle_latitude = (caregiver_latitude - patient_latitude) * math.pi / 180
    angle_longitude = (caregiver_longitude - patient_longitude) * math.pi / 180

    a = math.sin(angle_latitude / 2) * math.sin(angle_latitude / 2) + \
        math.cos(radian_patient_latitude) * math.cos(radian_caregiver_latitude) * \
        math.sin(angle_longitude / 2) * math.sin(angle_longitude / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c  # in miles
    return distance

def calculateTimezoneOffset(patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude):
    tf = TimezoneFinder()
    patient_timezone_str = tf.timezone_at(
        lng=patient_longitude, lat=patient_latitude)
    caregiver_timezone_str = tf.timezone_at(
        lng=caregiver_longitude, lat=caregiver_latitude)

    patient_timezone = pytz.timezone(patient_timezone_str)
    caregiver_timezone = pytz.timezone(caregiver_timezone_str)
    dt = datetime.datetime.now()
    patient_offset = patient_timezone.utcoffset(dt)
    caregiver_offset = caregiver_timezone.utcoffset(dt)
    offset = 0
    if(patient_offset > caregiver_offset):
        offset = patient_offset - caregiver_offset
    else:
        offset = caregiver_offset - patient_offset
    offset = offset.total_seconds() / 3600
    return offset


for i in range(0, 2):
    file_name_string = 'caregiver_distances' + str(i) + '.csv'
    caregiver_distances = open(file_name_string, 'w')
    with caregiver_distances:
        fnames = ['patient_lon', 'patient_lat',
                  'caregiver_lon', 'caregiver_lat', 'distance', 'offset', 'rank']
        # sets fields of CSV and ensure each line ends with new line
        caregiver_writer = csv.DictWriter(
            caregiver_distances, fieldnames=fnames, lineterminator='\n')
        caregiver_writer.writeheader()
        patient_longitude = user_df['longitude'][i]
        patient_latitude = user_df['latitude'][i]
        for j in range(2, len(user_df)):
            caregiver_longitude = user_df['longitude'][j]
            caregiver_latitude = user_df['latitude'][j]
            availability = user_df['availability'][j]
            distance = calculateDistance(
                patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude)
            timezoneDifference = calculateTimezoneOffset(
                patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude)
            rank = distance * math.sqrt(availability) * (timezoneDifference + 1)
            user_data = {
                'patient_lon': patient_longitude,
                'patient_lat': patient_latitude,
                'caregiver_lon': caregiver_longitude,
                'caregiver_lat': caregiver_latitude,
                'distance': distance,
                'offset': timezoneDifference,
                'rank': rank,
            }
            caregiver_writer.writerow(user_data)
caregiver_distances.close()
