import pandas as pd

df = pd.read_csv("./workload/workload2.csv")

for index, row in df.iterrows():
    # Assuming row is a list of string values
    float_values = [float(value) for value in row]
    print(float_values)
