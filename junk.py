import numpy as np
import pandas as pd


table_xy = {}
arr_x = [1,2,3]
arr_y = [1,2,3]
table_xy['gross income'] = {'x': arr_x, 'y': arr_y}
print(table_xy['gross income'].i)


arr = [1,2]
print(arr)

def step_function(const: None, step, max):
  arr = [0]*max
  if const:
    i = 0
    for x in range(max):
      arr[x] = const
      
  else:
    i = 0
    for x in range(max):
      arr[x] = i
      i += step
  
  return arr