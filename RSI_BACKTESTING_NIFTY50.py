# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 21:11:51 2023

@author: agraw
"""

import pandas as pd
import pandas_ta as ta

df=pd.read_csv(r"C:\Users\agraw\OneDrive\Desktop\program\data\nifty1hr.csv")

rsid=ta.rsi(df.close)

df=pd.concat([df,rsid],axis=1)
trade=0
buy=0
sell=0
candle=0
trad=[]
for i in df.index:
    
    if trade==0 and (df["RSI_14"][i]>40 and df["RSI_14"][i]<60):
        trade=1
        candle=-1   
        buy=df["close"][i]
    if trade==1:
        candle+=1
    if trade==1 and (df["RSI_14"][i]>80 or candle==10):
        trade=0
        candle=0
        sell=df["close"][i]
    if trade==0 and buy!=0:
        trad.append([buy,sell,sell-buy])
        buy=0
final=pd.DataFrame(trad,columns={'entry',"exit","pnl"})
fin=final.pnl.sum()
final.to_excel("final_pnl_of_rsi.xlsx")
