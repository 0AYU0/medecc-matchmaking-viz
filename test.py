
import datetime
import pytz
from timezonefinder import TimezoneFinder

def calculateTimezoneOffset(patient_latitude, patient_longitude, caregiver_latitude, caregiver_longitude):
    tf = TimezoneFinder()
    patient_timezone_str = tf.timezone_at(lng=patient_longitude, lat=patient_latitude)
    caregiver_timezone_str = tf.timezone_at(lng=caregiver_longitude, lat=caregiver_latitude)

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

print(calculateTimezoneOffset(45.2461607143057, 11.876255373891928, 40.958357872077656, -72.19747275736566))
for i in range(0, 2):
    file_name_string = 'caregiver_distances' + str(i) + '.csv'
    print(file_name_string)