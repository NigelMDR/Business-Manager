
import numpy as np
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

class Business:
  def __init__(self, name, income, cost, tax, employee_tax, tot_debt, monthly_debt):
    self.name = name
    self.employee = {}
    self.id = 1
    self.income = income
    self.cost = cost
    self.tax = tax
    self.employee_tax = employee_tax
    self.tot_debt = tot_debt
    self.monthly_debt = monthly_debt
    self.tot_employee_salary = 0
    self.tot_employee_contribution = 0
    
  def add_employee(self, Name:str, Contribution: float):
    salary = round(Contribution*self.employee_tax,2)
    self.employee[Name] = {'Salary': salary, 'Tax': self.employee_tax, 'Contribution': Contribution, 'diff': round(Contribution-salary,2)}
    self.tot_employee_salary += Contribution*self.employee_tax # Employee salary
    self.tot_employee_contribution += Contribution
    self.id += 1
  
  def delete_employee(self, Name):
    del self.employee[Name.lower()]
    
  def get_employees(self):
    return self.employee
    
  def get_stats(self):
    self.stats = {}
    temp = 0
    self.stats['revenue'] = {'#': round(self.income*(1-self.tax),2),
                             '%': -1*self.tax*100}
    # It is typically used to evaluate how efficiently a company is managing labor and supplies in production
    self.stats['gross profit'] = {'#': round(self.stats['revenue']['#'] - self.cost - self.tot_employee_salary,2), 
                                  '%': round((self.stats['revenue']['#'] - self.cost - self.tot_employee_salary)/abs(self.stats['revenue']['#'])*100,2)}
    # % = gross profit_margin above
    # self.stats['gross profit_margin'] = {'%': round(self.stats['gross profit']['#']/self.stats['revenue']['#']*100,2)}
                                        
    # Net Income aka bottom line
    temp = round(self.stats['gross profit']['#'] - self.monthly_debt,2)
    self.stats['net income'] = {'#': temp, 
                                '%': round(temp/abs(self.stats['gross profit']['#'])*100,2)}
  
    # Individual parts: what % of Revenue is spent on each
    temp = round(self.stats['revenue']['#'] - self.cost, 2)
    temp2 = round(self.stats['revenue']['#'],2)
    temp_percent = round((1-temp/temp2)*100,2)
    
    self.stats['Operating Cost'] = {'#': self.cost, 
                                  '%': temp_percent if temp > 0 else -1*temp_percent}
    
    temp = round(temp2 - self.tot_employee_salary, 2)
    temp_percent = round((1-temp/temp2)*100,2)
    self.stats['Employee Cost'] = {'#': self.tot_employee_salary, 
                                  '%': temp_percent if temp > 0 else -1*temp_percent}
    
    temp = round(temp2 - self.monthly_debt,2)
    temp_percent = round((1-temp/temp2)*100,2)
    self.stats['Bank Debt'] = {'#': self.tot_debt - self.monthly_debt, 
                                '%': temp_percent if temp > 0 else -1*temp_percent}
    return self.stats
  
  def __str__(self):
    self.get_stats()
    return self.name + '/n' + str(self.employee) + str(self.stats)
    

with st.sidebar:  
  income = st.number_input('Ingreso', value=14777.24)
  cost = st.number_input('Los Gastos Operativos', value=1088.64)
  tax = st.slider("Impuesto %",0,27, value=27)/100
  employee_tax = st.slider("Pago de Empleados %",0,100, value=74)/100
  E1 = st.number_input('Empleado 1', value=1380)
  E2 = st.number_input('Empleado 2', value=1595)
  E3 = st.number_input('Empleado 3', value=2000)
  E4 = st.number_input('Empleado 4', value=1500)
  E5 = st.number_input('Empleado 5', value=800)
  tot_debt = st.number_input('Deuda Bancaria', value=82000)
  monthly_debt = st.number_input('Mensualidad', value=4313)
  
  
business = Business('David',income, cost,tax, employee_tax, tot_debt, monthly_debt)
business.add_employee('A', E1)
business.add_employee('B', E2)
business.add_employee('C', E3)
business.add_employee('D', E4)
business.add_employee('E', E5)
stats = business.get_stats()
employee = business.get_employees()

col1, col2, col3 = st.columns(3)
col1.metric('Ganancia', str(stats['revenue']['#']) + 'S', str(stats['revenue']['%']) + '%')
col2.metric('Beneficio Bruto', str(stats['gross profit']['#']) + 'S', str(stats['gross profit']['%']) + '%')
col3.metric('Ingresos Netos', str(stats['net income']['#']) + 'S', str(stats['net income']['%']) + '%')
st.write('_______')

coll1, coll2, coll3, coll4, coll5 = st.columns(5)
coll1.metric('Empleado 1', str(employee['A']['Salary']) + 'S',str(employee['A']['diff']) + 'S',delta_color='off' )
coll2.metric('Empleado 2', str(employee['C']['Salary']) + 'S',str(employee['D']['diff']) + 'S',delta_color='off' )
coll3.metric('Empleado 3', str(employee['B']['Salary']) + 'S',str(employee['B']['diff']) + 'S',delta_color='off' )
coll4.metric('Empleado 4', str(employee['D']['Salary']) + 'S',str(employee['C']['diff']) + 'S',delta_color='off' )
coll5.metric('Empleado 5', str(employee['E']['Salary']) + 'S',str(employee['E']['diff']) + 'S',delta_color='off' )
st.write('_______')

col1n, col2n, col3n = st.columns(3)
col1n.metric('Costo Operativo',str(stats['Operating Cost']['#']) + 'S', str(stats['Operating Cost']['%']) + '%', delta_color='off')
col2n.metric('Costo del Empleado',str(stats['Employee Cost']['#']) + 'S', str(stats['Employee Cost']['%']) + '%', delta_color='off')
col3n.metric('Deuda Bancaria',str(stats['Bank Debt']['#']) + 'S', str(stats['Bank Debt']['%']) + '%', delta_color='off')

employee_cost = business.tot_employee_salary
revenue = stats['revenue']['#']

fx = lambda x: x*(1-tax)*(1-employee_cost/revenue)
y = [fx(val) for val in range(25000)]
chart_data = pd.DataFrame(
    y,
    columns=['a'])

st.line_chart(chart_data)
