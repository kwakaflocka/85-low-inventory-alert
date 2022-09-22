import datetime
import urllib.request, json
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime, timedelta

start_date=datetime.now()-timedelta(14)
end_date=datetime.now()
link="https://archive-api.open-meteo.com/v1/era5?latitude=39.95&longitude=-75.16&start_date=2022-06-01&end_date=2022-09-21&daily=temperature_2m_max,temperature_2m_min,apparent_temperature_max,apparent_temperature_min,precipitation_sum&timezone=America%2FNew_York&temperature_unit=fahrenheit&windspeed_unit=ms&precipitation_unit=inch"
with urllib.request.urlopen(link) as url:
    data=json.loads(url.read().decode())
    Date=data["daily"].get("time")
    MaxTempF=(data["daily"].get("temperature_2m_max"))
    MinTempF=(data["daily"].get("temperature_2m_min"))
    app_maxF=(data["daily"].get("apparent_temperature_max"))
    app_minF = (data["daily"].get("apparent_temperature_min"))
    precip_sum=(data["daily"].get("precipitation_sum"))
    results=zip(Date,MaxTempF,MinTempF,app_maxF,app_minF,precip_sum)

weatherdata={}
for day,max,min,amax,amin,precip in results:
    weather={}
    if max != None:
        day=day.replace('-', '')
        weather={"MaxTempF": max,"MinTempF":min,"app_maxF": amax,"app_minF":amin,"precip_sum":precip}
        weatherdata[f'{day}']=weather




weatherdata =pd.DataFrame.from_dict(weatherdata,orient='columns')



