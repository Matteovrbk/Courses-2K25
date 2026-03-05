from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt

# Initialize the Entsoe client
# N'oubliez pas d'utiliser votre clé API personnelle ici
client = EntsoePandasClient(api_key='1b5256a4-4558-41ff-a92b-c1541c16f687')

# Define the parameters for the query
country_code = 'BE' # Belgium
start_date = pd.Timestamp('20260218', tz='Etc/Universal') # premier argument: la date YYYYMMDD
end_date = pd.Timestamp('20260219', tz='Etc/Universal') # second argument: le fuseau horaire

# Fetch the data
data = client.query_load(country_code, start=start_date, end=end_date)

# display the data
plt.close("all")
data.plot()
plt.legend(loc='best')
plt.title('Belgian electrical consumption')
plt.show()