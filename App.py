import numpy as np
import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, Arrow
from bokeh.models import NumeralTickFormatter
from Business import *

st.set_page_config(layout="wide")
st.title('Estado :blue[Financiero]')
# ---------------------------------------------------------------------------- #
#                                Get User Input                                #
# ---------------------------------------------------------------------------- #

with st.sidebar:  
  st.title(':blue[ _Negocio_ ] Estadísticas :bar_chart:')
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
  projection = st.number_input('Objetivo para el próximo mes', value=income)

# ---------------------------------------------------------------------------- #
#                              Use Business Class                              #
# ---------------------------------------------------------------------------- #
  
business = Business('David',income, cost,tax, employee_tax, tot_debt, monthly_debt)
business.add_employee('A', E1)
business.add_employee('B', E2)
business.add_employee('C', E3)
business.add_employee('D', E4)
business.add_employee('E', E5)
stats = business.get_stats()
employee = business.get_employees()

def get_data():
  table_xy = {}
  M = 25000
  
  x = [x for x in range(1,M)]
  fx1 = lambda x: x*stats['gross profit']['%']/100
  y = [fx1(x) for x in x]
  table_xy['gross profit margin'] = {'x': x, 'y': y, 'name':'Margen de ingresos brutos'}
  
  y = [x for x in range(1,M)]
  x = [stats['revenue']['#'] for x in y]
  table_xy['revenue'] = {'x': x, 'y': y, 'name':'Ganancia'}
  
  x = [round(projection*(1-tax),2) for x in range(1,M)]
  y = [x for x in range(1,M)]
  table_xy['projection'] = {'x': x, 'y': y, 'name':'Proyección'}
  
  x = [x for x in range(1,M)]
  temp = fx1(round(projection*(1-tax),2))
  y = [temp for x in range(1,M)]
  table_xy['Gross profit'] = {'x': x, 'y': y, 'name':'Beneficio Bruto'}

  val = 0
  temp = fx1(round(projection*(1-tax),2))
  yz = table_xy['gross profit margin']['y']
  for idx, y in enumerate(yz):
    if y >= monthly_debt:
      val = idx
      break;
  x = [val for i in yz]
  table_xy['Gross profit intercept Goal'] = {'x': x, 'y': yz, 'name':'umbral'}

  
  x = [x for x in range(1,M)]
  fx4 = lambda x: x*(1-tax) - cost - stats['Employees Salary']
  y = [fx4(x) for x in x]
  table_xy['Gross income'] = {'x': x, 'y': y, 'name':'Ingresos brutos'}

  y = [x for x in range(1,M)]
  x = [income for x in y]
  table_xy['income'] = {'x': x, 'y': y, 'name':'income'}

  x = [x for x in range(1,M)]
  temp = fx4(income)
  y = [temp for i in x]
  table_xy['f(income)'] = {'x': x, 'y': y, 'name':'f(income)'}
  
  val = 0
  yz = table_xy['Gross income']['y']
  for idx, y in enumerate(yz):
    if y >= 0:
      val = idx
      break;
  
  x = [val for i in yz]
  table_xy['Danger'] = {'x': x, 'y': yz, 'name':'peligro'}

  return table_xy
table_xy = get_data()

# ---------------------------------------------------------------------------- #
#                               Display Statistic                              #
# ---------------------------------------------------------------------------- #

col1, col2, col3, col4 = st.columns(4)
col1.metric(':chart_with_downwards_trend: Ganancia', str(stats['revenue']['#']) + 'S', str(stats['revenue']['%']) + '%')
col2.metric(':bar_chart: Beneficio Bruto', str(stats['gross profit']['#']) + 'S', str(stats['gross profit']['%']) + '%')
col3.metric(':chart_with_upwards_trend: Ingresos Netos', str(stats['net income']['#']) + 'S', str(stats['net income']['%']) + '%')
if table_xy['projection']['x'][0] > table_xy['Gross profit intercept Goal']['x'][0]:
    col4.metric(':umbrella: Umbral','n/a')
else:
    final = round(table_xy['Gross profit intercept Goal']['x'][0]/(1-tax),2)
    col4.metric(':warning: Umbral',final, round((final-income)/final*100,2))
st.write('_______')

coll1, coll2, coll3, coll4, coll5 = st.columns(5)
coll1.metric(':male-technologist: Empleado 1', str(employee['A']['Salary']) + 'S',str(employee['A']['diff']) + 'S',delta_color='off' )
coll2.metric(':male-office-worker: Empleado 2', str(employee['C']['Salary']) + 'S',str(employee['D']['diff']) + 'S',delta_color='off' )
coll3.metric(':male-technologist: Empleado 3', str(employee['B']['Salary']) + 'S',str(employee['B']['diff']) + 'S',delta_color='off' )
coll4.metric(':male-office-worker: Empleado 4', str(employee['D']['Salary']) + 'S',str(employee['C']['diff']) + 'S',delta_color='off' )
coll5.metric(':male-technologist: Empleado 5', str(employee['E']['Salary']) + 'S',str(employee['E']['diff']) + 'S',delta_color='off' )
st.write('_______')

