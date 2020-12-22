# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 17:12:00 2020

@author: Utkarsh
"""

import pandas as pd

xl_fileZones = pd.read_excel(r'data\DistributorZones.xls',sheet_name=None)
xl_filesSales = pd.read_excel(r'data\SalesData.xls',sheet_name=None)
Dest_city = list(xl_fileZones['Distributor Zones']['Destination City'])
Pool_city = list(xl_fileZones['Table 1']['Location'])
Pool_city.append('Blawnox')
xl_filesSales.keys()

SalesData = xl_filesSales[list(xl_filesSales.keys())[0]]
zipwiseSales = SalesData.groupby(by='Destination Zip Code').sum()
zipwiseSales.columns = ['Demand']

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


miles = {}
i = Pool[-1]
for j in range(len(Pool)-1):
    miles[i,Pool[j]] = float(input("Dist between "+str(i)+" & "+str(Pool[j])+"(miles):"))
miles[15238,15238] = 0.0


PoolCost = xl_fileZones['Table 1']
PoolCost.drop('Location',axis=1,inplace=True)
PoolCost.set_index('Zip Code',inplace=True)
for i in PoolCost.columns:
    PoolCost.loc[15238] = [0.0, 0.0]

DistRates = xl_fileZones['Table 3 USPE Published Rates']
DistRates.set_index('Zone',inplace=True)
DirectRates = xl_fileZones['Table 2 USPE Proposed Rates']
DirectRates.set_index('Zone',inplace=True)


dist_zones.drop(dist_zones.columns[0:3],inplace=True,axis=1)
dist_zones.set_index('Destination Zip Code',inplace=True)
dist_zones.drop('geopoint',inplace=True,axis=1)
dist_zones.columns = [15238,91789,97420,89029,83263,86045,95687,99362]

zones = {}
for i in range(2,9):
    for j in Pool:
        zones[j,i] = []

for i in dist_zones.columns:
    for j in dist_zones.index:
        z = dist_zones.loc[j][i]
        zones[i,z].append(j)

data = pd.DataFrame(columns=['Location','Zip','Lat','Long','Cat','color'])

ind = 0
for i in range(len(Dest)):
    data.loc[ind] = [Dest_city[i], Dest[i], zip2latlong.loc[Dest[i]]['Latitude'], zip2latlong.loc[Dest[i]]['Longitude'], 'Destination', 'red']
    ind = ind+1
for i in range(len(Pool)):
    data.loc[ind] = [Pool_city[i], Pool[i], zip2latlong.loc[Pool[i]]['Latitude'], zip2latlong.loc[Pool[i]]['Longitude'], 'Pool', 'green']
    ind =  ind+1

data.to_csv('Data2PlotOnMap.csv')

'''
ind = range(1, 43*8+1)
write = pd.DataFrame(index=ind,columns=['Pool','Dest','d'])
for i in ind:
    write.loc[i]['Pool'] = Pool[int((i-1)/43)]
    write.loc[i]['Dest'] = Dest[(i-1)%43]

write.to_csv('data\DistData.csv')


miles imput :
2418
2703
2160
1863
1933
2524
2380

'''
