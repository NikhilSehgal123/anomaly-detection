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
DATA_PATH = 'sample_data/blood_pressure_data.csv'

client = AnomalyDetectorClient(AzureKeyCredential(API_KEY), ENDPOINT)

series = []
data_file = pd.read_csv(DATA_PATH, header=None, encoding='utf-8', date_parser=[0])
for index, row in data_file.iterrows():
    series.append(TimeSeriesPoint(timestamp=row[0], value=row[1]))

request = DetectRequest(series=series, granularity=TimeGranularity.HOURLY)

# Create another client to detect the anomaly in the last point
last_point_anomaly_response = client.detect_last_point(request)

print(last_point_anomaly_response.is_anomaly)

# Plot the data and label the anomaly as red
fig, ax = plt.subplots()
ax.plot(data_file.values[:, 0], data_file.values[:, 1], color='blue')
if last_point_anomaly_response.is_anomaly:
    ax.scatter(data_file.values[-1][0], data_file.values[-1][1], color='red')
plt.show()



