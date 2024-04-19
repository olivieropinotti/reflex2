import reflex as rx
import psycopg2
import pandas as pd


def get_db_connection():
    return psycopg2.connect(
        host="aws-0-eu-central-1.pooler.supabase.com",
        database="postgres",
        port="5432",
        user="postgres.mvanppvxhnokujxfikxz",
        password="cDUKwRM13XmlNl99")
# connect to the database

conn = get_db_connection()

# make a function that executes a query in the database
def query(query: str, return_type: str = "list_of_dicts") -> pd.DataFrame or list[dict]:
    # return_type can be "list_of_dicts" or "dataframe"
    if return_type not in ["list_of_dicts", "dataframe"]:
        raise ValueError("return_type must be 'list_of_dicts' or 'dataframe'")
    
    with conn.cursor() as cur:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        if return_type == "list_of_dicts":
            # return a list of dictionaries with the column names as keys and the values as values
            return [dict(zip([desc[0] for desc in cur.description], row)) for row in cur.fetchall()]
        
        elif return_type == "dataframe":
            return pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])
        
        else:
            raise ValueError("return_type must be 'list_of_dicts' or 'dataframe'")