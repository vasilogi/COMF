import pandas as pd

def read_datafile(CSV):
    # CSV: absolute path of the csv file
    # read the CSV file
    df           = pd.read_csv(CSV)
    conversion   = df['conversion'].to_numpy()
    time         = df['time'].to_numpy()
    temperature  = df['temperature'].to_numpy()[0]

    return conversion, time, temperature