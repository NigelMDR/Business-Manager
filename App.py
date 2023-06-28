import numpy as np
import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation, Arrow
from bokeh.models import NumeralTickFormatter
from Business import *

st.set_page_config(layout="wide")
st.title('Descripción :blue[General]')
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

# fx = lambda x: ((x*(1-tax))*(1-stats['Operating Cost']['%']/100))*(1-stats['Employee Cost']['%']/100)
fx = lambda x: x*stats['gross profit']['%']/100
fx2 = lambda x: x*.27
fx3 = lambda x: x+1

x1 = [fx3(x) for x in range(-1,25000)]
y1 = []
i = 0
for x in x1:
  y1.append(fx(x))

bounds = 0
temp = y1[::-1]
for val in temp:
  if val <= stats['gross profit']['#']:
    bounds = x1[y1.index(val)]
    break;
    
# Verticle Line

x2 = [stats['revenue']['#'] for val in range(-1,25000)]
y2 = [fx3(x) for x in range(-1,25000)]

x5 = [bounds for val in range(-1,25000)]
y5 = [fx3(x) for x in range(-1,25000)]

# Horizontal line

x4 = [fx3(x) for x in range(-1,25000)]
y4 = [stats['gross profit']['#'] for x in range(-1,25000)]

p = figure(
    title='Informe de meses basados en proyección',
    x_axis_label='Ganancia',
    y_axis_label='Beneficio Bruto',
    sizing_mode="stretch_width",
    tooltips="(@x, @y)",
    x_range=(0, income+1000),
    y_range=(0, fx(income)),
    height=400,
    )

low_box = BoxAnnotation(top=monthly_debt, fill_alpha=0.2, fill_color='red')
p.add_layout(low_box)

p.line(x1, y1, line_width=2, color= 'navy', legend_label='Proyección')
p.line(x2, y2, line_width=2, color= 'red', legend_label='Ganancia', line_dash='dashed')
p.line(x4, y4, line_width=2, color= 'green', legend_label='Beneficio Bruto', line_dash='dashed')


p.xaxis.ticker = [0, income, stats['revenue']['#']]
p.yaxis.ticker = [0, stats['gross profit']['#'] ]
p.toolbar_location = "below"

st.bokeh_chart(p)

# ---------------------------------------------------------------------------- #
#                                     Notes                                    #
# ---------------------------------------------------------------------------- #

code = '''
     impuestos = 0.27
     Ganancia = ingreso*(1-impuesto)
     Costo operativo = (Ganancia - Costo) / Ganancia 
     Costo del empleado = (Ganancia - salario total del empleado) / Ganancia 
     Proyección(x) = x*(1 - impuesto)*(1 - costo operativo)*(1 - Costo del empleado)
     Beneficio Bruto = Ganancia - Costo - salario total del empleado
     Margen de beneficio bruto = Beneficio Bruto / Ganancia
     Ingresos Netos = Beneficio Bruto - Deuda bancaria mensual
    '''
st.code(code, language='ltex')

