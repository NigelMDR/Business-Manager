import numpy as np
arr = np.random.randn(20, 3)
arr = np.array()
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