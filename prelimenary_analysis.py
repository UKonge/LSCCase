# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:12:00 2020

@author: Utkarsh
"""

import pandas as pd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

xl_fileZones = pd.read_excel(r'data\DistributorZones.xls',sheet_name=None)
xl_filesSales = pd.read_excel(r'data\SalesData.xls',sheet_name=None)

xl_filesSales.keys()

SalesData = xl_filesSales[list(xl_filesSales.keys())[0]]
zipwiseSales = SalesData.groupby(by='Destination Zip Code').sum()

dist_zones = xl_fileZones['Distributor Zones']
pool_zones = xl_fileZones['Table 1']

zip2latlong = pd.read_csv(r'data\us-zip-code-latitude-and-longitude.csv',sep=';')

zip2latlong['geopoint'] = zip2latlong['geopoint'].apply(lambda x: tuple(map(float,x.split(','))))
zip2latlong.set_index('Zip',inplace=True)


dist_zones['geopoint'] = ""
for i in dist_zones.index:
    j = dist_zones.loc[i]['Destination Zip Code']
    dist_zones['geopoint'][i] = zip2latlong.loc[int(j)]['geopoint']

zips = list(zip2latlong.index)

Pool = list(pool_zones['Zip Code'].unique())
Pool.append(15238)
Dest = list(SalesData['Destination Zip Code'].unique())

f = dist_zones.loc[0]['geopoint']
t = dist_zones.loc[1]['geopoint']

print(1.2*geodesic(f,t).miles)
print(f)
print(t)

cfactor = 1.21
miles = {}
for i in Pool:
    for j in Dest:
        pi = zip2latlong.loc[i]['geopoint']
        pj = zip2latlong.loc[j]['geopoint']
        d = cfactor * geodesic(pi,pj).miles
        miles[i,j] = d




'''
ind = range(1, 43*8+1)
write = pd.DataFrame(index=ind,columns=['Pool','Dest','d'])
for i in ind:
    write.loc[i]['Pool'] = Pool[int((i-1)/43)]
    write.loc[i]['Dest'] = Dest[(i-1)%43]

write.to_csv('data\DistData.csv')
'''
