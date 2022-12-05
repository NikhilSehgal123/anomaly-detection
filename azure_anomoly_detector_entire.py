from azure.ai.anomalydetector import AnomalyDetectorClient
from azure.ai.anomalydetector.models import DetectRequest, TimeSeriesPoint, TimeGranularity
from azure.core.credentials import AzureKeyCredential
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import dotenv

####################################################################################################
##### This is an exmaple of how to use the Azure Univariate Anomaly Detector API ###################
####################################################################################################

# Load environment variables
dotenv.load_dotenv()

# Set environment variables
API_KEY = os.getenv("ANOMALY_DETECTOR_API_KEY")
ENDPOINT = os.getenv("ANOMALY_DETECTOR_ENDPOINT")
DATA_PATH = 'sample_data/respiration_rate_data.csv'

client = AnomalyDetectorClient(AzureKeyCredential(API_KEY), ENDPOINT)

series = []
data_file = pd.read_csv(DATA_PATH, header=None, encoding='utf-8', date_parser=[0])
for index, row in data_file.iterrows():
    series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))

request = DetectRequest(series=series, granularity=TimeGranularity.HOURLY)

change_point_response = client.detect_change_point(request) # This is a point in the time series where the trend changes direction
anomaly_response = client.detect_entire_series(request) # This is a point in the time series where the value is anomalous

anomolies_x = []
anomolies_y = []
change_points_x = []
change_points_y = []

for i in range(len(data_file.values)):
    if (change_point_response.is_change_point[i]):
        change_points_x.append(data_file.values[i][0])
        change_points_y.append(data_file.values[i][1])
        print("Change point detected at index: " + str(i))
    elif (anomaly_response.is_anomaly[i]):
        anomolies_x.append(data_file.values[i][0])
        anomolies_y.append(data_file.values[i][1])
        print("Anomaly detected at index:      " + str(i))

# Zip the timestamps and values into a single array
anomolies = list(zip(anomolies_x, anomolies_y))
change_points = list(zip(change_points_x, change_points_y))

# Plot the data
fig, ax = plt.subplots()
ax.plot(data_file.values[:, 0], data_file.values[:, 1], label='Physiological Data')

# Plot the anomalies using a scatter plot with a red circle
if (len(anomolies) > 0):
    ax.scatter(*zip(*anomolies), color='red', marker='o', label='Anomaly')

# Plot the change points using a scatter plot with a green circle
if len(change_points) > 0:
    ax.scatter(*zip(*change_points), color='green', marker='o', label='Change Point')

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
fig.autofmt_xdate()
plt.legend()
plt.show()