col1n, col2n, col3n = st.columns(3)
col1n.metric(':bar_chart: Costo Operativo',str(stats['Operating Cost']['#']) + 'S', str(stats['Operating Cost']['%']) + '%', delta_color='off')
col2n.metric(':bar_chart: Costo del Empleado',str(stats['Employee Cost']['#']) + 'S', str(stats['Employee Cost']['%']) + '%', delta_color='off')
col3n.metric(':bar_chart: Deuda Bancaria',str(stats['Bank Debt']['#']) + 'S', str(stats['Bank Debt']['%']) + '%', delta_color='off')

# ---------------------------------------------------------------------------- #
#                                   Graphing                                   #
# ---------------------------------------------------------------------------- #




p1 = figure(
    title='Proyección usando el Margen de Ingresos Brutos',
    x_axis_label='Ganancia',
    y_axis_label='Beneficio Bruto',
    sizing_mode="stretch_width",
    tooltips="(@x, @y)",
    height=400,
    )

p1.toolbar_location = "below"
p1.xaxis.ticker = [0, table_xy['projection']['x'][0], table_xy['Gross profit intercept Goal']['x'][0]]
p1.yaxis.ticker = [0, stats['gross profit']['#'] ]
p1.line(table_xy['gross profit margin']['x'],table_xy['gross profit margin']['y'] , line_width=2, color= 'navy', legend_label=table_xy['gross profit margin']['name'])
p1.line(table_xy['Gross profit intercept Goal']['x'], table_xy['Gross profit intercept Goal']['y'], line_width=2, color= 'red', legend_label=table_xy['Gross profit intercept Goal']['name'], line_dash='dashed')
# p1.line(table_xy['revenue']['x'], table_xy['revenue']['y'], line_width=2, color= 'red', legend_label=table_xy['revenue']['name'], line_dash='dashed')
p1.line(table_xy['projection']['x'], table_xy['projection']['y'], line_width=2, color= 'blue', legend_label=table_xy['projection']['name'], line_dash='dashed')
p1.line(table_xy['Gross profit']['x'], table_xy['Gross profit']['y'], line_width=2, color= 'green', legend_label=table_xy['Gross profit']['name'], line_dash='dashed')

p2 = figure(
    title='Ingresos Brutos',
    x_axis_label='Ingreso',
    y_axis_label='Beneficio Bruto',
    sizing_mode="stretch_width",
    tooltips="(@x, @y)",
    height=400,
    )

p2.toolbar_location = "below"
p2.xaxis.ticker = [0, income, table_xy['Danger']['x'][0]]
p2.yaxis.ticker = [0, stats['gross profit']['#'] ]
p2.line(table_xy['Gross income']['x'], table_xy['Gross income']['y'], line_width=2, color= 'orange', legend_label=table_xy['Gross income']['name'])
p2.line(table_xy['income']['x'], table_xy['income']['y'], line_width=2, color= 'blue', legend_label=table_xy['income']['name'], line_dash='dashed')
p2.line(table_xy['f(income)']['x'], table_xy['f(income)']['y'], line_width=2, color= 'black', legend_label=table_xy['f(income)']['name'], line_dash='dashed')
p2.line(table_xy['Danger']['x'], table_xy['Danger']['y'], line_width=2, color= 'red', legend_label=table_xy['Danger']['name'], line_dash='dashed')

low_box = BoxAnnotation(top=monthly_debt, fill_alpha=0.2, fill_color='red')
p1.add_layout(low_box)
low_box2 = BoxAnnotation(top=monthly_debt, fill_alpha=0.2, fill_color='red')
p2.add_layout(low_box2)

st.bokeh_chart(p1)
st.bokeh_chart(p2)

# ---------------------------------------------------------------------------- #
#                                     Notes                                    #
# ---------------------------------------------------------------------------- #


code = '''

     Impuesto % : Porcentaje tomado por la empresa
     Pago de Empleados % : Porcentaje de cada empleado que se llevará a casa 'salario'

     impuestos = 0.27
     # Ganancia = ingreso*(1-impuestos)
     % Costo operativo = 1 - (Ganancia - (Los Gastos Operativos)) / Ganancia * 100
     # salario total del empleado = (Pago de Empleados)/100 * (Empleado 1 +  Empleado 2 + ... + Empleado 5)
     % Costo del empleado = 1 - (Ganancia - (salario total del empleado)) / Ganancia * 100
     # Beneficio Bruto = Ganancia - (Los Gastos Operativos) - (salario total del empleado)
     % Margen de beneficio bruto = 1 - (Beneficio Bruto) / Ganancia * 100
     # Ingresos Netos = (Beneficio Bruto) - (Deuda bancaria mensual)
     
     x es la variable
     Margen de ingresos brutos = x * (Margen de beneficio bruto)
     ingresos brutos = x*(1-tax) - (Los Gastos Operativos) - (salario total del empleado)
     
     # intercept = (punto cuando "Margen de ingresos brutos = Mensualidad")
     # umbral = intercept + intercept*(1-tax)
     % expected increase to reach threshold = (umbral - ingreso)/umbral
     
    '''
st.code(code, language='html')



