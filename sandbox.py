import pandas as pd
import numpy as np

df = pd.read_csv("./workload/workload2.csv")

repeated_floats_list = []
for index, row in df.iterrows():
    # Assuming row is a list of string values
    #print(list(map(float, row.split(","))))
    #repeated_floats_list.append(float_values)
    float_values = [float(value) for value in row]
    float_values = float_values.instances
    #res = '[%s]' % ','.join(map(str, float_values))
    #res = res[1:-1]
    #float_values = list(map(float, res.split(",")))
    #res = np.array(row, dtype=float)
    print(float_values)
    #print(repeated_floats_list)
