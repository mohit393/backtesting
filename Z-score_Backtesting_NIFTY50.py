# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 14:38:44 2023

@author: agraw
"""
import pandas as pd

df=pd.read_csv(r"C:\Users\agraw\OneDrive\Desktop\program\data\nifty1hr.csv")

df.drop(["open","high","low"],axis=1,inplace=True)

df["mean"]=df["close"].rolling(21).mean()
df["std"]=df["close"].rolling(21).std()
df["z-score"]=(df["close"]-df["mean"])/df["std"]
df.dropna(inplace=  True)

trade=0
entry_price=0
exit_price=0
pnl=pd.DataFrame(columns=["entry","exit","profit"])

for i in df.index:
    if trade==0 and (df["z-score"][i]<-2 and df["z-score"][i]>-4):
        trade=1
        entry_price=df["close"][i]
    if trade==1 and (df["z-score"][i]>0 or df["z-score"][i]<-4):
        trade=0
        exit_price=df["close"][i]
        pnl.loc[len(pnl.index)]=[entry_price,exit_price,exit_price-entry_price]
fin=pnl.profit.sum()
pnl.to_excel("final_pnl_of_Z-score.xlsx")