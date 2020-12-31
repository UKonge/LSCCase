# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 14:41:14 2020

@author: Utkarsh
"""

from pyomo.environ import *

m = ConcreteModel()

m.M = Param(initialize=50)
m.M1 = Param(initialize=1500)
m.M3 = Param(initialize=10**5)

m.x = Var(Pool,Dest,domain=Binary)
m.y = Var(Pool,domain=Binary)
m.r = Var(RangeSet(2,8),Pool,domain=NonNegativeReals)
m.d = Var(Pool,Dest,domain=NonNegativeReals)
m.g = Var(RangeSet(2,8),Pool,bounds=(0,1))

m.g_cons = ConstraintList()
for i in dist_zones.index:
    for j in dist_zones.columns:
        z = dist_zones.loc[i][j]
        m.g_cons.add(expr=m.g[z,j]>=m.x[j,i])

m.demand_satisfaction_cons = ConstraintList()
for i in Dest:
    m.demand_satisfaction_cons.add(expr=sum(m.d[j,i] for j in Pool) == zipwiseSales.loc[i]['Demand'])
    
m.zerooneDemand_cons = ConstraintList()
for i in Dest:
    for j in Pool:
        m.zerooneDemand_cons.add(expr=m.d[j,i] <= m.M1*m.x[j,i])

'''
m.poolLocations_cons = ConstraintList()
for j in Pool:
    m.poolLocations_cons.add(expr=sum(m.x[j,i] for i in Dest) <= m.M*m.y[j])
'''
   
m.poolLocations_cons = ConstraintList()
for j in Pool:
    for i in Dest:
        m.poolLocations_cons.add(expr=m.x[j,i] <= m.M*m.y[j])

m.minimumParcelCost_cons = ConstraintList()
for z in range(2,9):
    for j in Pool:
        if j != 15238:
            m.minimumParcelCost_cons.add(expr=DistRates.loc[z]['Minimum Charge']*m.y[j] <= m.r[z,j]+m.M3*(1-m.g[z,j]))
        else:
            m.minimumParcelCost_cons.add(expr=DistRates2.loc[z]['Minimum Charge']*m.y[j] <= m.r[z,j]+m.M3*(1-m.g[z,j]))

DistRates2 = DistRates.copy()
r = [0.28,0.32,0.35,0.40,0.45,0.58,0.70]
mi = [4.00,4.30,4.65,5.00,5.45,6.30,7.40]
for i in range(2,9):
    DistRates2.loc[i]['Rate per Pound'] = r[i-2]
    DistRates2.loc[i]['Minimum Charge'] = mi[i-2]
m.parcelCost_cons = ConstraintList()
for z in range(2,9):
    for j in Pool:
        if j != 15238:
            if len(zones[j,z]) > 0:
                m.parcelCost_cons.add(expr=sum(m.d[j,i] for i in zones[j,z])*DistRates.loc[z]['Rate per Pound'] <= m.r[z,j]+m.M3*(1-m.g[z,j]))              
        else:
            if len(zones[j,z]) > 0:
                m.parcelCost_cons.add(expr=sum(m.d[j,i] for i in zones[j,z])*DistRates2.loc[z]['Rate per Pound'] <= m.r[z,j]+m.M3*(1-m.g[z,j]))

m.allocation_cons = ConstraintList()
for i in Dest:
    m.allocation_cons.add(expr=sum(m.x[j,i] for j in Pool) == 1)

def obj(m):
    return 52*(sum(sum(m.r[z,j] for z in range(2,9)) for j in Pool)+sum(40000.0/52.0*m.y[j] for j in Pool[:-1])+sum(sum(m.d[j,i] for i in Dest)*PoolCost.loc[j]['Truckload Rate ($/Mile)']*miles[15238,j]+m.y[j]*PoolCost.loc[j]['Handling Cost/Shipment'] for j in Pool))
m.TotalCost = Objective(rule=obj,sense=maximize)
#m.pprint()

opt = SolverFactory('cbc.exe')
result = opt.solve(m,tee=True)
print(result.solver.status)
print(result.solver.termination_condition)

result.write()

for i in Pool:
    print("Choosing",i,"facility",m.y[i].value)
    
print('Total annual cost =',value(m.TotalCost))

allocation = pd.DataFrame(columns = Pool, index = Dest)
for i in Dest:
    for j in Pool:
        allocation.loc[i][j] = m.x[j,i].value
        
demand_flow = pd.DataFrame(columns = Pool, index = Dest)
for i in Dest:
    for j in Pool:
        demand_flow.loc[i][j] = m.d[j,i].value
        
for i in range(2,9):
    for j in Pool:
        print(i,j,m.r[i,j].value)
    print(" ")

