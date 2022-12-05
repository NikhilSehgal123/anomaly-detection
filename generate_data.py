import pandas as pd
import numpy as np

# Create some sample data for the Azure anomaly detector API
# The data should be a heart rate signal with a few anomalies in it
# The data should have two columns: timestamps and value
# The date column should follow the same format as the following '2018-03-01T00:00:00Z'

# Create a list of dates in ISO 8601 format
dates = pd.date_range(start='2022-03-01', end='2022-03-15', freq='H').strftime('%Y-%m-%dT%H:%M:%SZ').tolist()

# Create a list of heart rates
heart_rates = np.random.normal(70, 5, len(dates))
df = pd.DataFrame({'timestamp': dates, 'value': heart_rates})
anomalies = np.random.normal(100, 10, 5)
df.iloc[5:10, 1] = anomalies
df.iloc[-1, 1] = 100
df.to_csv('sample_data/heart_rate_data.csv', index=False, header=False)

# Create a list of respiration rates data in the same format as the heart rate data
respiration_rates = np.random.normal(15, 2, len(dates))
df = pd.DataFrame({'timestamp': dates, 'value': respiration_rates})
anomalies = np.random.normal(20, 5, 5)
df.iloc[5:10, 1] = anomalies
df.to_csv('sample_data/respiration_rate_data.csv', index=False, header=False)

# Create a list of blood pressure data in the same format as the heart rate data
blood_pressures = np.random.normal(120, 4, len(dates))
df = pd.DataFrame({'timestamp': dates, 'value': blood_pressures})
anomalies = np.random.normal(150, 20, 5)
df.iloc[5:10, 1] = anomalies
df.iloc[-1, 1] = 200
df.to_csv('sample_data/blood_pressure_data.csv', index=False, header=False)


