# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:14:44 2020

@author: Utkarsh
"""

import plotly.graph_objects as go
import plotly as plotly
import plotly.express as px
import pandas as pd

df = pd.read_csv('Data2PlotOnMap.csv')
df['Zip'] = df['Zip'].astype(str)
df['text'] = df['Location']+' '+df['Zip']
df['Zip'] = df['Zip'].astype(int)


data = dict(
        type = 'scattergeo',
        locationmode = 'USA-states', 
        mode = 'markers',
        )

data1 = data.copy()
data1['lon'] = df[df['Cat']  == 'Destination']['Long']
data1['lat'] = df[df['Cat']  == 'Destination']['Lat']
data1['marker'] = dict(color = 'red',size=10,line=dict(color='Black',width=2))
data1['name'] = 'Destination'
data1['text'] = df[df['Cat']  == 'Destination']['text']

data2 = data.copy()
data2['lon'] = df[df['Cat']  == 'Pool']['Long']
data2['lat'] = df[df['Cat']  == 'Pool']['Lat']
data2['marker'] = dict(color = 'green',size=10,line=dict(color='Black',width=2))
data2['name'] = 'Pool'
data2['text'] = df[df['Cat']  == 'Pool']['text']

layout = dict(
        title = 'Locations of Pools and Destinations <br>Hover for more info.',
        geo = dict(
            scope = 'usa',
            projection = dict(type='albers usa'),
        ),
    )

fig = dict(data=[data1, data2], layout=layout)
plotly.offline.plot(fig)