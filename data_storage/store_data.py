import pandas as pd

def save_to_csv(data, filename, folder="data"):
    path = f"{folder}/{filename}"
    data.to_csv(path, index=False)
