from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import os
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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

def is_file_processed(conn,file_name):
    query = text("SELECT 1 FROM processed_files WHERE file_name = :file_name")
    result = conn.execute(query, {'file_name': file_name}).fetchone()
    return result is not None

def mark_file_as_processed(conn, file_name):
    query = text("INSERT INTO processed_files (file_name) VALUES (:file_name)")
    conn.execute(query, {'file_name': file_name})