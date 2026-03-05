from entsoe import EntsoePandasClient
import pandas as pd

# Initialize the Entsoe client
# Remplacez 'VOTRE_CLE_API' par votre véritable jeton d'accès ENTSO-E
client = EntsoePandasClient(api_key='1b5256a4-4558-41ff-a92b-c1541c16f687')

# Define the parameters for the query
country_code = 'BE' # Belgium
start_date = pd.Timestamp('20260218', tz='Etc/Universal') # first argument: the date YYYYMMDD
end_date = pd.Timestamp('20260219', tz='Etc/Universal') # second argument: the time zone

# Fetch the data
data = client.query_load(country_code, start=start_date, end=end_date)
print(data)
