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

# ---------------------------------------------------------------------------- #
#                               Display Statistic                              #
# ---------------------------------------------------------------------------- #

col1, col2, col3 = st.columns(3)
col1.metric(':chart_with_downwards_trend: Ganancia', str(stats['revenue']['#']) + 'S', str(stats['revenue']['%']) + '%')
col2.metric(':bar_chart: Beneficio Bruto', str(stats['gross profit']['#']) + 'S', str(stats['gross profit']['%']) + '%')
col3.metric(':chart_with_upwards_trend: Ingresos Netos', str(stats['net income']['#']) + 'S', str(stats['net income']['%']) + '%')
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

def get_data():
  
  M = 25000
  
  x1 = [x for x in range(1,M)]
  fx1 = lambda x: x*stats['gross profit']['%']/100
  y1 = [fx1(x) for x in x1]
  
  y2 = [x for x in range(1,M)]
  x2 = [stats['revenue']['#'] for x in y2]
  
  x3 = [x for x in range(1,M)]
  y3 = [stats['gross profit']['#'] for x in range(1,M)]

  x4 = [x for x in range(1,M)]
  fx4 = lambda x: x*(1-tax) - cost - stats['Employees Salary']
  y4 = [fx4(x) for x in x4]

  y5 = [x for x in range(1,M)]
  x5 = [income for x in y2]
  
  x6 = [x for x in range(1,M)]
  y6 = [fx4(income) for x in y2]
  
  val = 0
  y7 = [x for x in range(1,M)]
  for idx, y in enumerate(y4):
    if y >= 0:
      val = idx
      break;
    
  x7 = [val for x in y7]


  return x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7

x1,y1,x2,y2,x3,y3,x4,y4,x5,y5,x6,y6,x7,y7 = get_data()

p1 = figure(
    title='Margen de Ingresos Brutos',
    x_axis_label='Ganancia',
    y_axis_label='Beneficio Bruto',
    sizing_mode="stretch_width",
    tooltips="(@x, @y)",
    height=400,
    )

p1.toolbar_location = "below"
p1.xaxis.ticker = [0, income, stats['revenue']['#']]
p1.yaxis.ticker = [0, stats['gross profit']['#'] ]
p1.line(x1, y1, line_width=2, color= 'navy', legend_label='Margen de ingresos brutos')
p1.line(x2, y2, line_width=2, color= 'red', legend_label='Ganancia', line_dash='dashed')
p1.line(x3, y3, line_width=2, color= 'green', legend_label='Beneficio Bruto', line_dash='dashed')

p2 = figure(
    title='Ingresos Brutos',
    x_axis_label='Ingreso',
    y_axis_label='Beneficio Bruto',
    sizing_mode="stretch_width",
    tooltips="(@x, @y)",
    height=400,
    )

p2.toolbar_location = "below"
p2.xaxis.ticker = [0, income, x7[0]]
p2.yaxis.ticker = [0, stats['gross profit']['#'] ]
p2.line(x4, y4, line_width=2, color= 'orange', legend_label='Ingresos brutos')
p2.line(x5, y5, line_width=2, color= 'blue', legend_label='ingreso', line_dash='dashed')
p2.line(x6, y6, line_width=2, color= 'black', legend_label='n/a', line_dash='dashed')
p2.line(x7, y7, line_width=2, color= 'red', legend_label='Peligro', line_dash='dashed')

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
     
    '''
st.code(code, language='ltex')



