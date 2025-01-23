from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
import logging


def create_connection(user, password, account, warehouse, database, schema):
    connection_string = (
    f"snowflake://{user}:{password}@{account}/"
    f"{database}/{schema}?warehouse={warehouse}"
    )

    try:
        engine = create_engine(connection_string)
        connection = engine.connect()
        logging.info("Connected to snowflake successfully")
        return connection,engine
    except SQLAlchemyError as e:
        logging.info(f"error while connecting to snowflake : {e}")
        return None,None
    
def close_connection(connection,engine):
    if connection:
        connection.close()
        logging.info("snowflake connection closed")
    if engine:
        engine.dispose()
        logging.info("SQLAlchemy engine disposed")

def insert_raw_data(table_name,data_frame,connection,engine):
    logging.info(f"loading raw data into table {table_name}")

    if connection:
        try:
            data_frame.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            logging.info(f"raw data loaded successfully into {table_name} with {len(data_frame)} rows")
        except SQLAlchemyError as e:
            logging.info(f"error while load raw data : {e} ")
    else:
        logging.info(f"Failed to connect to the database and load data into table {table_name}")