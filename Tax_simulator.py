# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 14:08:16 2021

@author: Satiksha
"""


import pandas as pd
import streamlit as st
import plotly.express as px


    
def new_tax_calculator(n):
    if n<=700000:
        return 0
    elif n<=1500000:
        return ((((n//300000)-1)*(n//300000)*0.5)*0.05*300000)+(n%300000)*(n//300000)*0.05
    else:
        return 150000+(n-1500000)*0.3

def old_tax_calculator(n):
    if n<=500000:
        return 0
    elif n<=1000000:
        return 12500+(n-500000)*0.2
    else:
        return 12500+100000+(n-1000000)*0.3
        


form = st.form(key='my_form')
in_hand_ctc=form.number_input('Enter your total in hand for the year',min_value=0,step=1)
deductions_80c=form.number_input('Enter total 80C declaration',min_value=0,step=1)
deductions_hra=form.number_input('Enter total HRA declaration',min_value=0,step=1)
deductions_80d=form.number_input('Enter total 80D declaration',min_value=0,step=1)
deductions_loan=form.number_input('Enter total Loan declarations',min_value=0,step=1)
deductions_other=form.number_input('Enter other declarations',min_value=0,step=1)
sal_range=form.slider("Select range for Salary graph",min_value=700000,max_value=20000000)

submit = form.form_submit_button('Submit')


total_declaration=(deductions_80c+deductions_hra+deductions_80d+deductions_loan+deductions_other)
old_taxable=in_hand_ctc-50000-total_declaration
new_taxable=in_hand_ctc-50000

dict=pd.DataFrame(columns=['In_Hand','New_tax','Old_tax'])
if submit:
    x=0
    old_tax=old_tax_calculator(old_taxable)
    new_tax=new_tax_calculator(new_taxable)
    st.write("As per New Regime",new_tax)
    st.write("As per Old Regime",old_tax)
    for p in range(700000,sal_range,100000):
        x+=1
        #recession_amt=sip_func(sip,i,r)
        n=new_tax_calculator(p-50000)
        o=old_tax_calculator(p-50000-total_declaration)
        #gain=appreciation_amt-recession_amt
        #gain_factor=gain/recession_amt
        dict.loc[x]=(p,n,o)
        
    plt=px.line(dict,x='In_Hand',y=['New_tax','Old_tax'])
    st.plotly_chart(plt)
