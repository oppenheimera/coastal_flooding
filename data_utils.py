import requests
import json
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as mdates
import calendar

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

def make_API_request(APIrequeststring):
    p, t_p = [], []
    response = requests.get(APIrequeststring)

    if response.status_code == 200:
        dataset = response.json()
    print("Finished a dataset")
    stn_name = dataset['metadata']['name']
    stn_lat = dataset['metadata']['lat']
    stn_lon = dataset['metadata']['lon']
    stn_ID = dataset['metadata']['id']
    for i in np.arange(len(dataset['data'])):
            yri = int(dataset['data'][i]['t'][0:4])
            moi = int(dataset['data'][i]['t'][5:7])
            dai = int(dataset['data'][i]['t'][8:10])
            hri = int(dataset['data'][i]['t'][11:13])
            mii = int(dataset['data'][i]['t'][14:16])
            if len(dataset['data'][i]['v']) > 0:
                p.append(float(dataset['data'][i]['v']))
            else:
                    p.append(np.nan)
            t_p.append(dt.datetime(yri, moi, dai, hri, mii, 0))
    return p, t_p

def make_yearly_API_requests(stationID, yearstart, yearend, product):
    p, t_p = [], []
    for i in np.arange(yearstart,yearend + 1): 
        APIrequeststring = "https://tidesandcurrents.noaa.gov/api/datagetter?begin_date="+str(i)+"0101 00:00&end_date="+str(i)+"1231 23:59&station="+stationID+"&product="+product+"&datum=NAVD&units=metric&time_zone=gmt&application=UC_Berkeley&format=json"
        data1,data2 = make_API_request(APIrequeststring)
        p += data1
        t_p += data2
    return np.array(p), np.array(t_p)

def make_monthly_API_requests(stationID, yearstart, yearend, product):
    p, t_p = [], []
    for i in np.arange(yearstart,yearend + 1):
        for month in months:
            try:
                month_end = calendar.monthrange(int(i), int(month))[1]
                APIrequeststring = "https://tidesandcurrents.noaa.gov/api/datagetter?begin_date="+str(i)+month+"01 00:00&end_date="+str(i)+month+str(month_end)+" 23:59&station="+stationID+"&product="+product+"&datum=NAVD&units=metric&time_zone=gmt&application=UC_Berkeley&format=json"
                data1,data2 = make_API_request(APIrequeststring)
                p += data1
                t_p += data2
            except Exception as e:
                print("Errored on date {}".format(str(i) + month))
    return np.array(p), np.array(t_p)

def API_requests_tester(stationID, year, nummonths, product):
    p, t_p = [], []
    for month in months[:nummonths]:
        try:
            month_end = calendar.monthrange(int(year), int(month))[1]
            APIrequeststring = "https://tidesandcurrents.noaa.gov/api/datagetter?begin_date="+str(year)+month+"01 00:00&end_date="+str(year)+month+str(month_end)+" 23:59&station="+stationID+"&product="+product+"&datum=NAVD&units=metric&time_zone=gmt&application=UC_Berkeley&format=json"
            data1,data2 = make_API_request(APIrequeststring)
            p += data1
            t_p += data2
        except Exception as e:
            print(e)
            print("Errored on date {}".format(str(year) + month))
    return np.array(p), np.array(t_p)


def interp_over_pressure_waterlevel(p, t_p, h, t_h):
    p_ind_baddata = np.where(np.isnan(p))[0]
    p_clean = np.delete(p, p_ind_baddata)
    tp_clean = np.delete(t_p, p_ind_baddata)

    timestamp_p_clean = []
    timestamp_h = []
    for t in tp_clean:
        timestamp_p_clean.append(calendar.timegm(t.timetuple()))
    for t in t_h:
        timestamp_h.append(calendar.timegm(t.timetuple()))
    p_interpolated_onto_h = np.interp(timestamp_h, timestamp_p_clean, p_clean)
    timestamp_p_clean = np.array(timestamp_p_clean)
    timestamp_h = np.array(timestamp_h)

    return t_h, timestamp_h-min(timestamp_h), p_interpolated_onto_h, h
