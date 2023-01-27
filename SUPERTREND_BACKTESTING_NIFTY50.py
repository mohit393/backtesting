# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 10:21:28 2023

@author: agraw
"""

import pandas as pd
import pandas_ta as ta

data=pd.read_csv(r"C:\Users\agraw\OneDrive\Desktop\program\data\nifty1hr.csv")

data.set_index(pd.to_datetime(data.datetime),inplace=True)
agg={
     "open":"first",
     "close":"last",
     "high":"max",
     "low":"min"}
df=data.resample('D').agg(agg)

df.dropna(inplace=True)

st103=ta.supertrend(df["high"], df["low"], df["close"],length=10,multiplier=3)

st92=ta.supertrend(df["high"], df["low"], df["close"],length=9,multiplier=2)

st81=ta.supertrend(df["high"], df["low"], df["close"],length=8,multiplier=1)
df=pd.concat([df,st103["SUPERTd_10_3.0"],st92["SUPERTd_9_2.0"],st81["SUPERTd_8_1.0"]],axis=1,join="inner")
status=0
buy=0
sell=0
pnl=pd.DataFrame(columns=['trade','entry','exit','profit'])

for i in df.index:
    if status==0 and df["SUPERTd_10_3.0"][i]==1 and df["SUPERTd_9_2.0"][i]==1 and df["SUPERTd_8_1.0"][i]==1:
        status=1
        buy=df['close'][i]
    if status==1 and (df["SUPERTd_10_3.0"][i]==-1 or df["SUPERTd_9_2.0"][i]==-1 or df["SUPERTd_8_1.0"][i]==-1):
        status=0
        sell=df['close'][i]
    if status==0 and buy>0:
        pnl.loc[len(pnl.index)]=[1,buy,sell,(sell-buy)]
        buy=0
    if status==0 and df["SUPERTd_10_3.0"][i]==-1 and df["SUPERTd_9_2.0"][i]==-1 and df["SUPERTd_8_1.0"][i]==-1:
        status=-1
        sell=df['close'][i]
    if status==-1 and (df["SUPERTd_10_3.0"][i]==1 or df["SUPERTd_9_2.0"][i]==1 or df["SUPERTd_8_1.0"][i]==1):
        status=0
        buy=df["close"][i]
    if status==0 and buy>0:
        pnl.loc[len(pnl.index)]=[-1,buy,sell,(sell-buy)]
        buy=0
        
final=pnl.profit.sum()
pnl.to_excel("final_pnl_of_supertrend.xlsx")