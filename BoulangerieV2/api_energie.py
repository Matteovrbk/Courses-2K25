from entsoe import EntsoePandasClient
import pandas as pd
def getprice():
    TOKEN = "1b5256a4-4558-41ff-a92b-c1541c16f687"
    client = EntsoePandasClient(api_key=TOKEN)

    start = pd.Timestamp("now", tz="Europe/Brussels").normalize()
    end = start + pd.Timedelta(days=1)
    prices = client.query_day_ahead_prices("BE", start=start, end=end)
    return prices

