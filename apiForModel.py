from tensorflow import keras
import tensorflow
import numpy as np
import tensorflow as tf


# date / dep_time / from / to / clas / time_taken / stop -> str
response = ["22-04", "19:00", "Kolkata", "Delhi", "economy", "10h 50m", "0"]
# result = price -> int

From = ['Hyderabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai', 'Bangalore']
To = ['Hyderabad', 'Kolkata', 'Mumbai', 'Delhi', 'Chennai', 'Bangalore']
Mean = [283.919857, 781.114409, 2.330489, 2.385270, 0.311351, 732.907093, 0.923924, 3.942571]
Std = [45.747274, 321.879003, 1.767264, 1.769400, 0.463047, 431.536740, 0.397781, 1.929122]

response[0] = int(response[0][3:5] + response[0][:2])
response[1] = int(response[1][:2]) * 60 + int(response[1][3:])
response[2] = From.index(response[2])
response[3] = To.index(response[3])
response[4] = 0 if response[4] == "economy" else 1
response[5] = int(response[5][:2]) * 60 + int(response[5][4:6])
response[6] = int(response[6])
flagOfClas = 1 if response[4] else 0
for i in range(7):
    response[i] = (response[i] - Mean[i]) / Std[i]
airline = ['GO FIRST', 'StarAir', 'Indigo', 'Vistara', 'AirAsia', 'Trujet', 'Air India', 'SpiceJet']
result = []
# 0         1          2    3     4      5           6      7
# date / dep_time / from / to / clas / time_taken / stop / airplane
# date / airplane / dep_time / from / time_taken / stop/ to / class
for plane in range(len(airline)):
    if flagOfClas and (plane == 3 or plane == 6):
        NormPlane = (plane - Mean[7]) / Std[7]
        rightData = [i for i in response + [NormPlane]]
        rightData = [rightData[0], rightData[7], rightData[1], rightData[2], rightData[5], rightData[6], rightData[3], rightData[4]]
        test = np.array([rightData])
        model = keras.models.load_model('modelForAvia.h5')
        y_pred = model.predict(test)
        y_pred = [i for i in y_pred]
        print(y_pred[0][0])
        if y_pred[0][0]> 20_000:
            result += [[airline[plane], y_pred[0][0]]]
    elif not(flagOfClas):
        NormPlane = (plane - Mean[7]) / Std[7]
        rightData = [i for i in response + [NormPlane]]
        rightData = [rightData[0], rightData[7], rightData[1], rightData[2], rightData[5], rightData[6], rightData[3], rightData[4]]
        test = np.array([rightData])
        model = keras.models.load_model('modelForAvia.h5')
        y_pred = model.predict(test)
        y_pred = [i for i in y_pred]
        print(y_pred[0][0])
        if 1200 < y_pred[0][0] < 25_000:
            result += [[airline[plane], y_pred[0][0] ]]

print(result)

