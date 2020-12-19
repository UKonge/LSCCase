# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:41:14 2020

@author: Utkarsh
"""

from pyomo.environ import *

m = ConcreteModel()

m.M = Param(initialize=50)
m.M1 = Param(initialize=1500)

m.x = Var(Pool,Dest,domain=Binary)
m.y = Var(Pool,domain=Binary)
m.r = Var(RangeSet(2,8),Pool,domain=NonNegativeReals)
m.d = Var(Pool,Dest,domain=NonNegativeReals)

m.demand_satisfaction_cons = ConstraintList()
for i in Dest:
    m.demand_satisfaction_cons.add(expr=sum(m.d[j,i] for j in Pool) == zipwiseSales.loc[i]['Demand'])
    
m.zerooneDemand_cons = ConstraintList()
for i in Dest:
    for j in Pool:
        m.zerooneDemand_cons.add(expr=m.d[j,i] <= m.M1*m.x[j,i])
        
m.poolLocations_cons = ConstraintList()
for j in Pool:
    m.poolLocations_cons.add(expr=sum(m.x[j,i] for i in Dest) <= m.M*m.y[j])

m.minimumParcelCost_cons = ConstraintList()
for z in range(2,9):
    for j in Pool:
        m.minimumParcelCost_cons.add(expr=DistRates.loc[z]['Minimum Charge']*m.y[j] <= m.r[z,j])
        
m.parcelCost_cons = ConstraintList()
for z in range(2,9):
    for j in Pool:
        if len(zones[j,z]) > 0:
            m.parcelCost_cons.add(expr=sum(m.d[j,i] for i in zones[j,z])*DistRates.loc[z]['Rate per Pound'] <= m.r[z,j])              
            

m.TotalCost = m.Objective(expr= sum(m.r[z,j] for z in range(2,9) for j in Pool)+
                                sum(40000/52*m.y[j] for j in Pool)+
                                sum(sum(m.d[j,i] for i in Dest)*PoolCost.loc[j]['Truckload Rate ($/Mile)']*miles[15238,j]+m.y[j]*PoolCost.loc[j]['Handling Cost/Shipment'] for j in Pool),
                                sense=minimize)
m.pprint()
