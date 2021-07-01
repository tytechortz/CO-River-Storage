import time
import requests
import csv 
from datetime import datetime, date, timedelta
import pandas as pd

today = time.strftime("%Y-%m-%d")


powell_data = 'https://data.usbr.gov/rise/api/result/download?type=csv&itemId=509&before=' + today + '&after=2000-01-01&filename=Lake%20Powell%20Glen%20Canyon%20Dam%20and%20Powerplant%20Daily%20Lake%2FReservoir%20Storage-af%20Time%20Series%20Data%20'
# print(powell_data)

with requests.Session() as s:

    powell_download = s.get(powell_data)
    
    powell_decoded_content = powell_download.content.decode('utf-8')

    crp = csv.reader(powell_decoded_content.splitlines(), delimiter=',')
    
    
    for i in range(9): next(crp)
    df_powell_water = pd.DataFrame(crp)
    
    df_powell_water = df_powell_water.drop(df_powell_water.columns[[1,3,4,5]], axis=1)
    df_powell_water.columns = ["Site", "Value", "Date"]

    df_powell_water = df_powell_water[1:]
    
    df_powell_water['power level'] = 6124000

    df_powell_water = df_powell_water.set_index("Date")
    df_powell_water = df_powell_water.sort_index()
    
powell_df = df_powell_water.drop(df_powell_water.index[0])
