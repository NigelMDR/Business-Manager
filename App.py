import numpy as np
import streamlit as st
import pandas as pd

with st.sidebar:
  revenue = st.number_input('Revenue', value=14777.24)
  operating_expenses = st.number_input('Operating Expenses', value=1088.64)
  tax = st.slider("tax",0,27, value=27)/100
  employee_pay = st.slider("Employee pay",0,100, value=74)/100
  E1 = st.number_input('Employee_1', value=1380)
  E2 = st.number_input('Employee_2', value=1595)
  E3 = st.number_input('Employee_3', value=2000)
  E4 = st.number_input('Employee_4', value=1500)
  E5 = st.number_input('Employee_5', value=800)

  employee_cost = (E1+E2+E3+E4+E5)*employee_pay
# tax = .23
# employee_pay = .70

col11, col22, col33 = st.columns(3)
col11.metric("After Company Tax", round(revenue*(1-tax),2) , str(-1*tax*100)+"%")
col22.metric("After Operating Expanses", round(revenue*(1-tax)-operating_expenses,2) , str(round(-1*operating_expenses/(revenue*(1-tax))*100,2))+"%")
col33.metric("After Employee Tax", round(revenue*(1-tax)-operating_expenses-employee_cost,2) , str(round(-1*employee_cost/(revenue*(1-tax)-operating_expenses)*100,2))+"%")

col1, col2, col3, col4, col5 = st.columns(5)
col5.metric("Employee 5", str(round(E5*employee_pay)),str(round((E1*(1-employee_pay)),2))+'S')
col3.metric("Employee 3", str(round(E3*employee_pay)),str(round((E1*(1-employee_pay)),2))+'S')
col4.metric("Employee 4", str(round(E4*employee_pay)),str(round((E1*(1-employee_pay)),2))+'S')
col1.metric("Employee 1", str(round(E1*employee_pay)),str(round((E1*(1-employee_pay)),2))+'S')
col2.metric("Employee 2", str(round(E2*employee_pay)),str(round((E1*(1-employee_pay)),2))+'S')



fx = lambda x: x*(1-tax)*(1-employee_cost/revenue)

y = [fx(val) for val in range(25000)]
min_goal = [4313 for i in range(2500)]

# st.write(min_goal)
# st.write(y)
chart_data = pd.DataFrame(
    y,
    columns=['a'])


st.line_chart(chart_data)


    