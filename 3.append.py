import pandas as pd
import glob

data_sources = glob.glob("./outputs/*.csv")

df = pd.DataFrame()

for data_source in data_sources:
    data = pd.read_csv(f'{data_source}')
    df.append(data)

df.to_csv("final")
