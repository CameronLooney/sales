import pandas as pd

def import_data(path):
    df = pd.read_csv(path)
    return df

df = import_data("/Users/cameronlooney/Downloads/Unicorn+Companies-2/Unicorn_Companies.csv")
def data_preprocess(x):
    if type(x) == float or type(x) == int:
        return x
    x = x.replace('$', "")
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return 0.0

df['Funding'] = df['Funding'].apply(data_preprocess)
df["Valuation"] = df["Valuation"].apply(data_preprocess)

x = df.to_csv("/Users/cameronlooney/Documents/Unicorn.csv", index=False)