import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import io
def connect_postgres():
    conn = psycopg2.connect(
        host="localhost",
        database="covid",
        user="cameron",
        password="root")
    return conn


def import_data(path):
    df = pd.read_csv(path)
    return df



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


def csv_to_postgres(pg_user, pg_password, pg_host, pg_database,pg_port ,csv_path,pg_tablename):
    try:
        engine = create_engine('postgresql+psycopg2://{}:{}@{}:{}/{}'.format(pg_user, pg_password, pg_host,pg_port, pg_database))
        print("Connected to Postgres")
        df = import_data(csv_path)
        df['Funding'] = df['Funding'].apply(data_preprocess)
        df["Valuation"] = df["Valuation"].apply(data_preprocess)
        df.head(0).to_sql(pg_tablename, engine, if_exists='replace',index=False) #drops old table and creates new empty table

        conn = engine.raw_connection()
        cur = conn.cursor()
        output = io.StringIO()
        df.to_csv(output, sep='\t', header=False, index=False)
        output.seek(0)
        contents = output.getvalue()
        cur.copy_from(output, pg_tablename, null="") # null values become ''
        conn.commit()
        cur.close()
    except:
        print("Error in writing to postgres")

